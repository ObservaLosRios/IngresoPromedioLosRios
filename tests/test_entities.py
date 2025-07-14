"""
Unit tests for domain entities.
Ensures business logic correctness.
"""

import pytest
from datetime import datetime
from src.domain.entities import IncomeRecord, Gender, IncomeAnalysis, TrendAnalysis


class TestGender:
    """Test Gender enumeration."""
    
    def test_from_code_valid(self):
        """Test creating Gender from valid codes."""
        assert Gender.from_code("M") == Gender.MALE
        assert Gender.from_code("F") == Gender.FEMALE
        assert Gender.from_code("_T") == Gender.BOTH
    
    def test_from_code_invalid(self):
        """Test creating Gender from invalid code raises ValueError."""
        with pytest.raises(ValueError, match="Invalid gender code"):
            Gender.from_code("X")
    
    def test_display_name(self):
        """Test gender display names."""
        assert Gender.MALE.display_name() == "Hombres"
        assert Gender.FEMALE.display_name() == "Mujeres"
        assert Gender.BOTH.display_name() == "Ambos sexos"


class TestIncomeRecord:
    """Test IncomeRecord entity."""
    
    def test_valid_income_record_creation(self):
        """Test creating a valid income record."""
        record = IncomeRecord(
            indicator="Test indicator",
            year=2020,
            region_code="CHL14",
            region_name="Región de Los Ríos",
            gender=Gender.MALE,
            value=500000.0
        )
        
        assert record.indicator == "Test indicator"
        assert record.year == 2020
        assert record.region_code == "CHL14"
        assert record.region_name == "Región de Los Ríos"
        assert record.gender == Gender.MALE
        assert record.value == 500000.0
    
    def test_invalid_year_raises_error(self):
        """Test that invalid year raises ValueError."""
        with pytest.raises(ValueError, match="Invalid year"):
            IncomeRecord(
                indicator="Test",
                year=1999,  # Invalid year
                region_code="CHL14",
                region_name="Test Region",
                gender=Gender.MALE,
                value=500000.0
            )
    
    def test_negative_value_raises_error(self):
        """Test that negative income value raises ValueError."""
        with pytest.raises(ValueError, match="Income value cannot be negative"):
            IncomeRecord(
                indicator="Test",
                year=2020,
                region_code="CHL14",
                region_name="Test Region",
                gender=Gender.MALE,
                value=-1000.0  # Negative value
            )
    
    def test_empty_region_name_raises_error(self):
        """Test that empty region name raises ValueError."""
        with pytest.raises(ValueError, match="Region name cannot be empty"):
            IncomeRecord(
                indicator="Test",
                year=2020,
                region_code="CHL14",
                region_name="",  # Empty region name
                gender=Gender.MALE,
                value=500000.0
            )
    
    def test_formatted_value(self):
        """Test formatted currency value."""
        record = IncomeRecord(
            indicator="Test",
            year=2020,
            region_code="CHL14",
            region_name="Test Region",
            gender=Gender.MALE,
            value=500000.0
        )
        
        assert record.formatted_value == "$500,000.00"
    
    def test_is_total_population(self):
        """Test total population check."""
        total_record = IncomeRecord(
            indicator="Test",
            year=2020,
            region_code="CHL14",
            region_name="Test Region",
            gender=Gender.BOTH,
            value=500000.0
        )
        
        male_record = IncomeRecord(
            indicator="Test",
            year=2020,
            region_code="CHL14",
            region_name="Test Region",
            gender=Gender.MALE,
            value=500000.0
        )
        
        assert total_record.is_total_population is True
        assert male_record.is_total_population is False


class TestIncomeAnalysis:
    """Test IncomeAnalysis value object."""
    
    def test_gap_direction_male_favored(self):
        """Test gap direction when males earn more."""
        analysis = IncomeAnalysis(
            year=2020,
            male_income=600000.0,
            female_income=500000.0,
            total_income=550000.0,
            gender_gap=100000.0,
            gender_gap_percentage=20.0
        )
        
        assert analysis.gap_direction == "Hombres"
    
    def test_gap_direction_female_favored(self):
        """Test gap direction when females earn more."""
        analysis = IncomeAnalysis(
            year=2020,
            male_income=500000.0,
            female_income=600000.0,
            total_income=550000.0,
            gender_gap=-100000.0,
            gender_gap_percentage=-16.67
        )
        
        assert analysis.gap_direction == "Mujeres"


class TestTrendAnalysis:
    """Test TrendAnalysis value object."""
    
    def test_period_description(self):
        """Test period description formatting."""
        trend = TrendAnalysis(
            start_year=2010,
            end_year=2020,
            growth_rate=25.0,
            average_annual_growth=2.5,
            volatility=5.2,
            trend_direction="Creciente"
        )
        
        assert trend.period_description == "2010-2020"
