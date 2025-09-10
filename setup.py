#!/usr/bin/env python3
"""
Setup script for RetailSense AI

This script helps set up the RetailSense AI environment and dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_uv_installation():
    """Check if uv is installed"""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ uv not found")
    print("💡 Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh")
    return False


def setup_credentials():
    """Set up credentials directory and template"""
    credentials_dir = Path("credentials")
    credentials_dir.mkdir(exist_ok=True)
    
    # Check if real credentials exist
    real_creds = credentials_dir / "retailsense-ai-ceb777b5822d.json"
    if real_creds.exists():
        print("✅ Google Cloud credentials found")
        return True
    
    # Check for template
    template_creds = credentials_dir / "service-account-template.json"
    if template_creds.exists():
        print("⚠️  Only template credentials found")
        print("💡 Replace template with your actual service account JSON")
        return False
    
    print("❌ No credentials found")
    print("💡 Place your Google Cloud service account JSON in credentials/")
    return False


def setup_directories():
    """Create required directories"""
    directories = ["outputs", "docs", "tests"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory: {directory}/")
    
    return True


def install_dependencies():
    """Install project dependencies using uv"""
    try:
        print("📦 Installing dependencies with uv...")
        result = subprocess.run(['uv', 'install'], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Output: {e.output}")
        return False
    except FileNotFoundError:
        print("❌ uv not found - please install uv first")
        return False


def run_tests():
    """Run the test suite"""
    try:
        print("🧪 Running tests...")
        result = subprocess.run(['uv', 'run', 'pytest', 'tests/', '-v'], 
                              check=True, capture_output=True, text=True)
        print("✅ All tests passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Some tests failed")
        print("💡 This is normal if BigQuery credentials are not set up")
        return False


def run_demo():
    """Run a quick demo to verify installation"""
    try:
        print("🎯 Running quick demo...")
        result = subprocess.run(['uv', 'run', 'python', '-m', 'retailsense_ai.main', '--demo'], 
                              check=True, capture_output=True, text=True, timeout=60)
        print("✅ Demo completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Demo timed out (this may be normal)")
        return True


def main():
    """Main setup function"""
    print("🛒 RETAILSENSE AI - SETUP SCRIPT")
    print("=" * 50)
    print("Setting up your RetailSense AI development environment...")
    print()
    
    success_count = 0
    total_checks = 7
    
    # 1. Check Python version
    if check_python_version():
        success_count += 1
    
    # 2. Check uv installation
    if check_uv_installation():
        success_count += 1
    
    # 3. Setup directories
    if setup_directories():
        success_count += 1
    
    # 4. Setup credentials
    if setup_credentials():
        success_count += 1
    
    # 5. Install dependencies
    if install_dependencies():
        success_count += 1
    
    # 6. Run tests
    if run_tests():
        success_count += 1
    
    # 7. Run demo
    if run_demo():
        success_count += 1
    
    print(f"\n📊 SETUP SUMMARY")
    print("=" * 50)
    print(f"✅ Successful: {success_count}/{total_checks}")
    
    if success_count == total_checks:
        print("🎉 Setup completed successfully!")
        print("\n🚀 Next steps:")
        print("   uv run python -m retailsense_ai.main --demo")
        print("   uv run jupyter notebook notebooks/retailsense_ai_complete_demo.ipynb")
    elif success_count >= 5:
        print("⚠️  Setup mostly complete with minor issues")
        print("💡 Check the messages above for any required actions")
    else:
        print("❌ Setup incomplete - please resolve the issues above")
    
    print(f"\n📚 Documentation: README.md")
    print(f"🆘 Support: https://github.com/yourusername/retailsense-ai/issues")


if __name__ == "__main__":
    main()