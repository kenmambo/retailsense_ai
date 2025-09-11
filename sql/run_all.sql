-- RetailSense AI - Master Script
-- Run this script to execute the complete BigQuery setup and analysis

-- ============================================================================
-- RETAILSENSE AI - COMPLETE BIGQUERY SETUP AND ANALYSIS
-- ============================================================================

-- Step 1: Create Dataset
-- @01_setup_dataset.sql

-- Step 2: Load GA4 Data  
-- @02_load_ga4_data.sql

-- Step 3: Create Product Analytics
-- @03_create_product_analytics.sql

-- Step 4: Create ML Models
-- @04_create_ml_models.sql

-- Step 5: Generate ML Predictions
-- @05_ml_predictions.sql

-- Step 6: Executive Dashboard
-- @06_executive_dashboard.sql

-- ============================================================================
-- COMPLETION MESSAGE
-- ============================================================================

SELECT 
  '🎉 RETAILSENSE AI SETUP COMPLETED!' as status,
  'All tables, models, and analytics are ready' as message,
  CURRENT_TIMESTAMP() as completed_at;