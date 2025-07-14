"""
Domain repositories interfaces.
Following Dependency Inversion Principle from SOLID.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .entities import IncomeRecord, IncomeAnalysis, TrendAnalysis


class IncomeDataRepository(ABC):
    """
    Abstract repository for income data operations.
    Defines the contract for data persistence operations.
    """
    
    @abstractmethod
    def save_records(self, records: List[IncomeRecord]) -> bool:
        """Save income records to storage."""
        pass
    
    @abstractmethod
    def get_records_by_year(self, year: int) -> List[IncomeRecord]:
        """Retrieve records for a specific year."""
        pass
    
    @abstractmethod
    def get_records_by_year_range(self, start_year: int, end_year: int) -> List[IncomeRecord]:
        """Retrieve records within a year range."""
        pass
    
    @abstractmethod
    def get_records_by_gender(self, gender: str) -> List[IncomeRecord]:
        """Retrieve records for a specific gender."""
        pass
    
    @abstractmethod
    def get_all_records(self) -> List[IncomeRecord]:
        """Retrieve all records."""
        pass


class DataExportRepository(ABC):
    """
    Abstract repository for data export operations.
    """
    
    @abstractmethod
    def export_to_csv(self, records: List[IncomeRecord], filepath: str) -> bool:
        """Export records to CSV format."""
        pass
    
    @abstractmethod
    def export_to_excel(self, records: List[IncomeRecord], filepath: str) -> bool:
        """Export records to Excel format."""
        pass
    
    @abstractmethod
    def export_analysis_results(self, analysis: Dict[str, Any], filepath: str) -> bool:
        """Export analysis results."""
        pass


class VisualizationRepository(ABC):
    """
    Abstract repository for visualization operations.
    """
    
    @abstractmethod
    def save_chart(self, chart_data: Dict[str, Any], filepath: str) -> bool:
        """Save chart to file."""
        pass
    
    @abstractmethod
    def get_chart_template(self, chart_type: str) -> Dict[str, Any]:
        """Get chart template configuration."""
        pass
