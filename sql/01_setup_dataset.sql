-- RetailSense AI - Dataset Setup Script
-- This script creates the dataset and basic structure for RetailSense AI

-- Create the retail intelligence dataset if it doesn't exist
CREATE SCHEMA IF NOT EXISTS `retail_intelligence`
OPTIONS(
  description="RetailSense AI multimodal e-commerce analysis dataset",
  location="US"
);

-- Grant necessary permissions (run this if you need to share access)
-- GRANT `roles/bigquery.dataViewer` ON SCHEMA `retail_intelligence` TO "user:someone@example.com";

-- Display dataset information
SELECT 
  schema_name,
  location,
  creation_time,
  last_modified_time
FROM `INFORMATION_SCHEMA.SCHEMATA`
WHERE schema_name = 'retail_intelligence';

-- Show message
SELECT "✅ RetailSense AI dataset setup completed successfully!" as setup_status;