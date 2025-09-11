#!/usr/bin/env python3
"""
Test Production RetailSense AI with Real BigQuery Data
"""

import os
import sys
sys.path.insert(0, 'src')

from retailsense_ai import RetailSenseAI

def main():
    print('🚀 Testing Production RetailSense AI with Real BigQuery Data')
    print('=' * 60)
    
    os.makedirs('production_output', exist_ok=True)
    
    try:
        # Initialize with production settings
        ai = RetailSenseAI()
        
        # Get basic analytics
        print('📊 Getting product performance data...')
        performance_data = ai.get_performance_data()
        print(f'✅ Retrieved {len(performance_data)} product records')
        
        print('🏷️ Getting category analysis...')
        category_data = ai.get_category_analysis()
        print(f'✅ Retrieved {len(category_data)} categories')
        
        # Show production stats
        if not performance_data.empty:
            total_revenue = performance_data['total_revenue'].sum()
            total_views = performance_data['total_views'].sum()
            total_purchases = performance_data['total_purchases'].sum()
            avg_price = performance_data['avg_price'].mean()
            
            print()
            print('📈 PRODUCTION ANALYTICS SUMMARY')
            print(f'💰 Total Revenue: ${total_revenue:,.2f}')
            print(f'👀 Total Views: {total_views:,}')
            print(f'🛒 Total Purchases: {total_purchases:,}')
            print(f'💵 Average Price: ${avg_price:.2f}')
            print(f'📊 Conversion Rate: {(total_purchases/total_views)*100:.2f}%')
            
            # Show top performers
            print()
            print('🏆 TOP 5 PRODUCTS BY REVENUE:')
            top_products = performance_data.nlargest(5, 'total_revenue')
            for i, (_, product) in enumerate(top_products.iterrows(), 1):
                print(f'  {i}. {product["product_name"]}: ${product["total_revenue"]:,.2f}')
            
            print()
            print('🏆 TOP 5 CATEGORIES BY REVENUE:')
            top_categories = category_data.nlargest(5, 'category_revenue')
            for i, (_, cat) in enumerate(top_categories.iterrows(), 1):
                print(f'  {i}. {cat["category"]}: ${cat["category_revenue"]:,.2f}')
            
            # Save results
            performance_data.to_csv('production_output/bigquery_performance_data.csv', index=False)
            category_data.to_csv('production_output/bigquery_category_analysis.csv', index=False)
            print()
            print('✅ Production data saved to production_output/')
            
            # Show sample of the real data
            print()
            print('📋 SAMPLE PRODUCT DATA (Real BigQuery Data):')
            print(performance_data[['product_name', 'category', 'total_revenue', 'total_views', 'total_purchases']].head(3).to_string(index=False))
            
        else:
            print('❌ No performance data available')
        
        print()
        print('🎉 Production test completed successfully!')
        print('🔗 BigQuery tables created in your project: retailsense-ai.retail_intelligence')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()