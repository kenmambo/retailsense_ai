-- RetailSense AI - Executive Dashboard Queries
-- This script provides executive-level insights and KPIs

-- Executive Summary Dashboard
WITH executive_metrics AS (
  -- Portfolio Overview
  SELECT 
    'Portfolio Overview' as section,
    'Total Products' as metric,
    CAST(COUNT(DISTINCT product_sku) AS STRING) as value,
    'Active products in portfolio' as description
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  SELECT 
    'Portfolio Overview',
    'Total Revenue',
    CONCAT('$', FORMAT('%.0f', SUM(total_revenue))),
    'Cumulative revenue generated'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  SELECT 
    'Portfolio Overview',
    'Average Product Value',
    CONCAT('$', FORMAT('%.0f', AVG(total_revenue))),
    'Revenue per product'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  -- Performance Metrics
  SELECT 
    'Performance Metrics',
    'Portfolio Conversion Rate',
    CONCAT(FORMAT('%.2f', AVG(view_to_purchase_rate) * 100), '%'),
    'Average conversion across all products'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  SELECT 
    'Performance Metrics',
    'High Performers',
    CONCAT(
      CAST(COUNT(CASE WHEN performance_score >= 75 THEN 1 END) AS STRING),
      ' of ',
      CAST(COUNT(*) AS STRING)
    ),
    'Products with performance score ≥ 75'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  -- Growth Analysis
  SELECT 
    'Growth Analysis',
    'Growing Products',
    CAST(COUNT(CASE WHEN trend_status = 'Growing' THEN 1 END) AS STRING),
    'Products showing positive revenue trend'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  SELECT 
    'Growth Analysis',
    'Declining Products',
    CAST(COUNT(CASE WHEN trend_status = 'Declining' THEN 1 END) AS STRING),
    'Products requiring attention'
  FROM `retail_intelligence.product_performance`
  
  UNION ALL
  
  -- Category Performance
  SELECT 
    'Category Performance',
    'Top Category',
    (
      SELECT category 
      FROM (
        SELECT category, SUM(total_revenue) as revenue
        FROM `retail_intelligence.product_performance`
        GROUP BY category
        ORDER BY revenue DESC
        LIMIT 1
      )
    ),
    'Highest revenue generating category'
  FROM `retail_intelligence.product_performance`
  LIMIT 1
  
  UNION ALL
  
  SELECT 
    'Category Performance',
    'Category Diversity',
    CAST(COUNT(DISTINCT category) AS STRING),
    'Number of product categories'
  FROM `retail_intelligence.product_performance`
)

SELECT * FROM executive_metrics
ORDER BY 
  CASE section
    WHEN 'Portfolio Overview' THEN 1
    WHEN 'Performance Metrics' THEN 2
    WHEN 'Growth Analysis' THEN 3
    WHEN 'Category Performance' THEN 4
  END,
  metric;

-- Top Performers Table
SELECT 
  '🏆 TOP 10 REVENUE GENERATORS' as title,
  '' as product_name,
  '' as category,
  '' as revenue,
  '' as trend,
  '' as performance_score

UNION ALL

SELECT 
  CAST(ROW_NUMBER() OVER(ORDER BY total_revenue DESC) AS STRING),
  SUBSTR(product_name, 1, 40),
  category,
  CONCAT('$', FORMAT('%.0f', total_revenue)),
  trend_status,
  CAST(ROUND(performance_score) AS STRING)
FROM `retail_intelligence.product_performance`
ORDER BY revenue DESC NULLS LAST
LIMIT 11;

-- Category Analysis
SELECT 
  '📊 CATEGORY PERFORMANCE ANALYSIS' as title,
  '' as category,
  '' as products,
  '' as revenue,
  '' as avg_conversion,
  '' as market_share

UNION ALL

SELECT 
  '',
  category,
  CAST(COUNT(*) AS STRING),
  CONCAT('$', FORMAT('%.0f', SUM(total_revenue))),
  CONCAT(FORMAT('%.2f', AVG(view_to_purchase_rate) * 100), '%'),
  CONCAT(FORMAT('%.1f', SUM(total_revenue) / (SELECT SUM(total_revenue) FROM `retail_intelligence.product_performance`) * 100), '%')
FROM `retail_intelligence.product_performance`
GROUP BY category
ORDER BY SUM(total_revenue) DESC NULLS LAST
LIMIT 11;

-- Performance Distribution
WITH performance_buckets AS (
  SELECT 
    CASE 
      WHEN performance_score >= 90 THEN 'Excellent (90+)'
      WHEN performance_score >= 75 THEN 'Good (75-89)'
      WHEN performance_score >= 50 THEN 'Average (50-74)'
      WHEN performance_score >= 25 THEN 'Below Average (25-49)'
      ELSE 'Poor (<25)'
    END as performance_tier,
    COUNT(*) as product_count,
    SUM(total_revenue) as tier_revenue
  FROM `retail_intelligence.product_performance`
  GROUP BY performance_tier
)

SELECT 
  '📈 PERFORMANCE DISTRIBUTION' as title,
  '' as tier,
  '' as products,
  '' as revenue,
  '' as percentage

UNION ALL

SELECT 
  '',
  performance_tier,
  CAST(product_count AS STRING),
  CONCAT('$', FORMAT('%.0f', tier_revenue)),
  CONCAT(FORMAT('%.1f', product_count / (SELECT COUNT(*) FROM `retail_intelligence.product_performance`) * 100), '%')
FROM performance_buckets
ORDER BY 
  CASE tier
    WHEN 'Excellent (90+)' THEN 1
    WHEN 'Good (75-89)' THEN 2
    WHEN 'Average (50-74)' THEN 3
    WHEN 'Below Average (25-49)' THEN 4
    WHEN 'Poor (<25)' THEN 5
    ELSE 6
  END;

-- Trend Analysis Summary
SELECT 
  '📊 BUSINESS TRENDS & PREDICTIONS' as section,
  'Revenue Trend' as metric,
  CASE 
    WHEN (SELECT COUNT(*) FROM `retail_intelligence.product_performance` WHERE trend_status = 'Growing') >
         (SELECT COUNT(*) FROM `retail_intelligence.product_performance` WHERE trend_status = 'Declining')
    THEN '📈 Portfolio Growing'
    ELSE '📉 Portfolio Declining'
  END as status,
  CONCAT(
    (SELECT COUNT(*) FROM `retail_intelligence.product_performance` WHERE trend_status = 'Growing'),
    ' growing vs ',
    (SELECT COUNT(*) FROM `retail_intelligence.product_performance` WHERE trend_status = 'Declining'),
    ' declining products'
  ) as details

UNION ALL

SELECT 
  'Business Trends & Predictions',
  'Forecast Revenue',
  '📊 30-Day Projection',
  CONCAT('$', FORMAT('%.0f', (
    SELECT SUM(forecast_value) 
    FROM ML.FORECAST(MODEL `retail_intelligence.revenue_forecasting_model`, STRUCT(30 as horizon))
  )))

UNION ALL

SELECT 
  'Business Trends & Predictions',
  'Customer Segments',
  '👥 Active Segments',
  CONCAT((
    SELECT COUNT(DISTINCT CENTROID_ID)
    FROM ML.PREDICT(
      MODEL `retail_intelligence.customer_segmentation_model`,
      (SELECT 1 as total_purchases, 100 as total_revenue, 50 as avg_order_value, 30 as days_active, 3 as unique_categories, 2 as device_diversity, 1 as geographic_reach)
    )
  ), ' customer segments identified');