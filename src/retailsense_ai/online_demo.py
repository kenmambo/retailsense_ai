#!/usr/bin/env python3
"""
RetailSense AI - Online Demo with BigQuery ML Integration

This module demonstrates the full online capabilities of RetailSense AI
using real BigQuery data and ML models.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from .core import RetailSenseAI

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

class RetailSenseAIOnlineDemo:
    """
    RetailSense AI Online Demo - BigQuery ML Integration
    
    Demonstrates advanced AI capabilities using real e-commerce data
    from Google Analytics 4 via BigQuery.
    """
    
    def __init__(self, project_id=None, credentials_path=None):
        """Initialize the online demo with BigQuery connection"""
        
        print("🌐 RetailSense AI Online Demo initialized!")
        print("   Mode: BigQuery ML Integration")
        print("   Data: Real GA4 E-commerce Dataset")
        
        # Initialize RetailSense AI with BigQuery
        try:
            self.retail_ai = RetailSenseAI(
                project_id=project_id,
                credentials_path=credentials_path
            )
            self.connected = True
            print("✅ BigQuery connection established")
        except Exception as e:
            print(f"❌ BigQuery connection failed: {e}")
            self.connected = False
            raise
    
    def run_comprehensive_setup(self, start_date="20210101", end_date="20210331"):
        """Run the complete BigQuery ML setup pipeline"""
        
        if not self.connected:
            raise RuntimeError("BigQuery connection not established")
        
        print("\n🚀 RUNNING COMPREHENSIVE BIGQUERY ML SETUP")
        print("=" * 60)
        
        # Run the complete pipeline
        self.analytics_data = self.retail_ai.create_comprehensive_pipeline(
            start_date=start_date, 
            end_date=end_date
        )
        
        if self.analytics_data is not None:
            print(f"\n📊 Analytics data loaded: {len(self.analytics_data)} products")
            return True
        else:
            print("\n❌ Setup failed")
            return False
    
    def demonstrate_ml_features(self, output_dir="outputs"):
        """Demonstrate all ML features with real data"""
        
        if not hasattr(self, 'analytics_data') or self.analytics_data is None:
            print("⚠️ Please run setup first")
            return None
        
        print("\n🤖 DEMONSTRATING ML FEATURES")
        print("=" * 50)
        
        results = {}
        
        # 1. Product Recommendations
        print("\n1️⃣ Product Recommendations...")
        try:
            # Get a sample user for recommendations
            sample_user_query = f"""
            SELECT user_pseudo_id, COUNT(*) as activity_count
            FROM `{self.retail_ai.dataset_ref}.base_sales`
            WHERE user_pseudo_id IS NOT NULL
            GROUP BY user_pseudo_id
            ORDER BY activity_count DESC
            LIMIT 5
            """
            sample_users = self.retail_ai.client.query(sample_user_query).to_dataframe()
            
            if not sample_users.empty:
                sample_user = sample_users.iloc[0]['user_pseudo_id']
                recommendations = self.retail_ai.get_product_recommendations(sample_user, top_k=10)
                
                if not recommendations.empty:
                    print(f"   ✅ Generated {len(recommendations)} recommendations for user {sample_user}")
                    print("   🎯 Top 3 Recommendations:")
                    for i, rec in recommendations.head(3).iterrows():
                        print(f"     {i+1}. {rec['product_name']} (Score: {rec['predicted_rating']:.3f})")
                    results['recommendations'] = recommendations
                else:
                    print("   ⚠️ No recommendations generated")
            else:
                print("   ⚠️ No users found for recommendations")
                
        except Exception as e:
            print(f"   ❌ Recommendation error: {str(e)[:100]}...")
        
        # 2. Revenue Forecasting
        print("\n2️⃣ Revenue Forecasting...")
        try:
            forecast = self.retail_ai.get_revenue_forecast(forecast_days=30)
            
            if not forecast.empty:
                print(f"   ✅ Generated {len(forecast)} days forecast")
                total_predicted = forecast['predicted_revenue'].sum()
                print(f"   💰 Predicted 30-day revenue: ${total_predicted:,.2f}")
                results['forecast'] = forecast
            else:
                print("   ⚠️ No forecast generated")
                
        except Exception as e:
            print(f"   ❌ Forecasting error: {str(e)[:100]}...")
        
        # 3. Customer Segmentation
        print("\n3️⃣ Customer Segmentation...")
        try:
            segments = self.retail_ai.get_customer_segments()
            
            if not segments.empty:
                print(f"   ✅ Identified {len(segments)} customer segments")
                for _, segment in segments.iterrows():
                    print(f"     Segment {int(segment['segment_id'])}: {int(segment['customer_count'])} customers, "
                          f"${segment['avg_revenue']:.2f} avg revenue")
                results['segments'] = segments
            else:
                print("   ⚠️ No segments generated")
                
        except Exception as e:
            print(f"   ❌ Segmentation error: {str(e)[:100]}...")
        
        # 4. Product Similarity Search
        print("\n4️⃣ Product Similarity Search...")
        try:
            # Get a sample product for similarity search
            if len(self.analytics_data) > 0:
                sample_product = self.analytics_data.iloc[0]['product_sku']
                similar_products = self.retail_ai.find_similar_products(sample_product, top_k=5)
                
                if not similar_products.empty:
                    print(f"   ✅ Found {len(similar_products)} similar products")
                    print(f"   🎯 Target: {self.analytics_data.iloc[0]['product_name']}")
                    print("   🔍 Similar products:")
                    for _, similar in similar_products.iterrows():
                        print(f"     • {similar['product_name']} (Similarity: {similar['similarity_score']:.3f})")
                    results['similar_products'] = similar_products
                else:
                    print("   ⚠️ No similar products found")
            else:
                print("   ⚠️ No products available for similarity search")
                
        except Exception as e:
            print(f"   ❌ Similarity search error: {str(e)[:100]}...")
        
        return results


def main():
    """Main function for running the online demo"""
    
    try:
        # Initialize online demo
        demo = RetailSenseAIOnlineDemo()
        
        # Run setup
        setup_success = demo.run_comprehensive_setup()
        
        if setup_success:
            # Demonstrate ML features
            ml_results = demo.demonstrate_ml_features()
            print("\n🌟 RetailSense AI BigQuery ML Demo - SUCCESS!")
        else:
            print("\n❌ Demo failed - check the error messages above")
            
    except Exception as e:
        print(f"\n❌ Failed to initialize online demo: {e}")
        print("💡 Ensure BigQuery credentials are properly configured")


if __name__ == "__main__":
    main()