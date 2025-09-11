-- RetailSense AI - Product Performance Analytics
-- This script creates comprehensive product performance metrics

-- Create product performance table with advanced metrics
CREATE OR REPLACE TABLE `retail_intelligence.product_performance` AS
WITH product_metrics AS (
  SELECT 
    product_sku,
    ANY_VALUE(product_name) as product_name,
    ANY_VALUE(category) as category,
    ANY_VALUE(brand) as brand,
    AVG(price) as avg_price,
    
    -- Event counts
    COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
    COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as total_views,
    COUNT(CASE WHEN event_name = 'add_to_cart' THEN 1 END) as total_cart_adds,
    COUNT(CASE WHEN event_name = 'begin_checkout' THEN 1 END) as total_checkouts,
    
    -- Revenue metrics
    SUM(CASE WHEN event_name = 'purchase' THEN revenue END) as total_revenue,
    COUNT(DISTINCT user_pseudo_id) as unique_users,
    COUNT(DISTINCT event_date) as active_days,
    
    -- Geographic diversity
    COUNT(DISTINCT country) as countries_sold,
    COUNT(DISTINCT device_category) as device_types,
    
    -- Conversion metrics
    SAFE_DIVIDE(
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END),
      COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
    ) as view_to_purchase_rate,
    
    SAFE_DIVIDE(
      COUNT(CASE WHEN event_name = 'add_to_cart' THEN 1 END),
      COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
    ) as view_to_cart_rate,
    
    SAFE_DIVIDE(
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END),
      COUNT(CASE WHEN event_name = 'add_to_cart' THEN 1 END)
    ) as cart_to_purchase_rate,
    
    -- Revenue per interaction
    SAFE_DIVIDE(
      SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END)
    ) as revenue_per_purchase,
    
    SAFE_DIVIDE(
      SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
      COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
    ) as revenue_per_view,
    
    -- Time-based analysis
    MIN(PARSE_DATE('%Y%m%d', event_date)) as first_sale_date,
    MAX(PARSE_DATE('%Y%m%d', event_date)) as last_sale_date
    
  FROM `retail_intelligence.base_sales`
  GROUP BY product_sku
  HAVING COUNT(*) >= 5  -- Filter for products with sufficient activity
),

-- Add trend analysis
trend_analysis AS (
  SELECT 
    product_sku,
    -- Calculate revenue trend using correlation with date
    CORR(
      UNIX_DATE(PARSE_DATE('%Y%m%d', event_date)), 
      CASE WHEN event_name = 'purchase' THEN revenue ELSE 0 END
    ) as revenue_trend_correlation
  FROM `retail_intelligence.base_sales`
  WHERE event_name = 'purchase'
  GROUP BY product_sku
)

SELECT 
  pm.*,
  ta.revenue_trend_correlation,
  CASE 
    WHEN ta.revenue_trend_correlation > 0.1 THEN 'Growing'
    WHEN ta.revenue_trend_correlation < -0.1 THEN 'Declining'
    ELSE 'Stable'
  END as trend_status,
  
  -- Performance score (composite metric)
  ROUND(
    (COALESCE(pm.view_to_purchase_rate, 0) * 40) +
    (COALESCE(pm.revenue_per_view, 0) / 10 * 30) +
    (LEAST(pm.unique_users / 100.0, 1.0) * 20) +
    (CASE WHEN ta.revenue_trend_correlation > 0 THEN 10 ELSE 0 END),
    2
  ) as performance_score
  
FROM product_metrics pm
LEFT JOIN trend_analysis ta ON pm.product_sku = ta.product_sku
ORDER BY pm.total_revenue DESC;

-- Show analytics summary
SELECT 
  'Product Analytics Created' as status,
  COUNT(*) as products_analyzed,
  ROUND(SUM(total_revenue), 2) as total_portfolio_revenue,
  ROUND(AVG(view_to_purchase_rate) * 100, 2) as avg_conversion_rate_pct,
  COUNT(DISTINCT category) as unique_categories,
  COUNT(CASE WHEN trend_status = 'Growing' THEN 1 END) as growing_products,
  COUNT(CASE WHEN trend_status = 'Declining' THEN 1 END) as declining_products,
  COUNT(CASE WHEN trend_status = 'Stable' THEN 1 END) as stable_products
FROM `retail_intelligence.product_performance`;

-- Show top performers
SELECT 
  CONCAT('🏆 Top 10 Products by Revenue') as section,
  '' as product_name,
  '' as category,
  NULL as revenue,
  '' as trend
UNION ALL
SELECT 
  CAST(ROW_NUMBER() OVER(ORDER BY total_revenue DESC) AS STRING),
  product_name,
  category,
  total_revenue,
  trend_status
FROM `retail_intelligence.product_performance`
ORDER BY revenue DESC NULLS LAST
LIMIT 11;