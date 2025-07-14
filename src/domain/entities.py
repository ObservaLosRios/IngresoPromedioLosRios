"""
Domain entities for income data processing.
Following Clean Architecture principles and SOLID design patterns.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime


class Gender(Enum):
    """Gender enumeration for type safety."""
    MALE = "M"
    FEMALE = "F"
    BOTH = "_T"
    
    @classmethod
    def from_code(cls, code: str) -> 'Gender':
        """Create Gender from code with validation."""
        mapping = {
            "M": cls.MALE,
            "F": cls.FEMALE,
            "_T": cls.BOTH
        }
        if code not in mapping:
            raise ValueError(f"Invalid gender code: {code}")
        return mapping[code]
    
    def display_name(self) -> str:
        """Get human-readable gender name."""
        mapping = {
            self.MALE: "Hombres",
            self.FEMALE: "Mujeres", 
            self.BOTH: "Ambos sexos"
        }
        return mapping[self]


@dataclass(frozen=True)
class IncomeRecord:
    """
    Immutable income record entity.
    Represents a single income data point with strong typing.
    """
    indicator: str
    year: int
    region_code: str
    region_name: str
    gender: Gender
    value: float
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate income record data."""
        if self.year < 2000 or self.year > 2030:
            raise ValueError(f"Invalid year: {self.year}")
        
        if self.value < 0:
            raise ValueError(f"Income value cannot be negative: {self.value}")
        
        if not self.region_name:
            raise ValueError("Region name cannot be empty")
    
    @property
    def formatted_value(self) -> str:
        """Format income value as currency."""
        return f"${self.value:,.2f}"
    
    @property
    def is_total_population(self) -> bool:
        """Check if record represents total population."""
        return self.gender == Gender.BOTH


@dataclass(frozen=True)
class IncomeAnalysis:
    """
    Value object for income analysis results.
    """
    year: int
    male_income: float
    female_income: float
    total_income: float
    gender_gap: float
    gender_gap_percentage: float
    
    @property
    def gap_direction(self) -> str:
        """Determine if gap favors males or females."""
        return "Hombres" if self.gender_gap > 0 else "Mujeres"


@dataclass(frozen=True)
class TrendAnalysis:
    """
    Value object for trend analysis results.
    """
    start_year: int
    end_year: int
    growth_rate: float
    average_annual_growth: float
    volatility: float
    trend_direction: str
    
    @property
    def period_description(self) -> str:
        """Get human-readable period description."""
        return f"{self.start_year}-{self.end_year}"
