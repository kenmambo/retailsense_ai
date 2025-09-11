-- RetailSense AI - Load GA4 E-commerce Data
-- This script loads and processes GA4 e-commerce sample data for analysis

-- Load base sales data from Google's public GA4 dataset
CREATE OR REPLACE TABLE `retail_intelligence.base_sales` AS
SELECT 
  items.item_id as product_sku,
  items.item_name as product_name,
  items.item_category as category,
  items.price_in_usd as price,
  event_date,
  user_pseudo_id,
  event_name,
  ecommerce.purchase_revenue_in_usd as revenue,
  items.item_variant as variant,
  items.item_brand as brand,
  traffic_source.name as traffic_source,
  device.category as device_category,
  geo.country as country,
  geo.city as city
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
UNNEST(items) as items
WHERE event_name IN ('purchase', 'add_to_cart', 'view_item', 'begin_checkout')
  AND _TABLE_SUFFIX BETWEEN '20210101' AND '20210331'  -- Q1 2021 data
  AND items.item_id IS NOT NULL
  AND items.price_in_usd > 0;

-- Show data loading summary
SELECT 
  'Base Sales Data Loaded' as status,
  COUNT(*) as total_records,
  COUNT(DISTINCT product_sku) as unique_products,
  COUNT(DISTINCT user_pseudo_id) as unique_users,
  COUNT(DISTINCT event_date) as date_range_days,
  ROUND(SUM(CASE WHEN event_name = 'purchase' THEN revenue END), 2) as total_revenue,
  COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
  COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as total_views
FROM `retail_intelligence.base_sales`;

-- Show sample data
SELECT 
  product_name,
  category,
  event_name,
  price,
  revenue
FROM `retail_intelligence.base_sales`
WHERE event_name = 'purchase'
ORDER BY revenue DESC
LIMIT 10;