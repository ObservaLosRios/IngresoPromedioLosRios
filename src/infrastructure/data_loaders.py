"""
CSV data loader implementation.
Following Open/Closed Principle from SOLID.
"""

import pandas as pd
from typing import List, Optional
from pathlib import Path
from loguru import logger

from domain.entities import IncomeRecord, Gender


class CSVDataLoader:
    """
    Concrete implementation for loading data from CSV files.
    Handles CSV-specific parsing and validation.
    """
    
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        """
        Initialize CSV loader with configuration.
        
        Args:
            encoding: File encoding (default: utf-8)
            delimiter: CSV delimiter (default: comma)
        """
        self._encoding = encoding
        self._delimiter = delimiter
    
    def load_income_data(self, filepath: str) -> List[IncomeRecord]:
        """
        Load income data from CSV file.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of IncomeRecord entities
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If data format is invalid
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        logger.info(f"Loading income data from: {filepath}")
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(
                filepath,
                encoding=self._encoding,
                delimiter=self._delimiter
            )
            
            # Validate required columns
            required_columns = ['Año', 'DTI_CL_SEXO', 'Sexo', 'DTI_CL_REGION', 'Región', 'Value', 'Indicador']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert to domain entities
            records = self._convert_to_entities(df)
            
            logger.info(f"Successfully loaded {len(records)} income records")
            return records
            
        except Exception as e:
            logger.error(f"Error loading CSV data: {str(e)}")
            raise
    
    def _convert_to_entities(self, df: pd.DataFrame) -> List[IncomeRecord]:
        """
        Convert pandas DataFrame to IncomeRecord entities.
        
        Args:
            df: Pandas DataFrame with income data
            
        Returns:
            List of IncomeRecord entities
        """
        records = []
        
        for _, row in df.iterrows():
            try:
                # Parse gender with validation
                gender = Gender.from_code(row['DTI_CL_SEXO'])
                
                # Create IncomeRecord entity
                record = IncomeRecord(
                    indicator=str(row['Indicador']),
                    year=int(row['Año']),
                    region_code=str(row['DTI_CL_REGION']),
                    region_name=str(row['Región']),
                    gender=gender,
                    value=float(row['Value'])
                )
                
                records.append(record)
                
            except (ValueError, KeyError) as e:
                logger.warning(f"Skipping invalid record: {str(e)}")
                continue
        
        return records
    
    def validate_csv_structure(self, filepath: str) -> bool:
        """
        Validate CSV file structure without loading all data.
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            True if structure is valid, False otherwise
        """
        try:
            # Read only first few rows for validation
            df_sample = pd.read_csv(
                filepath,
                encoding=self._encoding,
                delimiter=self._delimiter,
                nrows=5
            )
            
            required_columns = ['Año', 'DTI_CL_SEXO', 'Sexo', 'DTI_CL_REGION', 'Región', 'Value', 'Indicador']
            return all(col in df_sample.columns for col in required_columns)
            
        except Exception as e:
            logger.error(f"CSV validation failed: {str(e)}")
            return False


class ExcelDataLoader:
    """
    Concrete implementation for loading data from Excel files.
    Demonstrates Open/Closed Principle - extending functionality without modifying existing code.
    """
    
    def __init__(self, sheet_name: str = 'Sheet1'):
        """
        Initialize Excel loader.
        
        Args:
            sheet_name: Name of the Excel sheet to read
        """
        self._sheet_name = sheet_name
    
    def load_income_data(self, filepath: str) -> List[IncomeRecord]:
        """
        Load income data from Excel file.
        
        Args:
            filepath: Path to Excel file
            
        Returns:
            List of IncomeRecord entities
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {filepath}")
        
        logger.info(f"Loading income data from Excel: {filepath}")
        
        try:
            # Read Excel with pandas
            df = pd.read_excel(filepath, sheet_name=self._sheet_name)
            
            # Reuse CSV conversion logic (DRY principle)
            csv_loader = CSVDataLoader()
            records = csv_loader._convert_to_entities(df)
            
            logger.info(f"Successfully loaded {len(records)} records from Excel")
            return records
            
        except Exception as e:
            logger.error(f"Error loading Excel data: {str(e)}")
            raise
