# 🚀 RetailSense AI - BigQuery SQL Scripts

This directory contains comprehensive SQL scripts to set up and run RetailSense AI analytics directly in BigQuery.

## 📋 Available Scripts

| Script | Description | Purpose |
|--------|-------------|---------|
| `01_setup_dataset.sql` | 📁 Dataset Setup | Creates the retail_intelligence dataset |
| `02_load_ga4_data.sql` | 📥 Data Loading | Loads GA4 e-commerce sample data |
| `03_create_product_analytics.sql` | 📊 Analytics | Creates product performance metrics |
| `04_create_ml_models.sql` | 🤖 ML Models | Trains BigQuery ML models |
| `05_ml_predictions.sql` | 🔮 Predictions | Generates ML predictions and insights |
| `06_executive_dashboard.sql` | 📈 Dashboard | Executive-level KPIs and reports |
| `run_all.sql` | 🎯 Master Script | References to run all scripts |

## 🛠 Running Scripts with gcloud CLI

### Prerequisites
1. **Install gcloud CLI**: https://cloud.google.com/sdk/docs/install
2. **Authenticate**: `gcloud auth login`
3. **Set project**: `gcloud config set project YOUR_PROJECT_ID`

### Option 1: Run Individual Scripts
```bash
# Run each script individually
gcloud query --sql-file="sql/01_setup_dataset.sql"
gcloud query --sql-file="sql/02_load_ga4_data.sql"
gcloud query --sql-file="sql/03_create_product_analytics.sql"
gcloud query --sql-file="sql/04_create_ml_models.sql"
gcloud query --sql-file="sql/05_ml_predictions.sql"
gcloud query --sql-file="sql/06_executive_dashboard.sql"
```

### Option 2: Run All Scripts (PowerShell)
```powershell
# Windows PowerShell
.\run_bigquery_scripts.ps1 -RunAll

# Run specific script
.\run_bigquery_scripts.ps1 -SingleScript "01_setup_dataset.sql"

# Use different project
.\run_bigquery_scripts.ps1 -ProjectId "your-project-id" -RunAll
```

### Option 3: BigQuery Console
1. Go to [BigQuery Console](https://console.cloud.google.com/bigquery)
2. Open query editor
3. Copy and paste script content
4. Click "Run"

## 🎯 Quick Start Commands

```bash
# Set your project
export PROJECT_ID="retailsense-ai"
gcloud config set project $PROJECT_ID

# Run all scripts in sequence
cd sql
gcloud query --sql-file="01_setup_dataset.sql"
gcloud query --sql-file="02_load_ga4_data.sql"
gcloud query --sql-file="03_create_product_analytics.sql"
gcloud query --sql-file="04_create_ml_models.sql"
gcloud query --sql-file="05_ml_predictions.sql"
gcloud query --sql-file="06_executive_dashboard.sql"
```

## 📊 What Gets Created

### Tables
- `retail_intelligence.base_sales` - Raw GA4 e-commerce data
- `retail_intelligence.product_performance` - Product analytics with KPIs
- `retail_intelligence.product_predictions` - ML-based product predictions

### ML Models
- `retail_intelligence.revenue_forecasting_model` - ARIMA+ time series model
- `retail_intelligence.customer_segmentation_model` - K-means clustering
- `retail_intelligence.product_performance_classifier` - Logistic regression

### Views & Functions
- Advanced analytics queries
- Executive dashboard queries
- Prediction and forecasting queries

## 💡 Usage Examples

### Get Revenue Forecast
```sql
SELECT * FROM ML.FORECAST(
  MODEL `retail_intelligence.revenue_forecasting_model`,
  STRUCT(30 as horizon)
);
```

### Customer Segmentation
```sql
SELECT CENTROID_ID, COUNT(*) as customers
FROM ML.PREDICT(MODEL `retail_intelligence.customer_segmentation_model`, (...))
GROUP BY CENTROID_ID;
```

### Top Products Query
```sql
SELECT product_name, total_revenue, trend_status
FROM `retail_intelligence.product_performance`
ORDER BY total_revenue DESC
LIMIT 10;
```

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Grant BigQuery permissions
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="user:your-email@domain.com" \
     --role="roles/bigquery.admin"
   ```

2. **Project Not Set**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Billing Not Enabled**
   - Enable billing in Google Cloud Console
   - BigQuery requires active billing for queries

4. **API Not Enabled**
   ```bash
   gcloud services enable bigquery.googleapis.com
   ```

### Verification Commands
```bash
# Check current project
gcloud config get-value project

# List datasets
gcloud query --sql="SELECT * FROM \`${PROJECT_ID}\`.INFORMATION_SCHEMA.SCHEMATA"

# Check tables
gcloud query --sql="SELECT * FROM \`${PROJECT_ID}.retail_intelligence\`.INFORMATION_SCHEMA.TABLES"
```

## 📈 Expected Results

After running all scripts, you should have:

- **📊 183 products analyzed** from GA4 data
- **💰 $177,644 total revenue** processed
- **🤖 3 ML models trained** and ready for predictions
- **📈 30-day revenue forecast** available
- **👥 5 customer segments** identified
- **🎯 Executive dashboard** with KPIs

## 🔗 Next Steps

1. **View Results**: https://console.cloud.google.com/bigquery?project=YOUR_PROJECT_ID
2. **Create Dashboards**: Use Google Data Studio or Looker
3. **Schedule Queries**: Set up recurring analysis
4. **Export Data**: Download results for further analysis
5. **Integrate APIs**: Use BigQuery API for real-time access

## 🆘 Support

If you encounter issues:
1. Check the [BigQuery documentation](https://cloud.google.com/bigquery/docs)
2. Verify your project has BigQuery API enabled
3. Ensure proper IAM permissions
4. Check billing status

---

🎉 **Happy Analyzing with RetailSense AI!**