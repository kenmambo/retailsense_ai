#!/usr/bin/env python3
"""
RetailSense AI - Production Setup Helper

This script helps you set up the production environment for RetailSense AI
with real Google Cloud credentials and BigQuery access.
"""

import os
import json
import sys
from pathlib import Path

def check_credentials():
    """Check if valid credentials exist"""
    credentials_dir = Path("credentials")
    env_file = Path(".env")
    
    print("🔍 CHECKING PRODUCTION SETUP STATUS")
    print("=" * 50)
    
    # Check credentials directory
    if not credentials_dir.exists():
        print("❌ Credentials directory not found")
        return False
    
    # Check for credential files
    cred_files = list(credentials_dir.glob("*.json"))
    valid_creds = []
    
    for cred_file in cred_files:
        if cred_file.name == "service-account-template.json":
            continue
            
        try:
            with open(cred_file, 'r') as f:
                cred_data = json.load(f)
                if all(key in cred_data for key in ['type', 'project_id', 'private_key', 'client_email']):
                    valid_creds.append((cred_file, cred_data))
                    print(f"✅ Valid credentials found: {cred_file.name}")
                    print(f"   Project ID: {cred_data.get('project_id')}")
                    print(f"   Service Account: {cred_data.get('client_email')}")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Invalid credential file {cred_file.name}: {e}")
    
    # Check .env file
    if env_file.exists():
        print(f"✅ Environment file found: {env_file}")
        
        with open(env_file, 'r') as f:
            env_content = f.read()
            if 'PROJECT_ID=' in env_content and 'your-project-id' not in env_content:
                print("✅ Environment file configured with project ID")
            else:
                print("⚠️ Environment file needs PROJECT_ID configuration")
    else:
        print("❌ Environment file (.env) not found")
    
    return len(valid_creds) > 0

def provide_setup_instructions():
    """Provide detailed setup instructions"""
    print("\n🛠️ PRODUCTION SETUP INSTRUCTIONS")
    print("=" * 50)
    
    print("\n📋 STEP 1: Create Google Cloud Project")
    print("   1. Go to https://console.cloud.google.com/")
    print("   2. Create a new project or select existing one")
    print("   3. Note your PROJECT_ID (not display name)")
    print("   4. Enable billing for the project")
    
    print("\n🔌 STEP 2: Enable APIs")
    print("   1. Go to APIs & Services > Library")
    print("   2. Search and enable 'BigQuery API'")
    print("   3. Search and enable 'BigQuery Storage API'")
    
    print("\n🔐 STEP 3: Create Service Account")
    print("   1. Go to IAM & Admin > Service Accounts")
    print("   2. Click 'Create Service Account'")
    print("   3. Name: 'retailsense-ai'")
    print("   4. Description: 'RetailSense AI BigQuery Access'")
    print("   5. Click 'Create and Continue'")
    
    print("\n🎯 STEP 4: Grant Permissions")
    print("   Add these roles to your service account:")
    print("   - BigQuery Data Editor")
    print("   - BigQuery Job User")
    print("   - BigQuery Admin (for ML model creation)")
    
    print("\n🔑 STEP 5: Download Credentials")
    print("   1. Click on your service account")
    print("   2. Go to 'Keys' tab")
    print("   3. Click 'Add Key' > 'Create New Key'")
    print("   4. Choose 'JSON' format")
    print("   5. Download the file")
    print("   6. Save as 'credentials/retailsense-ai-credentials.json'")
    
    print("\n⚙️ STEP 6: Update Environment")
    print("   1. Open .env file")
    print("   2. Replace 'your-project-id' with your actual PROJECT_ID")
    print("   3. Verify GOOGLE_APPLICATION_CREDENTIALS path")
    
    print("\n🚀 STEP 7: Test Setup")
    print("   Run: uv run python setup_production.py --test")

def test_production_setup():
    """Test the production setup"""
    print("\n🧪 TESTING PRODUCTION SETUP")
    print("=" * 50)
    
    try:
        # Try to import and initialize RetailSense AI
        sys.path.insert(0, 'src')
        from retailsense_ai import RetailSenseAI
        
        print("📦 Importing RetailSenseAI...")
        
        # Try to initialize (this will test credentials and project)
        print("🔗 Testing BigQuery connection...")
        ai = RetailSenseAI()
        
        print("✅ SUCCESS! Production setup is working")
        print(f"   Project: {ai.project_id}")
        print(f"   Dataset: {ai.dataset_id}")
        print("\n🚀 Ready to run: uv run python -m retailsense_ai.main --bigquery")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Credentials Error: {e}")
        print("💡 Make sure you've downloaded the service account JSON file")
        return False
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Check your .env file and credentials")
        return False
        
    except Exception as e:
        print(f"❌ Setup Error: {e}")
        print("💡 Review the setup instructions above")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RetailSense AI Production Setup Helper")
    parser.add_argument("--test", action="store_true", help="Test current setup")
    parser.add_argument("--check", action="store_true", help="Check setup status")
    
    args = parser.parse_args()
    
    if args.test:
        success = test_production_setup()
        sys.exit(0 if success else 1)
    elif args.check:
        has_valid_setup = check_credentials()
        if has_valid_setup:
            print("\n✅ Production setup appears ready for testing")
            print("💡 Run with --test flag to verify BigQuery connection")
        else:
            print("\n❌ Production setup incomplete")
            provide_setup_instructions()
    else:
        # Default: check setup and provide instructions
        has_valid_setup = check_credentials()
        if not has_valid_setup:
            provide_setup_instructions()
        else:
            print("\n✅ Credentials found! Run with --test to verify setup")

if __name__ == "__main__":
    main()