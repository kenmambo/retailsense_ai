-- RetailSense AI - ML Predictions and Insights
-- This script generates predictions using the trained ML models

-- 1. Revenue Forecast for next 30 days
WITH revenue_forecast AS (
  SELECT 
    forecast_timestamp as forecast_date,
    forecast_value as predicted_revenue,
    prediction_interval_lower_bound as lower_bound,
    prediction_interval_upper_bound as upper_bound
  FROM ML.FORECAST(
    MODEL `retail_intelligence.revenue_forecasting_model`,
    STRUCT(30 as horizon)  -- 30 days forecast
  )
)
SELECT 
  '📈 Revenue Forecast (Next 30 Days)' as analysis_type,
  CAST(COUNT(*) AS STRING) as forecast_days,
  CONCAT('$', FORMAT('%.2f', SUM(predicted_revenue))) as total_predicted_revenue,
  CONCAT('$', FORMAT('%.2f', AVG(predicted_revenue))) as avg_daily_revenue,
  CONCAT('$', FORMAT('%.2f', SUM(lower_bound))) as conservative_estimate,
  CONCAT('$', FORMAT('%.2f', SUM(upper_bound))) as optimistic_estimate
FROM revenue_forecast

UNION ALL

-- 2. Customer Segmentation Analysis
SELECT 
  '👥 Customer Segmentation' as analysis_type,
  CONCAT('Segment ', CAST(CENTROID_ID AS STRING)) as segment_id,
  CAST(COUNT(*) AS STRING) as customer_count,
  CONCAT('$', FORMAT('%.2f', AVG(total_revenue))) as avg_revenue_per_customer,
  CONCAT('$', FORMAT('%.2f', AVG(avg_order_value))) as avg_order_value,
  CAST(ROUND(AVG(total_purchases)) AS STRING) as avg_purchases_per_customer
FROM ML.PREDICT(
  MODEL `retail_intelligence.customer_segmentation_model`,
  (
    SELECT 
      user_pseudo_id,
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
      IFNULL(SUM(CASE WHEN event_name = 'purchase' THEN revenue END), 0) as total_revenue,
      SAFE_DIVIDE(
        SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
        COUNT(CASE WHEN event_name = 'purchase' THEN 1 END)
      ) as avg_order_value,
      DATE_DIFF(
        MAX(PARSE_DATE('%Y%m%d', event_date)),
        MIN(PARSE_DATE('%Y%m%d', event_date)),
        DAY
      ) + 1 as days_active,
      COUNT(DISTINCT category) as unique_categories,
      COUNT(DISTINCT device_category) as device_diversity,
      COUNT(DISTINCT country) as geographic_reach
    FROM `retail_intelligence.base_sales`
    WHERE user_pseudo_id IS NOT NULL
    GROUP BY user_pseudo_id
    HAVING total_purchases > 0
  )
)
GROUP BY CENTROID_ID
ORDER BY analysis_type, avg_revenue_per_customer DESC;

-- 3. Product Performance Predictions
-- Predict which current products will be top performers
CREATE OR REPLACE TABLE `retail_intelligence.product_predictions` AS
WITH current_products AS (
  SELECT 
    product_sku,
    product_name,
    category,
    COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as current_views,
    COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as current_purchases,
    AVG(price) as avg_price,
    COUNT(DISTINCT user_pseudo_id) as current_users,
    COUNT(DISTINCT country) as current_geographic_reach,
    SAFE_DIVIDE(
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END),
      COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
    ) as current_conversion_rate
  FROM `retail_intelligence.base_sales`
  GROUP BY product_sku, product_name, category
  HAVING current_views > 10  -- Only products with sufficient data
)
SELECT 
  cp.product_sku,
  cp.product_name,
  cp.category,
  cp.current_views,
  cp.current_purchases,
  pred.predicted_is_top_performer,
  pred.predicted_is_top_performer_probs[OFFSET(0)].prob as probability_top_performer
FROM ML.PREDICT(
  MODEL `retail_intelligence.product_performance_classifier`,
  (
    SELECT 
      product_sku,
      current_views as early_views,
      current_purchases as early_purchases,
      avg_price,
      current_users as early_users,
      current_geographic_reach as early_geographic_reach,
      IFNULL(current_conversion_rate, 0) as early_conversion_rate
    FROM current_products
  )
) pred
JOIN current_products cp ON pred.product_sku = cp.product_sku
ORDER BY pred.predicted_is_top_performer_probs[OFFSET(0)].prob DESC;

-- 4. Business Intelligence Summary
SELECT 
  '🎯 Business Intelligence Summary' as report_section,
  '' as metric,
  '' as value,
  '' as insight

UNION ALL

SELECT 
  'Revenue Insights',
  'Current Portfolio Value',
  CONCAT('$', FORMAT('%.2f', SUM(total_revenue))),
  CONCAT(COUNT(*), ' active products generating revenue')
FROM `retail_intelligence.product_performance`

UNION ALL

SELECT 
  'Performance Insights',
  'High Performers',
  CAST(COUNT(CASE WHEN performance_score >= 75 THEN 1 END) AS STRING),
  CONCAT(ROUND(COUNT(CASE WHEN performance_score >= 75 THEN 1 END) / COUNT(*) * 100), '% of portfolio')
FROM `retail_intelligence.product_performance`

UNION ALL

SELECT 
  'Growth Insights',
  'Growing Products',
  CAST(COUNT(CASE WHEN trend_status = 'Growing' THEN 1 END) AS STRING),
  CONCAT('vs ', COUNT(CASE WHEN trend_status = 'Declining' THEN 1 END), ' declining products')
FROM `retail_intelligence.product_performance`

UNION ALL

SELECT 
  'Category Insights',
  'Top Category',
  (SELECT category FROM (
    SELECT category, SUM(total_revenue) as cat_revenue 
    FROM `retail_intelligence.product_performance` 
    GROUP BY category 
    ORDER BY cat_revenue DESC 
    LIMIT 1
  )),
  'Highest revenue generating category'

UNION ALL

SELECT 
  'Prediction Insights',
  'Future Top Performers',
  CAST((SELECT COUNT(*) FROM `retail_intelligence.product_predictions` WHERE predicted_is_top_performer = true) AS STRING),
  'Products predicted to become top performers'

ORDER BY report_section, metric;