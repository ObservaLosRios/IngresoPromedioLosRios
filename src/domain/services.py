"""
Domain services for business logic.
Following Single Responsibility Principle from SOLID.
"""

from typing import List, Dict, Any
import numpy as np
from .entities import IncomeRecord, IncomeAnalysis, TrendAnalysis, Gender


class IncomeAnalysisService:
    """
    Service for income data analysis operations.
    Contains pure business logic without external dependencies.
    """
    
    def calculate_gender_gap_by_year(self, records: List[IncomeRecord]) -> List[IncomeAnalysis]:
        """
        Calculate gender income gap for each year.
        
        Args:
            records: List of income records
            
        Returns:
            List of income analysis results by year
        """
        analyses = []
        years = sorted(set(record.year for record in records))
        
        for year in years:
            year_records = [r for r in records if r.year == year]
            
            male_income = self._get_income_by_gender(year_records, Gender.MALE)
            female_income = self._get_income_by_gender(year_records, Gender.FEMALE)
            total_income = self._get_income_by_gender(year_records, Gender.BOTH)
            
            if male_income and female_income:
                gap = male_income - female_income
                gap_percentage = (gap / female_income) * 100 if female_income > 0 else 0
                
                analysis = IncomeAnalysis(
                    year=year,
                    male_income=male_income,
                    female_income=female_income,
                    total_income=total_income or 0,
                    gender_gap=gap,
                    gender_gap_percentage=gap_percentage
                )
                analyses.append(analysis)
        
        return analyses
    
    def _get_income_by_gender(self, records: List[IncomeRecord], gender: Gender) -> float:
        """Get income value for specific gender."""
        for record in records:
            if record.gender == gender:
                return record.value
        return 0.0


class TrendAnalysisService:
    """
    Service for trend analysis operations.
    """
    
    def calculate_income_trend(self, records: List[IncomeRecord], gender: Gender = Gender.BOTH) -> TrendAnalysis:
        """
        Calculate income trend for specified gender.
        
        Args:
            records: List of income records
            gender: Gender to analyze (default: both sexes)
            
        Returns:
            Trend analysis results
        """
        filtered_records = [r for r in records if r.gender == gender]
        if not filtered_records:
            raise ValueError(f"No records found for gender: {gender}")
        
        # Sort by year
        sorted_records = sorted(filtered_records, key=lambda x: x.year)
        
        years = [r.year for r in sorted_records]
        values = [r.value for r in sorted_records]
        
        # Calculate metrics
        start_year = min(years)
        end_year = max(years)
        
        initial_value = values[0]
        final_value = values[-1]
        
        # Growth rate calculation
        periods = end_year - start_year
        growth_rate = ((final_value / initial_value) - 1) * 100 if periods > 0 else 0
        average_annual_growth = growth_rate / periods if periods > 0 else 0
        
        # Volatility (standard deviation of year-over-year changes)
        if len(values) > 1:
            yoy_changes = [(values[i] - values[i-1]) / values[i-1] * 100 
                          for i in range(1, len(values))]
            volatility = np.std(yoy_changes)
        else:
            volatility = 0
        
        trend_direction = "Creciente" if growth_rate > 0 else "Decreciente"
        
        return TrendAnalysis(
            start_year=start_year,
            end_year=end_year,
            growth_rate=growth_rate,
            average_annual_growth=average_annual_growth,
            volatility=volatility,
            trend_direction=trend_direction
        )
    
    def identify_outliers(self, records: List[IncomeRecord], threshold: float = 2.0) -> List[IncomeRecord]:
        """
        Identify outlier records using statistical methods.
        
        Args:
            records: List of income records
            threshold: Z-score threshold for outlier detection
            
        Returns:
            List of outlier records
        """
        if not records:
            return []
        
        values = [r.value for r in records]
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        outliers = []
        for record in records:
            if std_value > 0:
                z_score = abs((record.value - mean_value) / std_value)
                if z_score > threshold:
                    outliers.append(record)
        
        return outliers


class DataQualityService:
    """
    Service for data quality validation and cleaning.
    """
    
    def validate_records(self, records: List[IncomeRecord]) -> Dict[str, Any]:
        """
        Validate income records for data quality issues.
        
        Args:
            records: List of income records to validate
            
        Returns:
            Dictionary with validation results
        """
        issues = {
            "missing_values": [],
            "duplicates": [],
            "inconsistencies": [],
            "outliers": []
        }
        
        seen_records = set()
        
        for record in records:
            # Check for duplicates
            record_key = (record.year, record.gender.value, record.region_code)
            if record_key in seen_records:
                issues["duplicates"].append(record)
            else:
                seen_records.add(record_key)
            
            # Check for missing or invalid values
            if record.value <= 0:
                issues["missing_values"].append(record)
        
        # Use trend service to identify outliers
        trend_service = TrendAnalysisService()
        issues["outliers"] = trend_service.identify_outliers(records)
        
        return issues
    
    def clean_records(self, records: List[IncomeRecord]) -> List[IncomeRecord]:
        """
        Clean income records by removing duplicates and invalid entries.
        
        Args:
            records: List of income records to clean
            
        Returns:
            List of cleaned records
        """
        cleaned_records = []
        seen_keys = set()
        
        for record in records:
            record_key = (record.year, record.gender.value, record.region_code)
            
            # Remove duplicates and invalid records
            if (record_key not in seen_keys and 
                record.value > 0 and 
                record.year >= 2000):
                
                cleaned_records.append(record)
                seen_keys.add(record_key)
        
        return cleaned_records
