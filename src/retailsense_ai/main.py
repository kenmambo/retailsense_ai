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
from retailsense_ai.online_demo import RetailSenseAIOnlineDemo


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
        # Initialize RetailSense AI with environment variable support  
        retail_ai = RetailSenseAI(
            project_id=args.project_id,
            credentials_path=args.credentials
        )
        
        # Run comprehensive BigQuery ML pipeline
        print("🚀 Running comprehensive BigQuery ML pipeline...")
        analytics_data = retail_ai.create_comprehensive_pipeline()
        
        if analytics_data is not None:
            # Get additional analysis results
            print("📈 Retrieving analysis results...")
            performance_data = retail_ai.get_performance_data()
            category_data = retail_ai.get_category_analysis()
            
            print("\n✅ BIGQUERY ANALYSIS COMPLETED!")
            print("=" * 60)
            print(f"📊 Products analyzed: {len(performance_data):,}")
            print(f"🏷️  Categories: {len(category_data)}")
            
            if not performance_data.empty:
                total_revenue = performance_data['total_revenue'].sum()
                avg_conversion = performance_data['view_to_purchase_rate'].mean() * 100
                print(f"💰 Total revenue: ${total_revenue:,.2f}")
                print(f"📈 Avg conversion: {avg_conversion:.2f}%")
        
        else:
            print("❌ BigQuery analysis failed to complete")
            
    except Exception as e:
        print(f"❌ BigQuery analysis error: {e}")
        print("💡 Check credentials, project permissions, and network connectivity")


if __name__ == "__main__":
    main()