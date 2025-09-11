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
from dotenv import load_dotenv
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

class RetailSenseAI:
    """
    RetailSense AI - Multimodal E-commerce Intelligence Engine
    
    This class handles the setup and core functionality for analyzing
    e-commerce data using BigQuery's AI capabilities.
    """
    def __init__(self, project_id=None, dataset_id=None, credentials_path=None):
        # Load from environment variables first
        if project_id is None:
            project_id = os.getenv('PROJECT_ID')
        
        if dataset_id is None:
            dataset_id = os.getenv('DATASET_ID', 'retail_intelligence')
        
        if credentials_path is None:
            credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            
            # If still None, try default location
            if credentials_path is None:
                credentials_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                    "credentials", 
                    "retailsense-ai-credentials.json"
                )
        
        # Validate credentials file exists
        if not os.path.exists(credentials_path):
            available_files = []
            cred_dir = os.path.dirname(credentials_path)
            if os.path.exists(cred_dir):
                available_files = [f for f in os.listdir(cred_dir) if f.endswith('.json')]
            
            error_msg = (
                f"Credentials file not found at {credentials_path}.\n\n"
                "To set up BigQuery access:\n"
                "1. Create a Google Cloud Project\n"
                "2. Enable BigQuery API\n"
                "3. Create a service account with BigQuery permissions\n"
                "4. Download the JSON key file to credentials/\n"
                "5. Update your .env file with the correct path\n\n"
            )
            
            if available_files:
                error_msg += f"Available credential files in {cred_dir}: {', '.join(available_files)}\n"
            else:
                error_msg += "No credential files found in credentials/ directory.\n"
                
            error_msg += "\nFor demo mode, use: uv run python -m retailsense_ai.main --demo"
            
            raise FileNotFoundError(error_msg)
        
        # Load credentials
        try:
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        except Exception as e:
            raise ValueError(f"Invalid credentials file {credentials_path}: {e}")
        
        # Extract project_id from credentials if not provided
        if project_id is None:
            try:
                with open(credentials_path, 'r') as f:
                    import json
                    cred_data = json.load(f)
                    project_id = cred_data['project_id']
            except Exception as e:
                raise ValueError(f"Could not extract project_id from credentials: {e}")
        
        if not project_id:
            raise ValueError("Project ID is required. Set it in .env file or pass as parameter.")
        
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id, credentials=self.credentials)
        self.dataset_ref = f"{project_id}.{dataset_id}"
        
        print(f"🚀 RetailSense AI initialized!")
        print(f"   Project: {project_id}")
        print(f"   Dataset: {dataset_id}")
        print(f"   Credentials: {credentials_path}")
        
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
    
    def setup_ml_models(self):
        """Set up BigQuery ML models for advanced analytics"""
        
        print("🤖 Setting up BigQuery ML models...")
        
        # 1. Product Recommendation Model (Matrix Factorization)
        recommendation_model_query = f"""
        CREATE OR REPLACE MODEL `{self.dataset_ref}.product_recommendation_model`
        OPTIONS(
          model_type='MATRIX_FACTORIZATION',
          user_col='user_pseudo_id',
          item_col='product_sku',
          rating_col='implicit_rating',
          l2_reg=0.1,
          num_factors=50
        ) AS
        SELECT 
          user_pseudo_id,
          product_sku,
          -- Create implicit rating based on engagement
          CASE 
            WHEN event_name = 'purchase' THEN 5.0
            WHEN event_name = 'begin_checkout' THEN 4.0
            WHEN event_name = 'add_to_cart' THEN 3.0
            WHEN event_name = 'view_item' THEN 1.0
            ELSE 0.5
          END as implicit_rating
        FROM `{self.dataset_ref}.base_sales`
        WHERE user_pseudo_id IS NOT NULL
          AND product_sku IS NOT NULL
        """
        
        try:
            job = self.client.query(recommendation_model_query)
            job.result()
            print("✅ Product recommendation model created")
        except Exception as e:
            print(f"⚠️ Recommendation model creation skipped: {str(e)[:100]}...")
        
        # 2. Revenue Forecasting Model (Time Series)
        forecasting_model_query = f"""
        CREATE OR REPLACE MODEL `{self.dataset_ref}.revenue_forecasting_model`
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
        FROM `{self.dataset_ref}.base_sales`
        WHERE event_name = 'purchase' AND revenue IS NOT NULL
        GROUP BY date
        ORDER BY date
        """
        
        try:
            job = self.client.query(forecasting_model_query)
            job.result()
            print("✅ Revenue forecasting model created")
        except Exception as e:
            print(f"⚠️ Forecasting model creation skipped: {str(e)[:100]}...")
        
        # 3. Customer Segmentation Model (K-means)
        segmentation_model_query = f"""
        CREATE OR REPLACE MODEL `{self.dataset_ref}.customer_segmentation_model`
        OPTIONS(
          model_type='KMEANS',
          num_clusters=5,
          standardize_features=TRUE
        ) AS
        SELECT 
          total_purchases,
          total_revenue,
          avg_order_value,
          days_active,
          unique_categories
        FROM (
          SELECT 
            user_pseudo_id,
            COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
            SUM(CASE WHEN event_name = 'purchase' THEN revenue END) as total_revenue,
            SAFE_DIVIDE(
              SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
              COUNT(CASE WHEN event_name = 'purchase' THEN 1 END)
            ) as avg_order_value,
            DATE_DIFF(
              MAX(PARSE_DATE('%Y%m%d', event_date)),
              MIN(PARSE_DATE('%Y%m%d', event_date)),
              DAY
            ) + 1 as days_active,
            COUNT(DISTINCT category) as unique_categories
          FROM `{self.dataset_ref}.base_sales`
          WHERE user_pseudo_id IS NOT NULL
          GROUP BY user_pseudo_id
          HAVING total_purchases > 0
        )
        """
        
        try:
            job = self.client.query(segmentation_model_query)
            job.result()
            print("✅ Customer segmentation model created")
        except Exception as e:
            print(f"⚠️ Segmentation model creation skipped: {str(e)[:100]}...")
        
        return True
    
    def generate_product_embeddings(self):
        """Generate text embeddings for products using BigQuery ML"""
        
        print("🧠 Generating product embeddings...")
        
        # Create embeddings using product descriptions
        embeddings_query = f"""
        CREATE OR REPLACE TABLE `{self.dataset_ref}.product_embeddings` AS
        SELECT 
          p.product_sku,
          p.product_name,
          p.category,
          p.brand,
          p.total_revenue,
          p.view_to_purchase_rate,
          -- Create feature-based embeddings for similarity search
          ARRAY[
            CAST(LENGTH(p.product_name) as FLOAT64) / 50.0,  -- Name length normalized
            CAST(p.avg_price as FLOAT64) / 1000.0,  -- Price normalized
            CAST(p.total_views as FLOAT64) / 10000.0,  -- Views normalized
            p.view_to_purchase_rate * 100,  -- Conversion rate as percentage
            CASE WHEN p.category = 'Apparel' THEN 1.0 ELSE 0.0 END,
            CASE WHEN p.category = 'Electronics' THEN 1.0 ELSE 0.0 END,
            CASE WHEN p.category = 'Home & Garden' THEN 1.0 ELSE 0.0 END,
            CASE WHEN p.category = 'Office' THEN 1.0 ELSE 0.0 END,
            CASE WHEN p.category = 'Drinkware' THEN 1.0 ELSE 0.0 END,
            LOG(p.total_revenue + 1) / 10.0,  -- Log revenue normalized
            CAST(p.total_purchases as FLOAT64) / 1000.0  -- Purchases normalized
          ] as embedding_vector
        FROM `{self.dataset_ref}.product_performance` p
        WHERE p.total_purchases > 0
        """
        
        try:
            job = self.client.query(embeddings_query)
            job.result()
            
            # Get embedding stats
            stats_query = f"""
            SELECT 
              COUNT(*) as products_with_embeddings,
              ARRAY_LENGTH(embedding_vector) as embedding_dimension
            FROM `{self.dataset_ref}.product_embeddings`
            LIMIT 1
            """
            
            stats = self.client.query(stats_query).to_dataframe()
            print(f"✅ Product embeddings generated")
            print(f"   📊 Products: {stats['products_with_embeddings'].iloc[0]:,}")
            print(f"   🔢 Dimensions: {stats['embedding_dimension'].iloc[0]}")
            
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
        
        return True
    
    def create_similarity_search_function(self):
        """Create UDF for product similarity search"""
        
        print("🔍 Creating similarity search function...")
        
        similarity_function_query = f"""
        CREATE OR REPLACE FUNCTION `{self.dataset_ref}.cosine_similarity`(
          vector1 ARRAY<FLOAT64>, 
          vector2 ARRAY<FLOAT64>
        )
        RETURNS FLOAT64
        LANGUAGE SQL
        AS (
          (
            SELECT SUM(v1 * v2)
            FROM UNNEST(vector1) AS v1 WITH OFFSET pos1
            JOIN UNNEST(vector2) AS v2 WITH OFFSET pos2
            ON pos1 = pos2
          ) / (
            SQRT(
              (SELECT SUM(v1 * v1) FROM UNNEST(vector1) AS v1)
            ) * SQRT(
              (SELECT SUM(v2 * v2) FROM UNNEST(vector2) AS v2)
            )
          )
        );
        
        CREATE OR REPLACE FUNCTION `{self.dataset_ref}.find_similar_products`(
          target_sku STRING,
          top_k INT64
        )
        RETURNS ARRAY<STRUCT<
          product_sku STRING,
          similarity_score FLOAT64,
          product_name STRING,
          category STRING,
          total_revenue FLOAT64
        >>
        LANGUAGE SQL
        AS (
          WITH target_embedding AS (
            SELECT embedding_vector
            FROM `{self.dataset_ref}.product_embeddings`
            WHERE product_sku = target_sku
          ),
          similarities AS (
            SELECT 
              p.product_sku,
              p.product_name,
              p.category,
              p.total_revenue,
              `{self.dataset_ref}.cosine_similarity`(p.embedding_vector, t.embedding_vector) as similarity_score
            FROM `{self.dataset_ref}.product_embeddings` p
            CROSS JOIN target_embedding t
            WHERE p.product_sku != target_sku
            ORDER BY similarity_score DESC
            LIMIT top_k
          )
          
          SELECT ARRAY_AGG(
            STRUCT(
              product_sku,
              similarity_score,
              product_name,
              category,
              total_revenue
            )
          )
          FROM similarities
        );
        """
        
        try:
            job = self.client.query(similarity_function_query)
            job.result()
            print("✅ Similarity search functions created")
        except Exception as e:
            print(f"❌ Error creating similarity functions: {e}")
        
        return True
    
    def get_product_recommendations(self, user_id, top_k=10):
        """Get product recommendations for a user"""
        
        query = f"""
        SELECT 
          predicted_product_sku as product_sku,
          predicted_rating,
          p.product_name,
          p.category,
          p.total_revenue
        FROM ML.RECOMMEND(
          MODEL `{self.dataset_ref}.product_recommendation_model`,
          STRUCT('{user_id}' as user_pseudo_id)
        ) r
        JOIN `{self.dataset_ref}.product_performance` p
        ON r.predicted_product_sku = p.product_sku
        ORDER BY predicted_rating DESC
        LIMIT {top_k}
        """
        
        try:
            return self.client.query(query).to_dataframe()
        except Exception as e:
            print(f"❌ Error getting recommendations: {e}")
            return pd.DataFrame()
    
    def get_revenue_forecast(self, forecast_days=30):
        """Get revenue forecast for specified days"""
        
        query = f"""
        SELECT 
          forecast_timestamp as date,
          forecast_value as predicted_revenue,
          prediction_interval_lower_bound as lower_bound,
          prediction_interval_upper_bound as upper_bound
        FROM ML.FORECAST(
          MODEL `{self.dataset_ref}.revenue_forecasting_model`,
          STRUCT({forecast_days} as horizon)
        )
        ORDER BY forecast_timestamp
        """
        
        try:
            return self.client.query(query).to_dataframe()
        except Exception as e:
            print(f"❌ Error getting forecast: {e}")
            return pd.DataFrame()
    
    def get_customer_segments(self):
        """Get customer segmentation analysis"""
        
        query = f"""
        SELECT 
          CENTROID_ID as segment_id,
          COUNT(*) as customer_count,
          AVG(total_purchases) as avg_purchases,
          AVG(total_revenue) as avg_revenue,
          AVG(avg_order_value) as avg_order_value,
          AVG(days_active) as avg_days_active
        FROM ML.PREDICT(
          MODEL `{self.dataset_ref}.customer_segmentation_model`,
          (
            SELECT 
              user_pseudo_id,
              COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as total_purchases,
              SUM(CASE WHEN event_name = 'purchase' THEN revenue END) as total_revenue,
              SAFE_DIVIDE(
                SUM(CASE WHEN event_name = 'purchase' THEN revenue END),
                COUNT(CASE WHEN event_name = 'purchase' THEN 1 END)
              ) as avg_order_value,
              DATE_DIFF(
                MAX(PARSE_DATE('%Y%m%d', event_date)),
                MIN(PARSE_DATE('%Y%m%d', event_date)),
                DAY
              ) + 1 as days_active,
              COUNT(DISTINCT category) as unique_categories
            FROM `{self.dataset_ref}.base_sales`
            WHERE user_pseudo_id IS NOT NULL
            GROUP BY user_pseudo_id
            HAVING total_purchases > 0
          )
        )
        GROUP BY CENTROID_ID
        ORDER BY segment_id
        """
        
        try:
            return self.client.query(query).to_dataframe()
        except Exception as e:
            print(f"❌ Error getting customer segments: {e}")
            return pd.DataFrame()
    
    def find_similar_products(self, target_sku, top_k=5):
        """Find similar products using embeddings"""
        
        query = f"""
        SELECT *
        FROM UNNEST(`{self.dataset_ref}.find_similar_products`('{target_sku}', {top_k}))
        """
        
        try:
            return self.client.query(query).to_dataframe()
        except Exception as e:
            print(f"❌ Error finding similar products: {e}")
            return pd.DataFrame()
    
    def get_advanced_analytics(self):
        """Get comprehensive analytics dashboard data"""
        
        print("📊 Generating advanced analytics...")
        
        # Product performance with trends
        performance_query = f"""
        WITH daily_metrics AS (
          SELECT 
            product_sku,
            PARSE_DATE('%Y%m%d', event_date) as date,
            COUNT(CASE WHEN event_name = 'view_item' THEN 1 END) as daily_views,
            COUNT(CASE WHEN event_name = 'purchase' THEN 1 END) as daily_purchases,
            SUM(CASE WHEN event_name = 'purchase' THEN revenue END) as daily_revenue
          FROM `{self.dataset_ref}.base_sales`
          GROUP BY product_sku, date
        ),
        product_trends AS (
          SELECT 
            product_sku,
            AVG(daily_views) as avg_daily_views,
            AVG(daily_purchases) as avg_daily_purchases,
            AVG(daily_revenue) as avg_daily_revenue,
            -- Calculate trend (positive = growing, negative = declining)
            CORR(UNIX_DATE(date), daily_revenue) as revenue_trend
          FROM daily_metrics
          GROUP BY product_sku
        )
        SELECT 
          p.*,
          t.avg_daily_views,
          t.avg_daily_purchases,
          t.avg_daily_revenue,
          t.revenue_trend,
          CASE 
            WHEN t.revenue_trend > 0.1 THEN 'Growing'
            WHEN t.revenue_trend < -0.1 THEN 'Declining'
            ELSE 'Stable'
          END as trend_status
        FROM `{self.dataset_ref}.product_performance` p
        LEFT JOIN product_trends t ON p.product_sku = t.product_sku
        ORDER BY p.total_revenue DESC
        """
        
        try:
            performance_data = self.client.query(performance_query).to_dataframe()
            print(f"✅ Advanced performance data: {len(performance_data)} products")
            return performance_data
        except Exception as e:
            print(f"❌ Error getting advanced analytics: {e}")
            return self.get_performance_data()  # Fallback to basic data
    
    def create_comprehensive_pipeline(self, start_date="20210101", end_date="20210331"):
        """Run the complete BigQuery ML pipeline"""
        
        print("🚀 RETAILSENSE AI - COMPREHENSIVE BIGQUERY PIPELINE")
        print("=" * 60)
        
        try:
            # Step 1: Environment setup
            print("\n🔧 Step 1: Setting up environment...")
            self.setup_environment()
            
            # Step 2: Load data
            print("\n📥 Step 2: Loading GA4 data...")
            self.load_ga4_data(start_date, end_date)
            
            # Step 3: Create performance metrics
            print("\n📊 Step 3: Creating performance metrics...")
            self.create_product_performance_table()
            
            # Step 4: Set up ML models
            print("\n🤖 Step 4: Setting up ML models...")
            self.setup_ml_models()
            
            # Step 5: Generate embeddings
            print("\n🧠 Step 5: Generating product embeddings...")
            self.generate_product_embeddings()
            
            # Step 6: Create similarity functions
            print("\n🔍 Step 6: Creating similarity search...")
            self.create_similarity_search_function()
            
            # Step 7: Get comprehensive analytics
            print("\n📈 Step 7: Generating advanced analytics...")
            analytics_data = self.get_advanced_analytics()
            
            print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("✅ All BigQuery ML models and functions are ready")
            print("✅ Advanced analytics data generated")
            print("✅ Ready for production AI-powered insights")
            
            return analytics_data
            
        except Exception as e:
            print(f"\n❌ Pipeline error: {e}")
            print("💡 Check your BigQuery permissions and project setup")
            return None