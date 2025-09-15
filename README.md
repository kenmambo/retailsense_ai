# 🛒 RetailSense AI
### *Multimodal E-commerce Intelligence Engine*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![BigQuery](https://img.shields.io/badge/Google%20Cloud-BigQuery-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

**🚀 Transform your e-commerce data into actionable AI-powered insights**

[🎯 Features](#-features) • [⚡ Quick Start](#-quick-start) • [📊 Demo](#-demo) • [🛠 Installation](#-installation) • [📚 Documentation](#-documentation)

</div>

---

## 🎯 Features

### 🧠 **AI-Powered Analytics**
- **Product Similarity Search** - Find related products using advanced embedding techniques
- **Pricing Optimization** - AI-driven pricing strategy recommendations
- **Conversion Rate Analysis** - Deep dive into customer behavior patterns
- **Revenue Forecasting** - Predict future performance trends

### 📊 **BigQuery Integration**
- **Real-time Data Processing** - Leverage Google Cloud's BigQuery for massive dataset analysis
- **GA4 E-commerce Data** - Built-in integration with Google Analytics 4 sample data
- **Scalable Architecture** - Handle millions of transactions effortlessly
- **Advanced SQL Analytics** - Custom BigQuery ML models and functions

### 🎨 **Rich Visualizations**
- **Interactive Dashboards** - Beautiful, informative charts and graphs
- **Executive Reports** - Automated insights generation for business stakeholders
- **Performance Metrics** - Key KPIs and conversion funnel analysis
- **Category Analysis** - Product performance across different categories

### 🔧 **Production Ready**
- **Secure Credentials Management** - Safe handling of sensitive authentication data
- **Modular Architecture** - Clean, maintainable code structure
- **Comprehensive Testing** - Full test suite for reliability
- **Easy Deployment** - Ready for cloud deployment with Docker support

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Google Cloud Project with BigQuery API enabled
- Service Account credentials (JSON file)

### 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/retailsense-ai.git
   cd retailsense-ai
   ```

2. **Install with uv**
   ```bash
   uv install
   ```

3. **Set up credentials**
   ```bash
   # Copy your service account JSON file to credentials/
   cp /path/to/your/service-account.json credentials/retailsense-ai-credentials.json
   ```

4. **Run the demo**
   ```bash
   uv run python -m retailsense_ai.demo
   ```

---

## 📊 Demo

### 🎮 Interactive Jupyter Notebooks
Explore the complete functionality with our comprehensive notebook series:

```bash
# Run the complete notebook series
uv run jupyter notebook notebooks/

# Or run specific notebooks:
uv run jupyter notebook notebooks/01_setup_and_overview.ipynb
uv run jupyter notebook notebooks/02_data_generation_and_eda.ipynb
uv run jupyter notebook notebooks/03_ai_similarity_search.ipynb
uv run jupyter notebook notebooks/04_business_intelligence.ipynb
uv run jupyter notebook notebooks/05_bigquery_integration.ipynb
uv run jupyter notebook notebooks/06_final_results.ipynb
```

### 🖥 Command Line Demo
For a quick demonstration without BigQuery setup:

```bash
uv run python src/retailsense_ai/demo.py
```

### 📈 Sample Output
```
🎯 RETAILSENSE AI - COMPLETE DEMO PIPELINE
============================================================

🚀 RetailSense AI Demo initialized!
   Mode: Offline demonstration
   Focus: Core e-commerce intelligence features

📊 Creating sample e-commerce data with 50 products...
✅ Generated 50 sample products
   💰 Total revenue: $803,517.00
   📈 Avg conversion rate: 2.24%

🔍 Analyzing product performance...
💰 Top 5 Products by Revenue:
   Premium Mouse 4K: $70,436.40
   Professional Cable: $61,210.19
   Smart Mouse: $49,549.22
```

---

## 🛠 Installation & Setup

### Method 1: Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone https://github.com/yourusername/retailsense-ai.git
cd retailsense-ai
uv install
```

### Method 2: Traditional pip

```bash
git clone https://github.com/yourusername/retailsense-ai.git
cd retailsense-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -e .
```

### 🔐 Google Cloud Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable BigQuery API

2. **Create Service Account**
   ```bash
   # Using gcloud CLI
   gcloud iam service-accounts create retailsense-ai
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \\
       --member="serviceAccount:retailsense-ai@YOUR_PROJECT_ID.iam.gserviceaccount.com" \\
       --role="roles/bigquery.admin"
   gcloud iam service-accounts keys create credentials/retailsense-ai-credentials.json \\
       --iam-account=retailsense-ai@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

3. **Update credentials path in your code or set environment variable**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="credentials/retailsense-ai-credentials.json"
   ```

---

## 🏗 Project Structure

```
retailsense-ai/
├── 📁 src/retailsense_ai/          # Main package
│   ├── __init__.py                 # Package initialization
│   ├── core.py                     # BigQuery integration & core logic
│   └── demo.py                     # Offline demo functionality
├── 📁 notebooks/                   # Jupyter notebooks
│   ├── 01_setup_and_overview.ipynb      # Project introduction and overview
│   ├── 02_data_generation_and_eda.ipynb # Data generation and analysis
│   ├── 03_ai_similarity_search.ipynb    # Vector search and recommendations
│   ├── 04_business_intelligence.ipynb   # Forecasting and insights
│   ├── 05_bigquery_integration.ipynb    # Production BigQuery integration
│   ├── 06_final_results.ipynb           # Business impact and results
│   └── retailsense_ai_complete_demo.ipynb # Legacy demo notebook
├── 📁 credentials/                 # Secure credential storage
│   └── service-account-template.json
├── 📁 outputs/                     # Generated reports and visualizations
├── 📁 tests/                       # Test suite
├── 📁 docs/                        # Documentation
├── .gitignore                      # Git ignore file
├── pyproject.toml                  # Project configuration
└── README.md                       # This file
```

---

## 💻 Usage Examples

### Basic Analytics
```python
from retailsense_ai import RetailSenseAI

# Initialize with your project
ai = RetailSenseAI(project_id="your-project-id")

# Set up environment and load data
ai.setup_environment()
ai.load_ga4_data()
ai.create_product_performance_table()

# Get insights
performance_data = ai.get_performance_data()
category_analysis = ai.get_category_analysis()
```

### Offline Demo
```python
from retailsense_ai import RetailSenseAIDemo

# Run complete offline demonstration
demo = RetailSenseAIDemo()
results = demo.run_full_demo(output_dir="my_outputs")

# Access generated insights
insights = results['insights']
dashboard_path = results['dashboard_path']
```

---

## 📚 Documentation

### 🎯 Key Components

| Component | Description | Usage |
|-----------|-------------|-------|
| `RetailSenseAI` | Main class for BigQuery integration | Production analytics with real data |
| `RetailSenseAIDemo` | Offline demonstration class | Testing and demos without cloud setup |
| Jupyter Notebook | Complete interactive tutorial | Learning and experimentation |

### 📊 Available Analytics

- **Product Performance Metrics**
  - Revenue analysis
  - Conversion rate tracking
  - Customer behavior patterns

- **AI-Powered Features**
  - Product similarity search
  - Pricing optimization recommendations
  - Performance forecasting

- **Business Intelligence**
  - Executive summary reports
  - Category performance analysis
  - Actionable recommendations

---

## 🧪 Testing

Run the test suite to ensure everything works correctly:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=retailsense_ai

# Run specific test
uv run pytest tests/test_demo.py
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/retailsense-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/retailsense-ai/discussions)
- **Email**: team@retailsense.ai

---

## 🌟 Acknowledgments

- Google Cloud BigQuery team for the amazing AI capabilities
- Google Analytics 4 for the sample e-commerce dataset
- The open-source community for the excellent Python libraries

---

<div align="center">

**🚀 Ready to transform your e-commerce intelligence?**

[Get Started](#-quick-start) • [View Demo](notebooks/retailsense_ai_complete_demo.ipynb) • [Report Issues](https://github.com/yourusername/retailsense-ai/issues)

---

Made with ❤️ by the RetailSense AI Team

</div>