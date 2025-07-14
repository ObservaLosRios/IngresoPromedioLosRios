"""
Dependency Injection Container
Implements Dependency Inversion Principle from SOLID.
"""

import os
from pathlib import Path
from typing import Optional
from loguru import logger

from domain.repositories import IncomeDataRepository, DataExportRepository
from infrastructure.data_loaders import CSVDataLoader
from infrastructure.repositories import SQLiteIncomeRepository, FileDataExportRepository
from infrastructure.visualization import IncomeVisualizationService
from application.use_cases import (
    ExtractDataUseCase, 
    TransformDataUseCase, 
    LoadDataUseCase,
    FullETLPipelineUseCase
)


class DIContainer:
    """
    Dependency Injection Container for managing object creation and lifetime.
    Follows Inversion of Control principle.
    """
    
    def __init__(self, config: Optional[dict] = None):
        """
        Initialize DI container with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self._config = config or self._load_default_config()
        self._instances = {}
        
        # Setup logging
        self._setup_logging()
    
    def _load_default_config(self) -> dict:
        """Load default configuration from environment variables."""
        return {
            'database_path': os.getenv('DATABASE_PATH', 'data/processed/ingreso_promedio.db'),
            'output_path': os.getenv('OUTPUT_PATH', 'outputs'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'log_file': os.getenv('LOG_FILE', 'logs/etl.log')
        }
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_path = Path(self._config['log_file'])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.remove()  # Remove default handler
        
        # Add file handler
        logger.add(
            log_path,
            level=self._config['log_level'],
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            rotation="1 day",
            retention="30 days"
        )
        
        # Add console handler
        logger.add(
            lambda msg: print(msg, end=''),
            level=self._config['log_level'],
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
        )
    
    def get_csv_data_loader(self) -> CSVDataLoader:
        """Get CSV data loader instance."""
        if 'csv_loader' not in self._instances:
            self._instances['csv_loader'] = CSVDataLoader()
        return self._instances['csv_loader']
    
    def get_income_repository(self) -> IncomeDataRepository:
        """Get income data repository instance."""
        if 'income_repository' not in self._instances:
            db_path = self._config['database_path']
            # Ensure database directory exists
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self._instances['income_repository'] = SQLiteIncomeRepository(db_path)
        return self._instances['income_repository']
    
    def get_export_repository(self) -> DataExportRepository:
        """Get data export repository instance."""
        if 'export_repository' not in self._instances:
            self._instances['export_repository'] = FileDataExportRepository()
        return self._instances['export_repository']
    
    def get_visualization_service(self) -> IncomeVisualizationService:
        """Get visualization service instance."""
        if 'visualization_service' not in self._instances:
            output_dir = self._config['output_path']
            self._instances['visualization_service'] = IncomeVisualizationService(output_dir)
        return self._instances['visualization_service']
    
    def get_extract_use_case(self) -> ExtractDataUseCase:
        """Get extract use case instance."""
        if 'extract_use_case' not in self._instances:
            csv_loader = self.get_csv_data_loader()
            self._instances['extract_use_case'] = ExtractDataUseCase(csv_loader)
        return self._instances['extract_use_case']
    
    def get_transform_use_case(self) -> TransformDataUseCase:
        """Get transform use case instance."""
        if 'transform_use_case' not in self._instances:
            self._instances['transform_use_case'] = TransformDataUseCase()
        return self._instances['transform_use_case']
    
    def get_load_use_case(self) -> LoadDataUseCase:
        """Get load use case instance."""
        if 'load_use_case' not in self._instances:
            repository = self.get_income_repository()
            export_repository = self.get_export_repository()
            visualization_service = self.get_visualization_service()
            
            self._instances['load_use_case'] = LoadDataUseCase(
                repository,
                export_repository, 
                visualization_service
            )
        return self._instances['load_use_case']
    
    def get_full_etl_pipeline(self) -> FullETLPipelineUseCase:
        """Get full ETL pipeline use case instance."""
        if 'full_etl_pipeline' not in self._instances:
            extract_use_case = self.get_extract_use_case()
            transform_use_case = self.get_transform_use_case()
            load_use_case = self.get_load_use_case()
            
            self._instances['full_etl_pipeline'] = FullETLPipelineUseCase(
                extract_use_case,
                transform_use_case,
                load_use_case
            )
        return self._instances['full_etl_pipeline']
    
    def cleanup(self) -> None:
        """Cleanup resources and close connections."""
        logger.info("Cleaning up DI container resources")
        
        # Close database connections if any
        if 'income_repository' in self._instances:
            # SQLite connections are automatically closed by context managers
            pass
        
        # Clear instances
        self._instances.clear()
        logger.info("DI container cleanup completed")
