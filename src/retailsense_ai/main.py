#!/usr/bin/env python3
"""
RetailSense AI - Main execution script
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path for development
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from retailsense_ai import RetailSenseAI, RetailSenseAIDemo


def main():
    """Main entry point for RetailSense AI"""
    
    parser = argparse.ArgumentParser(
        description="RetailSense AI - Multimodal E-commerce Intelligence Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m retailsense_ai.main --demo                    # Run offline demo
  python -m retailsense_ai.main --bigquery               # Run BigQuery analysis
  python -m retailsense_ai.main --demo --output-dir custom_outputs
        """
    )
    
    parser.add_argument(
        "--demo", 
        action="store_true", 
        help="Run offline demonstration"
    )
    
    parser.add_argument(
        "--bigquery", 
        action="store_true", 
        help="Run BigQuery cloud analysis"
    )
    
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="outputs",
        help="Output directory for generated files (default: outputs)"
    )
    
    parser.add_argument(
        "--credentials", 
        type=str, 
        help="Path to Google Cloud credentials JSON file"
    )
    
    parser.add_argument(
        "--project-id", 
        type=str, 
        help="Google Cloud project ID"
    )
    
    parser.add_argument(
        "--n-products", 
        type=int, 
        default=50,
        help="Number of sample products for demo (default: 50)"
    )
    
    args = parser.parse_args()
    
    # Ensure at least one mode is selected
    if not args.demo and not args.bigquery:
        print("🎯 RetailSense AI - Multimodal E-commerce Intelligence Engine")
        print("=" * 60)
        print("Please specify a mode:")
        print("  --demo      Run offline demonstration")
        print("  --bigquery  Run BigQuery cloud analysis")
        print("\nFor help: python -m retailsense_ai.main --help")
        return
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.demo:
        run_demo(args)
    
    if args.bigquery:
        run_bigquery_analysis(args)


def run_demo(args):
    """Run the offline demonstration"""
    
    print("🎯 RETAILSENSE AI - OFFLINE DEMONSTRATION")
    print("=" * 60)
    print("Running comprehensive e-commerce intelligence demo...")
    print()
    
    try:
        # Initialize demo
        demo = RetailSenseAIDemo()
        
        # Run complete demo pipeline
        results = demo.run_full_demo(output_dir=args.output_dir)
        
        if results:
            print("\n🎉 DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"📊 Dashboard: {results['dashboard_path']}")
            print(f"📋 Report: {results['report_path']}")
            print(f"📁 Output directory: {args.output_dir}")
            print("\n💡 Next steps:")
            print("   - Review the generated dashboard and insights")
            print("   - Set up BigQuery for cloud-scale analysis")
            print("   - Explore the Jupyter notebook for interactive analysis")
        else:
            print("❌ Demo failed to complete")
            
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 Check the error details above and try again")


def run_bigquery_analysis(args):
    """Run BigQuery cloud analysis"""
    
    print("☁️ RETAILSENSE AI - BIGQUERY ANALYSIS")
    print("=" * 60)
    print("Connecting to Google Cloud BigQuery...")
    print()
    
    try:
        # Determine credentials path
        credentials_path = args.credentials
        if not credentials_path:
            # Look for credentials in default locations
            default_paths = [
                "credentials/retailsense-ai-ceb777b5822d.json",
                "credentials/service-account.json",
                os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            ]
            
            for path in default_paths:
                if path and os.path.exists(path):
                    credentials_path = path
                    break
        
        if not credentials_path or not os.path.exists(credentials_path):
            print("❌ BigQuery credentials not found!")
            print("💡 Please provide credentials using one of these methods:")
            print("   1. Use --credentials /path/to/service-account.json")
            print("   2. Place credentials in credentials/retailsense-ai-ceb777b5822d.json")
            print("   3. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
            return
        
        # Initialize RetailSense AI
        retail_ai = RetailSenseAI(
            project_id=args.project_id,
            credentials_path=credentials_path
        )
        
        # Run BigQuery analysis pipeline
        print("🔧 Setting up BigQuery environment...")
        retail_ai.setup_environment()
        
        print("📥 Loading GA4 sample data...")
        retail_ai.load_ga4_data()
        
        print("📊 Creating product performance analysis...")
        retail_ai.create_product_performance_table()
        
        # Get and display results
        print("📈 Retrieving analysis results...")
        performance_data = retail_ai.get_performance_data()
        category_data = retail_ai.get_category_analysis()
        
        print("\n✅ BIGQUERY ANALYSIS COMPLETED!")
        print("=" * 60)
        print(f"📊 Products analyzed: {len(performance_data):,}")
        print(f"🏷️  Categories: {len(category_data)}")
        print(f"💰 Total revenue: ${performance_data['total_revenue'].sum():,.2f}")
        print(f"📈 Avg conversion: {performance_data['view_to_purchase_rate'].mean()*100:.2f}%")
        
        # Save results to output directory
        performance_path = os.path.join(args.output_dir, "bigquery_performance_data.csv")
        category_path = os.path.join(args.output_dir, "bigquery_category_analysis.csv")
        
        performance_data.to_csv(performance_path, index=False)
        category_data.to_csv(category_path, index=False)
        
        print(f"\n📄 Results saved:")
        print(f"   - Performance data: {performance_path}")
        print(f"   - Category analysis: {category_path}")
        
    except Exception as e:
        print(f"❌ BigQuery analysis error: {e}")
        print("💡 Check credentials, project permissions, and network connectivity")


if __name__ == "__main__":
    main()