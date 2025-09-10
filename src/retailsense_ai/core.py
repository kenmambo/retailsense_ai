"""
Core RetailSense AI module for BigQuery integration
"""

import os
import pandas as pd
import numpy as np
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import storage
import warnings
warnings.filterwarnings('ignore')

class RetailSenseAI:
    """
    RetailSense AI - Multimodal E-commerce Intelligence Engine
    
    This class handles the setup and core functionality for analyzing
    e-commerce data using BigQuery's AI capabilities.
    """
    def __init__(self, project_id=None, dataset_id="retail_intelligence", credentials_path=None):
        # Load credentials
        if credentials_path is None:
            credentials_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                "credentials", 
                "retailsense-ai-ceb777b5822d.json"
            )
        
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(
                f"Credentials file not found at {credentials_path}. "
                "Please ensure your service account JSON file is in the credentials/ directory."
            )
        
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        
        # Extract project_id from credentials if not provided
        if project_id is None:
            with open(credentials_path, 'r') as f:
                import json
                cred_data = json.load(f)
                project_id = cred_data['project_id']
        
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id, credentials=self.credentials)
        self.dataset_ref = f"{project_id}.{dataset_id}"
        
        print(f"🚀 RetailSense AI initialized!")
        print(f"   Project: {project_id}")
        print(f"   Dataset: {dataset_id}")
        
    def setup_environment(self):
        """Set up the BigQuery environment and datasets"""
        
        # Create dataset if it doesn't exist
        try:
            dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
            dataset.location = "US"
            dataset.description = "RetailSense AI multimodal e-commerce analysis"
            
            dataset = self.client.create_dataset(dataset, exists_ok=True)
            print(f"✅ Dataset {self.dataset_id} ready")
            
        except Exception as e:
            print(f"❌ Error setting up dataset: {e}")
            
        return True
    
    def load_ga4_data(self, start_date="20210101", end_date="20210331"):
        """Load and process GA4 e-commerce sample data"""
        
        query = f"""
        CREATE OR REPLACE TABLE `{self.dataset_ref}.base_sales` AS
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
          items.item_brand as brand
        FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
        UNNEST(items) as items
        WHERE event_name IN ('purchase', 'add_to_cart', 'view_item', 'begin_checkout')
          AND _TABLE_SUFFIX BETWEEN '{start_date}' AND '{end_date}'
          AND items.item_id IS NOT NULL
          AND items.price_in_usd > 0
        """
        
        job = self.client.query(query)
        job.result()  # Wait for completion
        
        print(f"✅ Base sales data loaded ({start_date} to {end_date})")
        
        # Get row count
        count_query = f"SELECT COUNT(*) as row_count FROM `{self.dataset_ref}.base_sales`"
        result = self.client.query(count_query).to_dataframe()
        print(f"   📊 Total records: {result['row_count'].iloc[0]:,}")
        
        return True
    
    def create_product_performance_table(self):
        """Create comprehensive product performance metrics"""
        
        query = f"""
        CREATE OR REPLACE TABLE `{self.dataset_ref}.product_performance` AS
        SELECT 
          product_sku,
          ANY_VALUE(product_name) as product_name,
          ANY_VALUE(category) as category,
          ANY_VALUE(brand) as brand,
          AVG(price) as avg_price,
          COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
          COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as total_views,
          COUNT(CASE WHEN event_name = 'add_to_cart' THEN 1 END) as total_cart_adds,
          COUNT(CASE WHEN event_name = 'begin_checkout' THEN 1 END) as total_checkouts,
          SUM(CASE WHEN event_name = 'purchase' THEN revenue END) as total_revenue,
          COUNT(DISTINCT user_pseudo_id) as unique_users,
          
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
          
          -- Revenue metrics
          SAFE_DIVIDE(
            SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
            COUNT(CASE WHEN event_name = 'purchase' THEN 1 END)
          ) as revenue_per_purchase,
          
          SAFE_DIVIDE(
            SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
            COUNT(CASE WHEN event_name = 'view_item' THEN 1 END)
          ) as revenue_per_view
          
        FROM `{self.dataset_ref}.base_sales`
        GROUP BY product_sku
        HAVING COUNT(*) >= 5  -- Filter for products with sufficient activity
        ORDER BY total_revenue DESC
        """
        
        job = self.client.query(query)
        job.result()
        
        print("✅ Product performance table created")
        
        # Show summary stats
        summary_query = f"""
        SELECT 
          COUNT(*) as total_products,
          IFNULL(SUM(total_revenue), 0) as total_revenue,
          IFNULL(AVG(view_to_purchase_rate), 0) as avg_conversion_rate,
          COUNT(DISTINCT category) as unique_categories
        FROM `{self.dataset_ref}.product_performance`
        """
        
        summary = self.client.query(summary_query).to_dataframe()
        print(f"   📊 Products analyzed: {summary['total_products'].iloc[0]:,}")
        print(f"   💰 Total revenue: ${summary['total_revenue'].iloc[0]:,.2f}")
        print(f"   📈 Avg conversion: {summary['avg_conversion_rate'].iloc[0]*100:.2f}%")
        print(f"   🏷️  Categories: {summary['unique_categories'].iloc[0]}")
        
        return True
    
    def get_performance_data(self):
        """Get product performance data as DataFrame"""
        query = f"SELECT * FROM `{self.dataset_ref}.product_performance` ORDER BY total_revenue DESC"
        return self.client.query(query).to_dataframe()
    
    def get_category_analysis(self):
        """Get category-level analysis"""
        query = f"""
        SELECT 
          category,
          COUNT(*) as product_count,
          SUM(total_revenue) as category_revenue,
          AVG(view_to_purchase_rate) as avg_conversion_rate,
          SUM(total_views) as total_views,
          SUM(total_purchases) as total_purchases
        FROM `{self.dataset_ref}.product_performance`
        GROUP BY category
        ORDER BY category_revenue DESC
        """
        return self.client.query(query).to_dataframe()