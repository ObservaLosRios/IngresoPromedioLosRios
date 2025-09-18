"""
ETL Use Cases - Application Layer
Following Clean Architecture and SOLID principles.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

from domain.entities import IncomeRecord, IncomeAnalysis, TrendAnalysis
from domain.repositories import IncomeDataRepository, DataExportRepository
from domain.services import IncomeAnalysisService, TrendAnalysisService, DataQualityService
from infrastructure.data_loaders import CSVDataLoader
from infrastructure.visualization import IncomeVisualizationService


class ExtractDataUseCase:
    """
    Use case for extracting data from various sources.
    Implements Single Responsibility Principle.
    """
    
    def __init__(self, csv_loader: CSVDataLoader):
        """
        Initialize extract use case.
        
        Args:
            csv_loader: CSV data loader implementation
        """
        self._csv_loader = csv_loader
        self._quality_service = DataQualityService()
    
    def execute(self, filepath: str) -> List[IncomeRecord]:
        """
        Extract and validate income data from source.
        
        Args:
            filepath: Path to source data file
            
        Returns:
            List of validated IncomeRecord entities
            
        Raises:
            ValueError: If data validation fails
        """
        logger.info(f"Starting data extraction from: {filepath}")
        
        # Validate file exists and has correct structure
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Source file not found: {filepath}")
        
        if not self._csv_loader.validate_csv_structure(filepath):
            raise ValueError(f"Invalid CSV structure in file: {filepath}")
        
        # Extract raw data
        raw_records = self._csv_loader.load_income_data(filepath)
        logger.info(f"Extracted {len(raw_records)} raw records")
        
        # Validate data quality
        quality_issues = self._quality_service.validate_records(raw_records)
        
        # Log quality issues
        total_issues = sum(len(issues) for issues in quality_issues.values())
        if total_issues > 0:
            logger.warning(f"Found {total_issues} data quality issues:")
            for issue_type, issues in quality_issues.items():
                if issues:
                    logger.warning(f"  {issue_type}: {len(issues)} records")
        
        # Clean data
        cleaned_records = self._quality_service.clean_records(raw_records)
        logger.info(f"Cleaned data: {len(cleaned_records)} valid records")
        
        return cleaned_records


class TransformDataUseCase:
    """
    Use case for transforming and analyzing income data.
    """
    
    def __init__(self):
        """Initialize transform use case with domain services."""
        self._analysis_service = IncomeAnalysisService()
        self._trend_service = TrendAnalysisService()
    
    def execute(self, records: List[IncomeRecord]) -> Dict[str, Any]:
        """
        Transform data and perform analysis.
        
        Args:
            records: List of cleaned income records
            
        Returns:
            Dictionary containing analysis results
        """
        logger.info("Starting data transformation and analysis")
        
        if not records:
            raise ValueError("No records provided for transformation")
        
        # Perform gender gap analysis
        gender_analyses = self._analysis_service.calculate_gender_gap_by_year(records)
        logger.info(f"Calculated gender gap for {len(gender_analyses)} years")
        
        # Perform trend analysis for each gender
        trend_analyses = {}
        for gender in ['_T', 'M', 'F']:
            gender_records = [r for r in records if r.gender.value == gender]
            if gender_records:
                from domain.entities import Gender
                trend = self._trend_service.calculate_income_trend(
                    gender_records, 
                    Gender.from_code(gender)
                )
                trend_analyses[gender] = trend
        
        logger.info(f"Calculated trends for {len(trend_analyses)} gender categories")
        
        # Calculate summary statistics
        summary_stats = self._calculate_summary_statistics(records)
        
        # Package results
        results = {
            'gender_analyses': gender_analyses,
            'trend_analyses': trend_analyses,
            'summary_statistics': summary_stats,
            'total_records': len(records),
            'year_range': {
                'start': min(r.year for r in records),
                'end': max(r.year for r in records)
            }
        }
        
        logger.info("Data transformation completed successfully")
        return results
    
    def _calculate_summary_statistics(self, records: List[IncomeRecord]) -> Dict[str, Any]:
        """Calculate summary statistics for the dataset."""
        total_records = [r for r in records if r.gender.value == '_T']
        male_records = [r for r in records if r.gender.value == 'M']
        female_records = [r for r in records if r.gender.value == 'F']
        
        def calc_stats(record_list):
            if not record_list:
                return {}
            values = [r.value for r in record_list]
            return {
                'mean': sum(values) / len(values),
                'min': min(values),
                'max': max(values),
                'count': len(values)
            }
        
        return {
            'total_population': calc_stats(total_records),
            'male_population': calc_stats(male_records),
            'female_population': calc_stats(female_records)
        }


class LoadDataUseCase:
    """
    Use case for loading transformed data into storage and generating outputs.
    """
    
    def __init__(self, 
                 repository: IncomeDataRepository,
                 export_repository: DataExportRepository,
                 visualization_service: IncomeVisualizationService):
        """
        Initialize load use case.
        
        Args:
            repository: Income data repository
            export_repository: Data export repository  
            visualization_service: Visualization service
        """
        self._repository = repository
        self._export_repository = export_repository
        self._visualization_service = visualization_service
    
    def execute(self, 
                records: List[IncomeRecord], 
                analysis_results: Dict[str, Any],
                output_formats: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Load data into storage and generate outputs.
        
        Args:
            records: List of income records
            analysis_results: Analysis results from transform phase
            output_formats: List of desired output formats
            
        Returns:
            Dictionary with paths to generated files
        """
        logger.info("Starting data loading and output generation")
        
        output_formats = output_formats or ['csv', 'excel', 'charts']
        generated_files = {}
        
        # Save to database
        success = self._repository.save_records(records)
        if success:
            logger.info("Successfully saved records to database")
        else:
            logger.error("Failed to save records to database")
        
        # Generate exports
        if 'csv' in output_formats:
            csv_path = "docs/outputs/income_data_processed.csv"
            if self._export_repository.export_to_csv(records, csv_path):
                generated_files['csv'] = csv_path
                logger.info(f"CSV export saved: {csv_path}")
        
        if 'excel' in output_formats:
            excel_path = "docs/outputs/income_data_processed.xlsx"
            if self._export_repository.export_to_excel(records, excel_path):
                generated_files['excel'] = excel_path
                logger.info(f"Excel export saved: {excel_path}")
        
        # Export analysis results
        analysis_path = "docs/outputs/analysis_results.json"
        if self._export_repository.export_analysis_results(analysis_results, analysis_path):
            generated_files['analysis'] = analysis_path
            logger.info(f"Analysis results saved: {analysis_path}")
        
        # Generate visualizations
        if 'charts' in output_formats:
            chart_paths = self._generate_visualizations(records, analysis_results)
            generated_files.update(chart_paths)
        
        logger.info(f"Data loading completed. Generated {len(generated_files)} output files")
        return generated_files
    
    def _generate_visualizations(self, 
                               records: List[IncomeRecord], 
                               analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate visualization charts."""
        chart_paths = {}
        
        try:
            # Income trend chart
            trend_path = self._visualization_service.create_income_trend_chart(records)
            chart_paths['trend_chart'] = trend_path
            
            # Gender gap chart
            if 'gender_analyses' in analysis_results:
                gap_path = self._visualization_service.create_gender_gap_chart(
                    analysis_results['gender_analyses']
                )
                chart_paths['gap_chart'] = gap_path
            
            # Income comparison chart
            comparison_path = self._visualization_service.create_comparison_chart(records)
            chart_paths['comparison_chart'] = comparison_path
            
            logger.info(f"Generated {len(chart_paths)} visualization charts")
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {str(e)}")
        
        return chart_paths


class FullETLPipelineUseCase:
    """
    Complete ETL pipeline orchestrator.
    Coordinates all ETL phases following the Facade pattern.
    """
    
    def __init__(self,
                 extract_use_case: ExtractDataUseCase,
                 transform_use_case: TransformDataUseCase,
                 load_use_case: LoadDataUseCase):
        """
        Initialize full ETL pipeline.
        
        Args:
            extract_use_case: Extract phase use case
            transform_use_case: Transform phase use case
            load_use_case: Load phase use case
        """
        self._extract_use_case = extract_use_case
        self._transform_use_case = transform_use_case
        self._load_use_case = load_use_case
    
    def execute(self, 
                source_filepath: str,
                output_formats: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute complete ETL pipeline.
        
        Args:
            source_filepath: Path to source data file
            output_formats: List of desired output formats
            
        Returns:
            Dictionary with pipeline results and generated files
        """
        logger.info("Starting full ETL pipeline execution")
        
        try:
            # Extract phase
            logger.info("=== EXTRACT PHASE ===")
            records = self._extract_use_case.execute(source_filepath)
            
            # Transform phase
            logger.info("=== TRANSFORM PHASE ===")
            analysis_results = self._transform_use_case.execute(records)
            
            # Load phase
            logger.info("=== LOAD PHASE ===")
            generated_files = self._load_use_case.execute(
                records, 
                analysis_results, 
                output_formats
            )
            
            # Pipeline results
            pipeline_results = {
                'status': 'success',
                'records_processed': len(records),
                'analysis_results': analysis_results,
                'generated_files': generated_files,
                'execution_summary': {
                    'extract': f"Processed {len(records)} records",
                    'transform': f"Analyzed {len(analysis_results.get('gender_analyses', []))} years",
                    'load': f"Generated {len(generated_files)} output files"
                }
            }
            
            logger.info("ETL pipeline completed successfully")
            return pipeline_results
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e),
                'records_processed': 0,
                'generated_files': {}
            }
