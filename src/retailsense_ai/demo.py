"""
Demo module for RetailSense AI offline functionality
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

class RetailSenseAIDemo:
    """
    RetailSense AI Demo - Offline version showing core functionality
    """
    
    def __init__(self):
        print("🚀 RetailSense AI Demo initialized!")
        print("   Mode: Offline demonstration")
        print("   Focus: Core e-commerce intelligence features")
        
    def create_sample_data(self, n_products=50):
        """Create sample e-commerce data for demonstration"""
        
        print(f"\n📊 Creating sample e-commerce data with {n_products} products...")
        
        # Generate sample products
        categories = ['Electronics', 'Audio', 'Accessories', 'Wearables', 'Computing']
        brands = ['TechCorp', 'AudioPro', 'SmartDevices', 'EliteGear', 'NextGen']
        
        np.random.seed(42)  # For reproducible results
        
        products = []
        for i in range(n_products):
            product = {
                'product_sku': f'PROD_{i+1:03d}',
                'product_name': self._generate_product_name(i),
                'category': np.random.choice(categories),
                'brand': np.random.choice(brands),
                'price': round(np.random.uniform(20, 500), 2),
                'total_views': np.random.randint(100, 5000),
                'total_cart_adds': 0,
                'total_purchases': 0,
                'total_revenue': 0,
                'unique_users': 0
            }
            
            # Calculate realistic conversion rates
            conversion_rate = np.random.uniform(0.02, 0.15)
            cart_rate = np.random.uniform(0.1, 0.4)
            
            product['total_cart_adds'] = int(product['total_views'] * cart_rate)
            product['total_purchases'] = int(product['total_cart_adds'] * conversion_rate)
            product['total_revenue'] = round(product['total_purchases'] * product['price'], 2)
            product['unique_users'] = int(product['total_views'] * np.random.uniform(0.3, 0.8))
            
            # Calculate metrics
            product['view_to_purchase_rate'] = product['total_purchases'] / product['total_views'] if product['total_views'] > 0 else 0
            product['cart_to_purchase_rate'] = product['total_purchases'] / product['total_cart_adds'] if product['total_cart_adds'] > 0 else 0
            product['revenue_per_view'] = product['total_revenue'] / product['total_views'] if product['total_views'] > 0 else 0
            
            products.append(product)
        
        self.products_df = pd.DataFrame(products)
        
        print(f"✅ Generated {len(products)} sample products")
        print(f"   💰 Total revenue: ${self.products_df['total_revenue'].sum():,.2f}")
        print(f"   📈 Avg conversion rate: {self.products_df['view_to_purchase_rate'].mean()*100:.2f}%")
        
        return self.products_df
    
    def _generate_product_name(self, index):
        """Generate realistic product names"""
        prefixes = ['Premium', 'Pro', 'Smart', 'Wireless', 'Digital', 'Ultra', 'Advanced', 'Professional']
        products = ['Headphones', 'Speaker', 'Mouse', 'Keyboard', 'Monitor', 'Watch', 'Camera', 'Charger', 'Cable', 'Stand']
        suffixes = ['2024', 'X', 'Plus', 'Max', 'Elite', 'Pro', 'HD', '4K']
        
        prefix = np.random.choice(prefixes)
        product = np.random.choice(products)
        suffix = np.random.choice(suffixes) if np.random.random() > 0.5 else ''
        
        return f"{prefix} {product} {suffix}".strip()
    
    def analyze_performance(self):
        """Analyze product performance metrics"""
        
        print("\n🔍 Analyzing product performance...")
        
        # Top performers by revenue
        top_revenue = self.products_df.nlargest(5, 'total_revenue')
        print("\n💰 Top 5 Products by Revenue:")
        for _, product in top_revenue.iterrows():
            print(f"   {product['product_name']}: ${product['total_revenue']:,.2f}")
        
        # Best conversion rates
        top_conversion = self.products_df.nlargest(5, 'view_to_purchase_rate')
        print("\n📈 Top 5 Products by Conversion Rate:")
        for _, product in top_conversion.iterrows():
            print(f"   {product['product_name']}: {product['view_to_purchase_rate']*100:.2f}%")
        
        # Category analysis
        category_analysis = self.products_df.groupby('category').agg({
            'total_revenue': 'sum',
            'total_views': 'sum',
            'view_to_purchase_rate': 'mean'
        }).round(2)
        
        print("\n🏷️  Category Performance:")
        for category, data in category_analysis.iterrows():
            print(f"   {category}: ${data['total_revenue']:,.2f} revenue, {data['view_to_purchase_rate']*100:.2f}% conversion")
        
        return top_revenue, category_analysis
    
    def create_visualizations(self, output_dir="outputs"):
        """Create performance visualizations"""
        
        print(f"\n📊 Creating visualizations in {output_dir}/...")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('RetailSense AI - E-commerce Performance Dashboard', fontsize=16)
        
        # 1. Revenue by Category
        category_revenue = self.products_df.groupby('category')['total_revenue'].sum().sort_values(ascending=True)
        axes[0, 0].barh(category_revenue.index, category_revenue.values)
        axes[0, 0].set_title('Revenue by Category')
        axes[0, 0].set_xlabel('Revenue ($)')
        
        # 2. Conversion Rate Distribution
        axes[0, 1].hist(self.products_df['view_to_purchase_rate'] * 100, bins=15, edgecolor='black', alpha=0.7)
        axes[0, 1].set_title('Conversion Rate Distribution')
        axes[0, 1].set_xlabel('Conversion Rate (%)')
        axes[0, 1].set_ylabel('Number of Products')
        
        # 3. Price vs Revenue Scatter
        scatter = axes[1, 0].scatter(self.products_df['price'], 
                                   self.products_df['total_revenue'], 
                                   c=self.products_df['view_to_purchase_rate'], 
                                   cmap='viridis', alpha=0.6)
        axes[1, 0].set_title('Price vs Revenue (colored by conversion rate)')
        axes[1, 0].set_xlabel('Price ($)')
        axes[1, 0].set_ylabel('Revenue ($)')
        plt.colorbar(scatter, ax=axes[1, 0], label='Conversion Rate')
        
        # 4. Brand Performance
        brand_performance = self.products_df.groupby('brand').agg({
            'total_revenue': 'sum',
            'view_to_purchase_rate': 'mean'
        })
        axes[1, 1].scatter(brand_performance['view_to_purchase_rate'] * 100, 
                          brand_performance['total_revenue'])
        axes[1, 1].set_title('Brand Performance')
        axes[1, 1].set_xlabel('Avg Conversion Rate (%)')
        axes[1, 1].set_ylabel('Total Revenue ($)')
        
        # Add brand labels
        for brand, data in brand_performance.iterrows():
            axes[1, 1].annotate(brand, 
                              (data['view_to_purchase_rate'] * 100, data['total_revenue']),
                              xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.tight_layout()
        dashboard_path = os.path.join(output_dir, 'retailsense_dashboard.png')
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
        print(f"✅ Dashboard saved as '{dashboard_path}'")
        plt.close()
        
        return dashboard_path
    
    def demo_similarity_search(self):
        """Demonstrate product similarity search (simplified version)"""
        
        print("\n🧠 Demonstrating product similarity search...")
        
        # Simple similarity based on category, price range, and performance metrics
        def find_similar_products(target_sku, top_k=3):
            target = self.products_df[self.products_df['product_sku'] == target_sku].iloc[0]
            
            # Calculate similarity scores
            similarities = []
            for _, product in self.products_df.iterrows():
                if product['product_sku'] == target_sku:
                    continue
                
                # Simple similarity calculation
                category_match = 1.0 if product['category'] == target['category'] else 0.3
                brand_match = 1.0 if product['brand'] == target['brand'] else 0.5
                price_similarity = 1.0 - abs(product['price'] - target['price']) / max(product['price'], target['price'])
                performance_similarity = 1.0 - abs(product['view_to_purchase_rate'] - target['view_to_purchase_rate'])
                
                overall_similarity = (category_match * 0.4 + brand_match * 0.2 + 
                                    price_similarity * 0.2 + performance_similarity * 0.2)
                
                similarities.append({
                    'product_sku': product['product_sku'],
                    'product_name': product['product_name'],
                    'category': product['category'],
                    'similarity_score': overall_similarity,
                    'price': product['price'],
                    'conversion_rate': product['view_to_purchase_rate']
                })
            
            # Sort by similarity and return top k
            similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
            return similarities[:top_k]
        
        # Demo with a random product
        target_product = self.products_df.sample(1).iloc[0]
        similar_products = find_similar_products(target_product['product_sku'])
        
        print(f"\n📍 Target Product: {target_product['product_name']}")
        print(f"   Category: {target_product['category']}")
        print(f"   Price: ${target_product['price']:.2f}")
        print(f"   Conversion Rate: {target_product['view_to_purchase_rate']*100:.2f}%")
        
        print("\n🎯 Most Similar Products:")
        for i, product in enumerate(similar_products, 1):
            print(f"   {i}. {product['product_name']}")
            print(f"      Similarity: {product['similarity_score']:.3f}")
            print(f"      Price: ${product['price']:.2f}")
            print(f"      Conversion: {product['conversion_rate']*100:.2f}%")
            print()
        
        return target_product, similar_products
    
    def generate_insights_report(self, output_dir="outputs"):
        """Generate executive insights report"""
        
        print(f"\n📋 Generating Executive Insights Report in {output_dir}/...")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate key metrics
        total_revenue = self.products_df['total_revenue'].sum()
        avg_conversion = self.products_df['view_to_purchase_rate'].mean()
        top_category = self.products_df.groupby('category')['total_revenue'].sum().idxmax()
        best_performer = self.products_df.loc[self.products_df['total_revenue'].idxmax()]
        
        insights = {
            "executive_summary": {
                "total_products": len(self.products_df),
                "total_revenue": f"${total_revenue:,.2f}",
                "average_conversion_rate": f"{avg_conversion*100:.2f}%",
                "top_performing_category": top_category,
                "best_product": best_performer['product_name']
            },
            "key_findings": [
                f"💰 Total portfolio revenue: ${total_revenue:,.2f}",
                f"📈 Average conversion rate: {avg_conversion*100:.2f}%",
                f"🏆 Top category: {top_category}",
                f"⭐ Best performer: {best_performer['product_name']} (${best_performer['total_revenue']:,.2f})",
                f"📊 Product portfolio spans {len(self.products_df['category'].unique())} categories"
            ],
            "recommendations": [
                "🎯 Focus marketing spend on high-conversion products",
                "💡 Investigate pricing strategies for underperforming high-traffic items", 
                "🔄 Expand successful product categories",
                "📱 Implement similar product recommendation system",
                "⚡ Optimize checkout flow to improve cart-to-purchase rates"
            ]
        }
        
        # Save report
        report_path = os.path.join(output_dir, 'retailsense_insights_report.json')
        with open(report_path, 'w') as f:
            json.dump(insights, f, indent=2)
        
        print("\n📊 RETAILSENSE AI INSIGHTS REPORT")
        print("=" * 50)
        
        print(f"\n📈 EXECUTIVE SUMMARY:")
        for key, value in insights["executive_summary"].items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🔍 KEY FINDINGS:")
        for finding in insights["key_findings"]:
            print(f"   {finding}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in insights["recommendations"]:
            print(f"   {rec}")
        
        print(f"\n✅ Report saved as '{report_path}'")
        
        return insights, report_path
    
    def run_full_demo(self, output_dir="outputs"):
        """Run the complete demo pipeline"""
        
        print("🎯 RETAILSENSE AI - COMPLETE DEMO PIPELINE")
        print("=" * 60)
        
        try:
            # Create sample data
            products_df = self.create_sample_data()
            
            # Run analysis
            top_products, category_analysis = self.analyze_performance()
            
            # Create visualizations
            dashboard_path = self.create_visualizations(output_dir)
            
            # Demo AI features
            target_product, similar_products = self.demo_similarity_search()
            
            # Generate insights report
            insights, report_path = self.generate_insights_report(output_dir)
            
            print("\n🎉 DEMO COMPLETE!")
            print("=" * 60)
            print("✅ Core RetailSense AI functionality demonstrated")
            print(f"📊 Dashboard visualization: {dashboard_path}")
            print(f"📋 Executive insights report: {report_path}")
            print("💡 Ready for production deployment with Google Cloud BigQuery")
            
            return {
                'products_df': products_df,
                'top_products': top_products,
                'category_analysis': category_analysis,
                'dashboard_path': dashboard_path,
                'insights': insights,
                'report_path': report_path,
                'target_product': target_product,
                'similar_products': similar_products
            }
            
        except Exception as e:
            print(f"\n❌ Error during demo: {e}")
            import traceback
            traceback.print_exc()
            return None