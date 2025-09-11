# RetailSense AI - BigQuery Script Runner
# PowerShell script to run all BigQuery SQL scripts using gcloud

param(
    [string]$ProjectId = "retailsense-ai",
    [switch]$RunAll = $false,
    [string]$SingleScript = ""
)

Write-Host "🚀 RetailSense AI - BigQuery Script Runner" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud version 2>$null
    Write-Host "✅ Google Cloud CLI detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI not found. Please install gcloud CLI first." -ForegroundColor Red
    exit 1
}

# Set project
Write-Host "🔧 Setting project to: $ProjectId" -ForegroundColor Yellow
gcloud config set project $ProjectId

# Define scripts in execution order
$scripts = @(
    @{Name="01_setup_dataset.sql"; Description="📁 Setting up dataset"},
    @{Name="02_load_ga4_data.sql"; Description="📥 Loading GA4 data"},
    @{Name="03_create_product_analytics.sql"; Description="📊 Creating product analytics"},
    @{Name="04_create_ml_models.sql"; Description="🤖 Training ML models"},
    @{Name="05_ml_predictions.sql"; Description="🔮 Generating predictions"},
    @{Name="06_executive_dashboard.sql"; Description="📈 Creating dashboard"}
)

function Run-BigQueryScript {
    param($ScriptPath, $Description)
    
    Write-Host "`n$Description" -ForegroundColor Yellow
    Write-Host "Running: $ScriptPath" -ForegroundColor Gray
    
    try {
        $result = gcloud sql query --sql-file="sql\$ScriptPath" --project=$ProjectId 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Completed: $ScriptPath" -ForegroundColor Green
        } else {
            Write-Host "❌ Error in: $ScriptPath" -ForegroundColor Red
            Write-Host $result -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "❌ Failed to execute: $ScriptPath" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor Red
        return $false
    }
    return $true
}

# Run single script or all scripts
if ($SingleScript -ne "") {
    $script = $scripts | Where-Object { $_.Name -eq $SingleScript }
    if ($script) {
        Run-BigQueryScript $script.Name $script.Description
    } else {
        Write-Host "❌ Script not found: $SingleScript" -ForegroundColor Red
        Write-Host "Available scripts:" -ForegroundColor Yellow
        $scripts | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Gray }
    }
} elseif ($RunAll) {
    Write-Host "`n🔄 Running all scripts in sequence..." -ForegroundColor Cyan
    
    $allSuccess = $true
    foreach ($script in $scripts) {
        $success = Run-BigQueryScript $script.Name $script.Description
        if (-not $success) {
            $allSuccess = $false
            Write-Host "❌ Stopping execution due to error" -ForegroundColor Red
            break
        }
        Start-Sleep -Seconds 2  # Brief pause between scripts
    }
    
    if ($allSuccess) {
        Write-Host "`n🎉 All scripts completed successfully!" -ForegroundColor Green
        Write-Host "🔗 View your BigQuery console: https://console.cloud.google.com/bigquery?project=$ProjectId" -ForegroundColor Cyan
    }
} else {
    Write-Host "`nUsage:" -ForegroundColor Yellow
    Write-Host "  .\run_bigquery_scripts.ps1 -RunAll                    # Run all scripts"
    Write-Host "  .\run_bigquery_scripts.ps1 -SingleScript '01_setup_dataset.sql'  # Run specific script"
    Write-Host "  .\run_bigquery_scripts.ps1 -ProjectId 'your-project'  # Use different project"
    Write-Host ""
    Write-Host "Available scripts:" -ForegroundColor Cyan
    $scripts | ForEach-Object { 
        Write-Host "  📄 $($_.Name) - $($_.Description)" -ForegroundColor Gray
    }
}

Write-Host "`n✨ RetailSense AI BigQuery Setup Complete!" -ForegroundColor Cyan