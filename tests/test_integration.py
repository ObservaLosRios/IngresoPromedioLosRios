"""
Integration tests for the ETL pipeline.
Tests the complete workflow.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd

from src.presentation.di_container import DIContainer


class TestETLIntegration:
    """Integration tests for the complete ETL pipeline."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_csv_file(self, temp_dir):
        """Create sample CSV file for testing."""
        csv_content = """Indicador,DTI_CL_ANO,Año,DTI_CL_REGION,Región,DTI_CL_SEXO,Sexo,Value
Ingreso medio nominal de la población ocupada,2020,2020,CHL14,Región de Los Ríos,_T,Ambos sexos,500000.0
Ingreso medio nominal de la población ocupada,2020,2020,CHL14,Región de Los Ríos,M,Hombres,550000.0
Ingreso medio nominal de la población ocupada,2020,2020,CHL14,Región de Los Ríos,F,Mujeres,450000.0
Ingreso medio nominal de la población ocupada,2021,2021,CHL14,Región de Los Ríos,_T,Ambos sexos,520000.0
Ingreso medio nominal de la población ocupada,2021,2021,CHL14,Región de Los Ríos,M,Hombres,570000.0
Ingreso medio nominal de la población ocupada,2021,2021,CHL14,Región de Los Ríos,F,Mujeres,470000.0"""
        
        csv_file = temp_dir / "test_income_data.csv"
        csv_file.write_text(csv_content)
        return str(csv_file)
    
    @pytest.fixture
    def di_container(self, temp_dir):
        """Create DI container with test configuration."""
        config = {
            'database_path': str(temp_dir / "test.db"),
            'output_path': str(temp_dir / "outputs"),
            'log_level': 'INFO',
            'log_file': str(temp_dir / "test.log")
        }
        return DIContainer(config)
    
    def test_full_etl_pipeline(self, sample_csv_file, di_container):
        """Test complete ETL pipeline execution."""
        # Get ETL pipeline
        pipeline = di_container.get_full_etl_pipeline()
        
        # Execute pipeline
        results = pipeline.execute(sample_csv_file, ['csv', 'excel'])
        
        # Verify results
        assert results['status'] == 'success'
        assert results['records_processed'] == 6
        assert 'analysis_results' in results
        assert 'generated_files' in results
        
        # Verify analysis results
        analysis_results = results['analysis_results']
        assert 'gender_analyses' in analysis_results
        assert 'trend_analyses' in analysis_results
        assert 'summary_statistics' in analysis_results
        
        # Verify gender analysis
        gender_analyses = analysis_results['gender_analyses']
        assert len(gender_analyses) == 2  # 2020 and 2021
        
        # Check 2020 analysis
        analysis_2020 = next(a for a in gender_analyses if a.year == 2020)
        assert analysis_2020.male_income == 550000.0
        assert analysis_2020.female_income == 450000.0
        assert analysis_2020.gender_gap == 100000.0
        
        # Verify trend analysis
        trend_analyses = analysis_results['trend_analyses']
        assert '_T' in trend_analyses  # Total population
        assert 'M' in trend_analyses   # Male
        assert 'F' in trend_analyses   # Female
        
        # Check total population trend
        total_trend = trend_analyses['_T']
        assert total_trend.start_year == 2020
        assert total_trend.end_year == 2021
        assert total_trend.growth_rate > 0  # Income increased
    
    def test_extract_use_case(self, sample_csv_file, di_container):
        """Test extract use case in isolation."""
        extract_use_case = di_container.get_extract_use_case()
        
        records = extract_use_case.execute(sample_csv_file)
        
        assert len(records) == 6
        
        # Check first record
        first_record = records[0]
        assert first_record.year in [2020, 2021]
        assert first_record.region_name == "Región de Los Ríos"
        assert first_record.value > 0
    
    def test_transform_use_case(self, sample_csv_file, di_container):
        """Test transform use case in isolation."""
        # First extract data
        extract_use_case = di_container.get_extract_use_case()
        records = extract_use_case.execute(sample_csv_file)
        
        # Then transform
        transform_use_case = di_container.get_transform_use_case()
        results = transform_use_case.execute(records)
        
        assert 'gender_analyses' in results
        assert 'trend_analyses' in results
        assert 'summary_statistics' in results
        assert results['total_records'] == 6
        
        # Verify year range
        year_range = results['year_range']
        assert year_range['start'] == 2020
        assert year_range['end'] == 2021
    
    def test_load_use_case(self, sample_csv_file, di_container, temp_dir):
        """Test load use case in isolation."""
        # Setup: extract and transform data
        extract_use_case = di_container.get_extract_use_case()
        records = extract_use_case.execute(sample_csv_file)
        
        transform_use_case = di_container.get_transform_use_case()
        analysis_results = transform_use_case.execute(records)
        
        # Test load use case
        load_use_case = di_container.get_load_use_case()
        generated_files = load_use_case.execute(records, analysis_results, ['csv'])
        
        assert 'csv' in generated_files
        assert 'analysis' in generated_files
        
        # Verify CSV file was created
        csv_path = Path(generated_files['csv'])
        assert csv_path.exists()
        
        # Verify content
        df = pd.read_csv(csv_path)
        assert len(df) == 6
        assert 'Año' in df.columns
        assert 'Valor' in df.columns
    
    def test_invalid_csv_file(self, di_container, temp_dir):
        """Test pipeline with invalid CSV file."""
        # Create invalid CSV
        invalid_csv = temp_dir / "invalid.csv"
        invalid_csv.write_text("invalid,csv,content\n1,2,3")
        
        pipeline = di_container.get_full_etl_pipeline()
        results = pipeline.execute(str(invalid_csv))
        
        assert results['status'] == 'failed'
        assert 'error' in results
    
    def test_nonexistent_file(self, di_container):
        """Test pipeline with nonexistent file."""
        pipeline = di_container.get_full_etl_pipeline()
        results = pipeline.execute("nonexistent_file.csv")
        
        assert results['status'] == 'failed'
        assert 'error' in results
