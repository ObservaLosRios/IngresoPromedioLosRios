"""
Repository implementations for data persistence.
Following Dependency Inversion and Interface Segregation principles.
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from loguru import logger

from domain.repositories import IncomeDataRepository, DataExportRepository
from domain.entities import IncomeRecord, Gender


class SQLiteIncomeRepository(IncomeDataRepository):
    """
    SQLite implementation of IncomeDataRepository.
    Provides persistent storage for income data.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize SQLite repository.
        
        Args:
            db_path: Path to SQLite database file
        """
        self._db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database tables if they don't exist."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS income_records (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        indicator TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        region_code TEXT NOT NULL,
                        region_name TEXT NOT NULL,
                        gender TEXT NOT NULL,
                        value REAL NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(year, region_code, gender)
                    )
                """)
                conn.commit()
                logger.info(f"Database initialized: {self._db_path}")
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
    
    def save_records(self, records: List[IncomeRecord]) -> bool:
        """
        Save income records to SQLite database.
        
        Args:
            records: List of IncomeRecord entities
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                
                for record in records:
                    cursor.execute("""
                        INSERT OR REPLACE INTO income_records 
                        (indicator, year, region_code, region_name, gender, value)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        record.indicator,
                        record.year,
                        record.region_code,
                        record.region_name,
                        record.gender.value,
                        record.value
                    ))
                
                conn.commit()
                logger.info(f"Saved {len(records)} records to database")
                return True
                
        except Exception as e:
            logger.error(f"Failed to save records: {str(e)}")
            return False
    
    def get_records_by_year(self, year: int) -> List[IncomeRecord]:
        """Get records for a specific year."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT indicator, year, region_code, region_name, gender, value
                    FROM income_records 
                    WHERE year = ?
                    ORDER BY gender
                """, (year,))
                
                rows = cursor.fetchall()
                return self._rows_to_entities(rows)
                
        except Exception as e:
            logger.error(f"Failed to get records for year {year}: {str(e)}")
            return []
    
    def get_records_by_year_range(self, start_year: int, end_year: int) -> List[IncomeRecord]:
        """Get records within a year range."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT indicator, year, region_code, region_name, gender, value
                    FROM income_records 
                    WHERE year BETWEEN ? AND ?
                    ORDER BY year, gender
                """, (start_year, end_year))
                
                rows = cursor.fetchall()
                return self._rows_to_entities(rows)
                
        except Exception as e:
            logger.error(f"Failed to get records for range {start_year}-{end_year}: {str(e)}")
            return []
    
    def get_records_by_gender(self, gender: str) -> List[IncomeRecord]:
        """Get records for a specific gender."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT indicator, year, region_code, region_name, gender, value
                    FROM income_records 
                    WHERE gender = ?
                    ORDER BY year
                """, (gender,))
                
                rows = cursor.fetchall()
                return self._rows_to_entities(rows)
                
        except Exception as e:
            logger.error(f"Failed to get records for gender {gender}: {str(e)}")
            return []
    
    def get_all_records(self) -> List[IncomeRecord]:
        """Get all records."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT indicator, year, region_code, region_name, gender, value
                    FROM income_records 
                    ORDER BY year, gender
                """)
                
                rows = cursor.fetchall()
                return self._rows_to_entities(rows)
                
        except Exception as e:
            logger.error(f"Failed to get all records: {str(e)}")
            return []
    
    def _rows_to_entities(self, rows: List[tuple]) -> List[IncomeRecord]:
        """Convert database rows to IncomeRecord entities."""
        records = []
        for row in rows:
            try:
                record = IncomeRecord(
                    indicator=row[0],
                    year=row[1],
                    region_code=row[2],
                    region_name=row[3],
                    gender=Gender.from_code(row[4]),
                    value=row[5]
                )
                records.append(record)
            except ValueError as e:
                logger.warning(f"Skipping invalid database record: {str(e)}")
                continue
        
        return records


class FileDataExportRepository(DataExportRepository):
    """
    File-based implementation of DataExportRepository.
    Handles exporting data to various file formats.
    """
    
    def export_to_csv(self, records: List[IncomeRecord], filepath: str) -> bool:
        """
        Export records to CSV format.
        
        Args:
            records: List of IncomeRecord entities
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to DataFrame
            data = []
            for record in records:
                data.append({
                    'Indicador': record.indicator,
                    'Año': record.year,
                    'Código_Región': record.region_code,
                    'Región': record.region_name,
                    'Sexo': record.gender.display_name(),
                    'Valor': record.value,
                    'Valor_Formateado': record.formatted_value
                })
            
            df = pd.DataFrame(data)
            
            # Ensure output directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Export to CSV
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Exported {len(records)} records to CSV: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export to CSV: {str(e)}")
            return False
    
    def export_to_excel(self, records: List[IncomeRecord], filepath: str) -> bool:
        """
        Export records to Excel format.
        
        Args:
            records: List of IncomeRecord entities
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to DataFrame (reuse CSV logic)
            data = []
            for record in records:
                data.append({
                    'Indicador': record.indicator,
                    'Año': record.year,
                    'Código_Región': record.region_code,
                    'Región': record.region_name,
                    'Sexo': record.gender.display_name(),
                    'Valor': record.value,
                    'Valor_Formateado': record.formatted_value
                })
            
            df = pd.DataFrame(data)
            
            # Ensure output directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Export to Excel with formatting
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Datos_Ingreso', index=False)
                
                # Get workbook and worksheet for formatting
                workbook = writer.book
                worksheet = writer.sheets['Datos_Ingreso']
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            logger.info(f"Exported {len(records)} records to Excel: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export to Excel: {str(e)}")
            return False
    
    def export_analysis_results(self, analysis: Dict[str, Any], filepath: str) -> bool:
        """
        Export analysis results to JSON format.
        
        Args:
            analysis: Analysis results dictionary
            filepath: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            
            # Ensure output directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Export to JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Exported analysis results to: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export analysis results: {str(e)}")
            return False
