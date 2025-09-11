# RetailSense AI - Production Setup Guide

## 🚀 Transitioning from Demo to Production

This guide will help you transition your RetailSense AI project from using demo data to real BigQuery data with Google Analytics 4.

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ A Google Cloud Project with billing enabled
- ✅ BigQuery API enabled in your project
- ✅ Google Analytics 4 setup (optional - can use public dataset)
- ✅ Basic understanding of BigQuery and Google Cloud IAM

## 🛠 Step-by-Step Setup

### Step 1: Google Cloud Project Setup

1. **Create or Select a Google Cloud Project**
   ```bash
   # Using gcloud CLI (optional)
   gcloud projects create your-retailsense-project-id
   gcloud config set project your-retailsense-project-id
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable bigquery.googleapis.com
   gcloud services enable storage.googleapis.com
   ```

   Or via the [Google Cloud Console](https://console.cloud.google.com/apis/library):
   - BigQuery API
   - Google Cloud Storage API

### Step 2: Service Account Creation

1. **Create a Service Account**
   ```bash
   gcloud iam service-accounts create retailsense-ai \\
       --display-name="RetailSense AI Service Account" \\
       --description="Service account for RetailSense AI BigQuery access"
   ```

2. **Grant BigQuery Permissions**
   ```bash
   # Basic BigQuery permissions
   gcloud projects add-iam-policy-binding your-project-id \\
       --member="serviceAccount:retailsense-ai@your-project-id.iam.gserviceaccount.com" \\
       --role="roles/bigquery.dataEditor"
   
   gcloud projects add-iam-policy-binding your-project-id \\
       --member="serviceAccount:retailsense-ai@your-project-id.iam.gserviceaccount.com" \\
       --role="roles/bigquery.jobUser"
   ```

3. **Create and Download Service Account Key**
   ```bash
   gcloud iam service-accounts keys create credentials/retailsense-ai-credentials.json \\
       --iam-account=retailsense-ai@your-project-id.iam.gserviceaccount.com
   ```

### Step 3: Local Environment Configuration

1. **Update your `.env` file**
   ```env
   # Update these values with your actual project details
   PROJECT_ID=your-actual-project-id
   GOOGLE_APPLICATION_CREDENTIALS=credentials/retailsense-ai-credentials.json
   DATASET_ID=retail_intelligence
   BIGQUERY_LOCATION=US
   
   # Demo Configuration (keep as is)
   DEMO_OUTPUT_DIR=outputs
   DEMO_SAMPLE_SIZE=50
   DEMO_VISUALIZATION_DPI=300
   
   # Development Settings
   DEBUG=false
   LOG_LEVEL=INFO
   ```

2. **Install Dependencies**
   ```bash
   # Install/update all dependencies including python-dotenv
   uv install
   ```

### Step 4: Verify Setup

1. **Test BigQuery Connection**
   ```bash
   # This should now connect to your BigQuery project
   uv run python -c "from retailsense_ai import RetailSenseAI; ai = RetailSenseAI(); print('✅ BigQuery connection successful!')"
   ```

2. **Run a Quick BigQuery Test**
   ```bash
   uv run python -m retailsense_ai.main --bigquery --output-dir test_output
   ```

## 📊 Data Sources

### Option 1: Google Analytics 4 Public Dataset (Recommended for Testing)

The project is configured to use Google's public GA4 e-commerce dataset:
- Dataset: `bigquery-public-data.ga4_obfuscated_sample_ecommerce`
- Contains real e-commerce event data (anonymized)
- No additional setup required
- Free to query (subject to BigQuery quotas)

### Option 2: Your Own GA4 Data

To use your own Google Analytics 4 data:

1. **Link GA4 to BigQuery**
   - In GA4 Admin → BigQuery Links
   - Create a new BigQuery link
   - Choose daily export settings

2. **Update Data Source in Code**
   ```python
   # In core.py, modify the load_ga4_data method to point to your dataset
   # Replace: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*
   # With: your-project.analytics_123456789.events_*
   ```

## 🔧 Advanced Configuration

### Custom Dataset Configuration

```python
# You can customize the dataset and table names
retail_ai = RetailSenseAI(
    project_id="your-project-id",
    dataset_id="custom_retail_analytics",
    credentials_path="path/to/your/credentials.json"
)
```

### Environment Variables

All configuration can be managed via environment variables:

```bash
export PROJECT_ID="your-project-id"
export DATASET_ID="retail_intelligence"
export GOOGLE_APPLICATION_CREDENTIALS="credentials/retailsense-ai-credentials.json"
export BIGQUERY_LOCATION="US"
```

## 🚨 Security Best Practices

### 1. Credential Security
- ✅ Never commit credential files to version control
- ✅ Use environment variables in production
- ✅ Rotate service account keys regularly
- ✅ Follow principle of least privilege

### 2. BigQuery Security
- ✅ Use dataset-level permissions
- ✅ Enable audit logging
- ✅ Set up billing alerts
- ✅ Monitor query costs

### 3. Production Deployment
```bash
# For production, use environment variables instead of .env files
export PROJECT_ID="production-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/secure/path/to/credentials.json"

# Run the application
uv run python -m retailsense_ai.main --bigquery
```

## 🎯 Available Analysis Features

Once configured, you can access:

### Basic Analytics
- Product performance metrics
- Category analysis  
- Conversion rate analysis
- Revenue insights

### Advanced ML Features
- Product recommendation models
- Customer segmentation
- Revenue forecasting
- Product similarity search

### Example Usage
```python
from retailsense_ai import RetailSenseAI

# Initialize with your configuration
ai = RetailSenseAI()

# Run complete ML pipeline
analytics_data = ai.create_comprehensive_pipeline()

# Get specific insights
recommendations = ai.get_product_recommendations(user_id="user123")
forecast = ai.get_revenue_forecast(forecast_days=30)
segments = ai.get_customer_segments()
```

## 🔍 Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Verify the file path in `.env`
   - Check file permissions
   - Ensure the file is valid JSON

2. **"Permission denied"**
   - Verify service account has BigQuery permissions
   - Check project billing is enabled
   - Confirm APIs are enabled

3. **"Dataset not found"**
   - The dataset will be created automatically
   - Verify you have dataset creation permissions
   - Check the dataset location setting

4. **"Query timeout"**
   - Some ML model creation queries take time
   - Check BigQuery quotas
   - Monitor query progress in BigQuery console

### Getting Help

- Check the [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- Review [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- Monitor costs in [Google Cloud Console](https://console.cloud.google.com/billing)

## 💰 Cost Considerations

### BigQuery Pricing
- **Query Processing**: ~$5 per TB processed
- **Storage**: ~$0.02 per GB per month
- **ML Models**: Additional charges for model training

### Cost Optimization Tips
- Use table partitioning for large datasets
- Implement query result caching
- Set up billing alerts
- Use slots for predictable workloads

## 🚀 Next Steps

After successful setup:

1. **Explore the Data**
   ```bash
   uv run python -m retailsense_ai.main --bigquery
   ```

2. **Set Up Automated Pipelines**
   - Schedule regular data refreshes
   - Implement monitoring and alerting
   - Set up automated reporting

3. **Integrate with Business Systems**
   - Export insights to BI tools
   - Set up API access for applications
   - Create automated dashboards

4. **Scale the Analysis**
   - Add more data sources
   - Implement real-time analytics
   - Build custom ML models

## 📞 Support

If you encounter issues during setup:

1. Check the logs for detailed error messages
2. Verify all prerequisites are met
3. Test with demo mode first: `uv run python -m retailsense_ai.main --demo`
4. Review Google Cloud Console for permission issues

---

🎉 **Congratulations!** You're now ready to analyze real e-commerce data with RetailSense AI and BigQuery ML!