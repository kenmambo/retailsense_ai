-- RetailSense AI - BigQuery ML Models
-- This script creates machine learning models for advanced analytics

-- 1. Revenue Forecasting Model (ARIMA_PLUS)
CREATE OR REPLACE MODEL `retail_intelligence.revenue_forecasting_model`
OPTIONS(
  model_type='ARIMA_PLUS',
  time_series_timestamp_col='date',
  time_series_data_col='daily_revenue',
  auto_arima=TRUE,
  data_frequency='DAILY'
) AS
SELECT 
  PARSE_DATE('%Y%m%d', event_date) as date,
  SUM(revenue) as daily_revenue
FROM `retail_intelligence.base_sales`
WHERE event_name = 'purchase' 
  AND revenue IS NOT NULL
  AND revenue > 0
GROUP BY date
ORDER BY date;

-- 2. Customer Segmentation Model (K-means)
CREATE OR REPLACE MODEL `retail_intelligence.customer_segmentation_model`
OPTIONS(
  model_type='KMEANS',
  num_clusters=5,
  standardize_features=TRUE
) AS
WITH customer_features AS (
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
  HAVING total_purchases > 0  -- Only customers who made purchases
)
SELECT 
  total_purchases,
  total_revenue,
  IFNULL(avg_order_value, 0) as avg_order_value,
  days_active,
  unique_categories,
  device_diversity,
  geographic_reach
FROM customer_features;

-- 3. Product Classification Model (Logistic Regression)
-- Predicts if a product will be a top performer based on early metrics
CREATE OR REPLACE MODEL `retail_intelligence.product_performance_classifier`
OPTIONS(
  model_type='LOGISTIC_REG',
  input_label_cols=['is_top_performer']
) AS
WITH early_metrics AS (
  SELECT 
    product_sku,
    -- Features from first 30 days
    COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as early_views,
    COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as early_purchases,
    AVG(price) as avg_price,
    COUNT(DISTINCT user_pseudo_id) as early_users,
    COUNT(DISTINCT country) as early_geographic_reach,
    SAFE_DIVIDE(
      COUNT(CASE WHEN event_name = 'purchase' THEN 1 END),
      COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
    ) as early_conversion_rate
  FROM `retail_intelligence.base_sales`
  WHERE PARSE_DATE('%Y%m%d', event_date) <= DATE_ADD(
    (SELECT MIN(PARSE_DATE('%Y%m%d', event_date)) FROM `retail_intelligence.base_sales`), 
    INTERVAL 30 DAY
  )
  GROUP BY product_sku
),
performance_labels AS (
  SELECT 
    product_sku,
    total_revenue,
    CASE 
      WHEN total_revenue >= PERCENTILE_CONT(total_revenue, 0.8) OVER() THEN true
      ELSE false
    END as is_top_performer
  FROM `retail_intelligence.product_performance`
)
SELECT 
  em.early_views,
  em.early_purchases,
  em.avg_price,
  em.early_users,
  em.early_geographic_reach,
  IFNULL(em.early_conversion_rate, 0) as early_conversion_rate,
  pl.is_top_performer
FROM early_metrics em
JOIN performance_labels pl ON em.product_sku = pl.product_sku
WHERE em.early_views > 0;  -- Only products with some early activity

-- Show model training results
SELECT 
  'ML Models Training Completed' as status,
  'revenue_forecasting_model' as model_1,
  'customer_segmentation_model' as model_2,
  'product_performance_classifier' as model_3;

-- Get model evaluation metrics
SELECT 
  model_name,
  model_type,
  feature_columns,
  label_columns,
  training_run_time,
  evaluation_metrics
FROM `retail_intelligence.INFORMATION_SCHEMA.ML_MODELS`
WHERE model_name IN (
  'revenue_forecasting_model',
  'customer_segmentation_model', 
  'product_performance_classifier'
);