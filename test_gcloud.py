#!/usr/bin/env python3
"""
Test gcloud installation and run BigQuery scripts
"""

import subprocess
import sys
import os

def test_gcloud():
    """Test if gcloud is installed and working"""
    print("🔍 Testing gcloud CLI installation...")
    
    try:
        # Try different possible gcloud paths
        gcloud_commands = [
            'gcloud',
            'gcloud.exe', 
            r'C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.exe',
            r'C:\Users\{}\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.exe'.format(os.getenv('USERNAME'))
        ]
        
        for gcloud_cmd in gcloud_commands:
            try:
                result = subprocess.run([gcloud_cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Found gcloud at: {gcloud_cmd}")
                    print(f"Version: {result.stdout.split()[2]}")
                    return gcloud_cmd
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                continue
                
        print("❌ gcloud CLI not found in standard locations")
        print("\n📥 To install gcloud CLI:")
        print("1. Go to: https://cloud.google.com/sdk/docs/install")
        print("2. Download and install Google Cloud CLI")
        print("3. Restart your terminal")
        print("4. Run: gcloud auth login")
        return None
        
    except Exception as e:
        print(f"❌ Error testing gcloud: {e}")
        return None

def run_bigquery_script(gcloud_cmd, script_path, project_id="retailsense-ai"):
    """Run a BigQuery script using gcloud"""
    print(f"\n🚀 Running {script_path}...")
    
    try:
        # Use bq command which is more reliable for BigQuery
        bq_cmd = gcloud_cmd.replace('gcloud', 'bq')
        
        cmd = [bq_cmd, 'query', 
               '--use_legacy_sql=false',
               '--project_id=' + project_id,
               '--format=prettyjson']
        
        # Read SQL file
        with open(script_path, 'r') as f:
            sql_content = f.read()
        
        # Run the query
        result = subprocess.run(cmd, input=sql_content, 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ Successfully executed {script_path}")
            return True
        else:
            print(f"❌ Error executing {script_path}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to run {script_path}: {e}")
        return False

def main():
    print("🚀 RetailSense AI - BigQuery Script Test")
    print("=" * 50)
    
    # Test gcloud installation
    gcloud_cmd = test_gcloud()
    
    if not gcloud_cmd:
        print("\n💡 Alternative: You can run scripts directly in BigQuery Console")
        print("1. Go to: https://console.cloud.google.com/bigquery")
        print("2. Open query editor")
        print("3. Copy and paste script content from sql/ directory")
        print("4. Click 'Run'")
        return
    
    # Test project access
    print(f"\n🔧 Testing project access...")
    try:
        result = subprocess.run([gcloud_cmd, 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            project_id = result.stdout.strip()
            print(f"✅ Current project: {project_id}")
        else:
            project_id = "retailsense-ai"
            print(f"⚠️ No project set, using default: {project_id}")
            print(f"💡 To set project: gcloud config set project YOUR_PROJECT_ID")
    except Exception as e:
        project_id = "retailsense-ai"
        print(f"⚠️ Could not get project, using default: {project_id}")
    
    # Show available scripts
    sql_dir = "sql"
    if os.path.exists(sql_dir):
        print(f"\n📁 Available SQL scripts in {sql_dir}/:")
        sql_files = [f for f in os.listdir(sql_dir) if f.endswith('.sql')]
        for sql_file in sorted(sql_files):
            print(f"   📄 {sql_file}")
        
        print(f"\n🎯 To run scripts:")
        print(f"Option 1 - BigQuery Console (Recommended):")
        print(f"   1. Open: https://console.cloud.google.com/bigquery?project={project_id}")
        print(f"   2. Copy content from sql/*.sql files")
        print(f"   3. Paste and run in query editor")
        
        print(f"\nOption 2 - Command Line:")
        print(f"   bq query --use_legacy_sql=false --project_id={project_id} < sql/01_setup_dataset.sql")
        
        print(f"\nOption 3 - Python Script:")
        print(f"   uv run python test_gcloud.py")
        
    else:
        print(f"❌ SQL directory not found: {sql_dir}")
    
    print(f"\n✨ Ready to run RetailSense AI BigQuery analytics!")

if __name__ == "__main__":
    main()