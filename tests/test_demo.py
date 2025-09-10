"""
Tests for RetailSense AI Demo functionality
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from unittest.mock import patch, MagicMock

# Add src to path for testing
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from retailsense_ai.demo import RetailSenseAIDemo


class TestRetailSenseAIDemo:
    """Test suite for RetailSenseAIDemo class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.demo = RetailSenseAIDemo()
        
    def test_initialization(self):
        """Test demo initialization"""
        assert isinstance(self.demo, RetailSenseAIDemo)
        
    def test_create_sample_data(self):
        """Test sample data generation"""
        n_products = 10
        df = self.demo.create_sample_data(n_products=n_products)
        
        # Check data structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == n_products
        
        # Check required columns
        required_columns = [
            'product_sku', 'product_name', 'category', 'brand', 'price',
            'total_views', 'total_cart_adds', 'total_purchases', 'total_revenue',
            'view_to_purchase_rate', 'cart_to_purchase_rate'
        ]
        for col in required_columns:
            assert col in df.columns
            
        # Check data types and ranges
        assert df['price'].dtype in [np.float64, float]
        assert df['total_views'].dtype in [np.int64, int]
        assert (df['price'] >= 20).all()
        assert (df['price'] <= 500).all()
        assert (df['total_views'] >= 100).all()
        assert (df['view_to_purchase_rate'] >= 0).all()
        assert (df['view_to_purchase_rate'] <= 1).all()
        
    def test_generate_product_name(self):
        """Test product name generation"""
        name = self.demo._generate_product_name(0)
        assert isinstance(name, str)
        assert len(name) > 0
        
    def test_analyze_performance(self):
        """Test performance analysis"""
        # Generate sample data first
        self.demo.create_sample_data(n_products=20)
        
        # Run analysis
        top_products, category_analysis = self.demo.analyze_performance()
        
        # Check top products
        assert isinstance(top_products, pd.DataFrame)
        assert len(top_products) <= 5
        
        # Check category analysis
        assert isinstance(category_analysis, pd.DataFrame)
        assert 'total_revenue' in category_analysis.columns
        assert 'view_to_purchase_rate' in category_analysis.columns
        
    def test_create_visualizations(self):
        """Test visualization creation"""
        # Generate sample data first
        self.demo.create_sample_data(n_products=20)
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            dashboard_path = self.demo.create_visualizations(output_dir=temp_dir)
            
            # Check that file was created
            assert os.path.exists(dashboard_path)
            assert dashboard_path.endswith('.png')
            
    def test_demo_similarity_search(self):
        """Test similarity search functionality"""
        # Generate sample data first
        self.demo.create_sample_data(n_products=20)
        
        # Run similarity search
        target_product, similar_products = self.demo.demo_similarity_search()
        
        # Check results
        assert isinstance(target_product, pd.Series)
        assert isinstance(similar_products, list)
        assert len(similar_products) > 0
        
        # Check similarity structure
        for product in similar_products:
            assert 'product_sku' in product
            assert 'similarity_score' in product
            assert isinstance(product['similarity_score'], float)
            assert 0 <= product['similarity_score'] <= 1
            
    def test_generate_insights_report(self):
        """Test insights report generation"""
        # Generate sample data first
        self.demo.create_sample_data(n_products=20)
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            insights, report_path = self.demo.generate_insights_report(output_dir=temp_dir)
            
            # Check insights structure
            assert isinstance(insights, dict)
            assert 'executive_summary' in insights
            assert 'key_findings' in insights
            assert 'recommendations' in insights
            
            # Check executive summary
            summary = insights['executive_summary']
            assert 'total_products' in summary
            assert 'total_revenue' in summary
            assert 'average_conversion_rate' in summary
            
            # Check report file
            assert os.path.exists(report_path)
            assert report_path.endswith('.json')
            
    def test_run_full_demo(self):
        """Test complete demo pipeline"""
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            results = self.demo.run_full_demo(output_dir=temp_dir)
            
            # Check results structure
            assert isinstance(results, dict)
            required_keys = [
                'products_df', 'top_products', 'category_analysis',
                'dashboard_path', 'insights', 'report_path'
            ]
            for key in required_keys:
                assert key in results
                
            # Check that files were created
            assert os.path.exists(results['dashboard_path'])
            assert os.path.exists(results['report_path'])
            
    def test_empty_data_handling(self):
        """Test handling of edge cases"""
        # Test with minimal data
        df = self.demo.create_sample_data(n_products=1)
        assert len(df) == 1
        
        # Ensure all required fields are present
        assert df['total_revenue'].iloc[0] >= 0
        assert 0 <= df['view_to_purchase_rate'].iloc[0] <= 1


class TestRetailSenseAIDemoIntegration:
    """Integration tests for RetailSense AI Demo"""
    
    def test_reproducible_results(self):
        """Test that results are reproducible with same seed"""
        demo1 = RetailSenseAIDemo()
        demo2 = RetailSenseAIDemo()
        
        # Both should generate identical data with same parameters
        df1 = demo1.create_sample_data(n_products=10)
        df2 = demo2.create_sample_data(n_products=10)
        
        # Check that data is identical (numpy seed is set in create_sample_data)
        pd.testing.assert_frame_equal(df1, df2)
        
    def test_data_quality(self):
        """Test data quality and business logic"""
        demo = RetailSenseAIDemo()
        df = demo.create_sample_data(n_products=50)
        
        # Business logic checks
        assert (df['total_cart_adds'] <= df['total_views']).all()
        assert (df['total_purchases'] <= df['total_cart_adds']).all()
        assert (df['total_revenue'] >= 0).all()
        
        # Check that conversion rates make sense
        calculated_conversion = df['total_purchases'] / df['total_views']
        np.testing.assert_array_almost_equal(
            df['view_to_purchase_rate'].values,
            calculated_conversion.values,
            decimal=10
        )
        
    @patch('matplotlib.pyplot.savefig')
    def test_visualization_without_file_io(self, mock_savefig):
        """Test visualization creation without actual file I/O"""
        demo = RetailSenseAIDemo()
        demo.create_sample_data(n_products=20)
        
        # Mock the savefig to avoid actual file creation
        mock_savefig.return_value = None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            dashboard_path = demo.create_visualizations(output_dir=temp_dir)
            
            # Check that savefig was called
            mock_savefig.assert_called_once()
            assert temp_dir in dashboard_path


if __name__ == "__main__":
    pytest.main([__file__])