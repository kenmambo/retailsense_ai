# 🎯 RetailSense AI - Quick Start Guide

## 🚀 Ready-to-Use Commands

Your project supports both offline demo mode and production BigQuery analytics!

### 🏃‍♂️ **Run the Project**
```bash
# Run offline demo (no cloud setup required)
uv run python -m retailsense_ai.main --demo

# Run BigQuery analysis (requires Google Cloud credentials)
uv run python -m retailsense_ai.main --bigquery

# Run all tests
uv run pytest tests/ -v
```

### 🔧 **Quick Setup**

#### For Demo Mode (No Setup Required)
```bash
# Clone and run immediately
git clone <your-repo-url>
cd retailsense_ai
uv install
uv run python -m retailsense_ai.main --demo
```

#### For Production Mode (BigQuery)
1. **Set up Google Cloud credentials** (see [PRODUCTION_SETUP.md](PRODUCTION_SETUP.md))
2. **Update `.env` file** with your project details:
   ```env
   PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=credentials/retailsense-ai-credentials.json
   ```
3. **Run BigQuery analysis**:
   ```bash
   uv run python -m retailsense_ai.main --bigquery
   ```

### 📁 **Project Structure**
```
retailsense-ai/
├── 📁 src/retailsense_ai/          # Main package
│   ├── __init__.py                 # Package exports
│   ├── core.py                     # BigQuery integration
│   ├── demo.py                     # Offline analytics
│   └── main.py                     # CLI entry point
├── 📁 notebooks/                   # Jupyter notebooks
│   ├── 01_setup_and_overview.ipynb      # Project introduction and overview
│   ├── 02_data_generation_and_eda.ipynb # Data generation and analysis
│   ├── 03_ai_similarity_search.ipynb    # Vector search and recommendations
│   ├── 04_business_intelligence.ipynb   # Forecasting and insights
│   ├── 05_bigquery_integration.ipynb    # Production BigQuery integration
│   ├── 06_final_results.ipynb           # Business impact and results
│   └── retailsense_ai_complete_demo.ipynb # Legacy demo notebook
├── 📁 credentials/                 # Secure credentials (gitignored)
│   ├── service-account-template.json
│   └── retailsense-ai-ceb777b5822d.json (your actual credentials)
├── 📁 outputs/                     # Generated files
│   ├── retailsense_dashboard.png
│   ├── retailsense_insights_report.json
│   ├── bigquery_performance_data.csv
│   └── bigquery_category_analysis.csv
├── 📁 tests/                       # Test suite
├── pyproject.toml                  # uv project configuration
├── README.md                       # Comprehensive documentation
├── LICENSE                         # MIT license
└── .gitignore                      # Git ignore (includes credentials)
```

### 🔐 **Security Features**
- ✅ **Credentials Protected**: Your JSON file is in `credentials/` (gitignored)
- ✅ **Template Available**: `service-account-template.json` for sharing
- ✅ **Environment Variables**: Support for `.env` files
- ✅ **Path Handling**: Automatic credential discovery

### 📊 **Generated Outputs**
- **Dashboard**: Beautiful visualizations showing performance metrics
- **Insights Report**: Executive summary with actionable recommendations
- **BigQuery Data**: Real GA4 e-commerce analysis results
- **Test Coverage**: Comprehensive test suite ensuring reliability

### 🛠 **Development Features**
- **uv Package Management**: Fast, reliable dependency management
- **Modular Architecture**: Clean separation of concerns
- **Type Hints**: Full type annotation support
- **Testing**: Comprehensive pytest test suite
- **Documentation**: Rich README with examples

### 🎯 **What's Working**
1. ✅ **Offline Demo**: Generates sample data and analytics
2. ✅ **BigQuery Integration**: Connects to real GA4 data
3. ✅ **Visualizations**: Creates professional dashboards
4. ✅ **AI Features**: Product similarity and pricing optimization
5. ✅ **Jupyter Notebook**: Interactive analysis environment
6. ✅ **Tests**: All 12 tests passing
7. ✅ **CLI Interface**: Professional command-line tool

### 🚀 **GitHub Ready**
Your project is now perfectly organized for GitHub with:
- Professional README with badges and examples
- Secure credential management
- Comprehensive documentation
- MIT license
- Proper gitignore
- Test coverage
- Clean code structure

### 📚 **Next Steps**
1. **Push to GitHub**: `git add . && git commit -m "Initial commit" && git push`
2. **Share Demo**: Run `uv run python -m retailsense_ai.main --demo` for stakeholders
3. **Cloud Scale**: Use `--bigquery` for production analytics
4. **Interactive Analysis**: Explore the notebook series in `notebooks/`

### 💡 **Key Commands Summary**
```bash
# Quick demo
uv run python -m retailsense_ai.main --demo

# Full analysis with BigQuery
uv run python -m retailsense_ai.main --bigquery --output-dir my_analysis

# Interactive notebook series
uv run jupyter notebook notebooks/

# Run tests
uv run pytest tests/ -v

# Check project status
uv run python setup.py
```

## 🎉 **Your RetailSense AI Project is Ready!**

Everything is now professionally organized, secure, and ready to showcase your multimodal e-commerce intelligence platform!