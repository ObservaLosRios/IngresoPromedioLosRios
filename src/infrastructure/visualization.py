"""
Economist-style visualization system.
Creates elegant charts with The Economist magazine styling.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from loguru import logger

from domain.entities import IncomeRecord, IncomeAnalysis, TrendAnalysis, Gender


class EconomistStyler:
    """
    The Economist magazine style configuration and utilities.
    Implements elegant, professional chart styling.
    """
    
    # The Economist color palette
    COLORS = {
        'primary': '#E3120B',      # Economist red
        'secondary': '#0D4F8C',    # Deep blue
        'tertiary': '#9C8AA5',     # Light purple
        'accent': '#F39C12',       # Orange
        'success': '#27AE60',      # Green
        'warning': '#E67E22',      # Dark orange
        'text': '#2C3E50',         # Dark grey
        'light_text': '#7F8C8D',   # Light grey
        'background': '#FFFFFF',   # White
        'grid': '#ECF0F1'          # Very light grey
    }
    
    # Typography settings
    FONTS = {
        'title': {'family': 'serif', 'size': 16, 'weight': 'bold'},
        'subtitle': {'family': 'serif', 'size': 12, 'weight': 'normal'},
        'axis_label': {'family': 'sans-serif', 'size': 10, 'weight': 'normal'},
        'tick_label': {'family': 'sans-serif', 'size': 9, 'weight': 'normal'},
        'annotation': {'family': 'sans-serif', 'size': 8, 'style': 'italic'}
    }
    
    @classmethod
    def setup_matplotlib_style(cls) -> None:
        """Configure matplotlib with Economist-style defaults."""
        plt.style.use('default')  # Reset to default first
        
        # Set global font
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman', 'serif']
        plt.rcParams['font.sans-serif'] = ['Arial', 'sans-serif']
        
        # Figure and axes settings
        plt.rcParams['figure.facecolor'] = cls.COLORS['background']
        plt.rcParams['axes.facecolor'] = cls.COLORS['background']
        plt.rcParams['axes.edgecolor'] = cls.COLORS['grid']
        plt.rcParams['axes.linewidth'] = 0.5
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        plt.rcParams['axes.spines.left'] = True
        plt.rcParams['axes.spines.bottom'] = True
        
        # Grid settings
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.grid.axis'] = 'y'
        plt.rcParams['grid.color'] = cls.COLORS['grid']
        plt.rcParams['grid.linewidth'] = 0.5
        plt.rcParams['grid.alpha'] = 0.7
        
        # Text settings
        plt.rcParams['text.color'] = cls.COLORS['text']
        plt.rcParams['axes.labelcolor'] = cls.COLORS['text']
        plt.rcParams['xtick.color'] = cls.COLORS['light_text']
        plt.rcParams['ytick.color'] = cls.COLORS['light_text']
        
        # Legend settings
        plt.rcParams['legend.frameon'] = False
        plt.rcParams['legend.fontsize'] = 9
    
    @classmethod
    def add_economist_title(cls, ax: plt.Axes, title: str, subtitle: str = None) -> None:
        """
        Add Economist-style title with decorative line.
        
        Args:
            ax: Matplotlib axes object
            title: Main title text
            subtitle: Optional subtitle text
        """
        # Title positioning
        title_y = 1.08
        subtitle_y = 1.03
        
        # Main title
        ax.text(0.15, title_y, title, 
               transform=ax.transAxes,
               fontsize=cls.FONTS['title']['size'],
               fontweight=cls.FONTS['title']['weight'],
               fontfamily=cls.FONTS['title']['family'],
               color=cls.COLORS['text'])
        
        # Decorative line (The Economist signature style)
        line_start = 0.15
        line_end = 0.95
        line_y = title_y - 0.02
        
        ax.plot([line_start, line_end], [line_y, line_y], 
               transform=ax.transAxes,
               color=cls.COLORS['primary'], 
               linewidth=2, 
               solid_capstyle='round')
        
        # Subtitle if provided
        if subtitle:
            ax.text(0.15, subtitle_y, subtitle,
                   transform=ax.transAxes,
                   fontsize=cls.FONTS['subtitle']['size'],
                   fontweight=cls.FONTS['subtitle']['weight'],
                   fontfamily=cls.FONTS['subtitle']['family'],
                   color=cls.COLORS['light_text'],
                   style='italic')
    
    @classmethod
    def format_currency_axis(cls, ax: plt.Axes, axis: str = 'y') -> None:
        """
        Format axis to display currency values in thousands/millions.
        
        Args:
            ax: Matplotlib axes object
            axis: Which axis to format ('x' or 'y')
        """
        def currency_formatter(x, pos):
            """Format currency values."""
            if x >= 1000000:
                return f'${x/1000000:.1f}M'
            elif x >= 1000:
                return f'${x/1000:.0f}k'
            else:
                return f'${x:.0f}'
        
        if axis == 'y':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(currency_formatter))
        else:
            ax.xaxis.set_major_formatter(plt.FuncFormatter(currency_formatter))
    
    @classmethod
    def add_source_note(cls, fig: plt.Figure, source: str) -> None:
        """
        Add source note at the bottom of the figure.
        
        Args:
            fig: Matplotlib figure object
            source: Source text
        """
        fig.text(0.15, 0.02, f"Fuente: {source}",
                fontsize=cls.FONTS['annotation']['size'],
                fontfamily=cls.FONTS['annotation']['family'],
                color=cls.COLORS['light_text'],
                style=cls.FONTS['annotation']['style'])


class IncomeVisualizationService:
    """
    Service for creating income data visualizations.
    Follows Single Responsibility Principle.
    """
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize visualization service.
        
        Args:
            output_dir: Directory for saving charts
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styler = EconomistStyler()
        self.styler.setup_matplotlib_style()
    
    def create_income_trend_chart(self, records: List[IncomeRecord], 
                                title: str = None, 
                                subtitle: str = None) -> str:
        """
        Create income trend line chart.
        
        Args:
            records: List of income records
            title: Chart title
            subtitle: Chart subtitle
            
        Returns:
            Path to saved chart file
        """
        # Prepare data
        df_data = []
        for record in records:
            df_data.append({
                'Año': record.year,
                'Ingreso': record.value,
                'Sexo': record.gender.display_name()
            })
        
        import pandas as pd
        df = pd.DataFrame(df_data)
        
        # Create figure with proper size and margins
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
        
        # Plot lines for each gender
        colors = {
            'Hombres': self.styler.COLORS['primary'],
            'Mujeres': self.styler.COLORS['secondary'],
            'Ambos sexos': self.styler.COLORS['tertiary']
        }
        
        for gender in df['Sexo'].unique():
            gender_data = df[df['Sexo'] == gender].sort_values('Año')
            ax.plot(gender_data['Año'], gender_data['Ingreso'],
                   color=colors.get(gender, self.styler.COLORS['accent']),
                   linewidth=2.5,
                   marker='o',
                   markersize=4,
                   label=gender,
                   markerfacecolor='white',
                   markeredgewidth=2)
        
        # Styling
        self.styler.add_economist_title(
            ax, 
            title or "Evolución del Ingreso Promedio",
            subtitle or "Región de Los Ríos, Chile"
        )
        
        # Axis formatting
        ax.set_xlabel('Año', **self.styler.FONTS['axis_label'])
        ax.set_ylabel('Ingreso Promedio (CLP)', **self.styler.FONTS['axis_label'])
        self.styler.format_currency_axis(ax, 'y')
        
        # Legend
        ax.legend(loc='upper left', frameon=False, fontsize=10)
        
        # Grid customization
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Source note
        self.styler.add_source_note(fig, "Instituto Nacional de Estadísticas (INE)")
        
        # Save chart
        filename = "income_trend_chart.png"
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        logger.info(f"Income trend chart saved: {filepath}")
        return str(filepath)
    
    def create_gender_gap_chart(self, analyses: List[IncomeAnalysis],
                              title: str = None,
                              subtitle: str = None) -> str:
        """
        Create gender income gap visualization.
        
        Args:
            analyses: List of income analysis results
            title: Chart title
            subtitle: Chart subtitle
            
        Returns:
            Path to saved chart file
        """
        # Prepare data
        years = [a.year for a in analyses]
        gap_percentages = [a.gender_gap_percentage for a in analyses]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
        
        # Create bar chart
        bars = ax.bar(years, gap_percentages,
                     color=self.styler.COLORS['primary'],
                     alpha=0.8,
                     edgecolor=self.styler.COLORS['primary'],
                     linewidth=1)
        
        # Add value labels on bars
        for bar, value in zip(bars, gap_percentages):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{value:.1f}%',
                   ha='center', va='bottom',
                   fontsize=9,
                   color=self.styler.COLORS['text'])
        
        # Styling
        self.styler.add_economist_title(
            ax,
            title or "Brecha Salarial de Género",
            subtitle or "Diferencia porcentual entre ingresos de hombres y mujeres"
        )
        
        # Axis formatting
        ax.set_xlabel('Año', **self.styler.FONTS['axis_label'])
        ax.set_ylabel('Brecha Salarial (%)', **self.styler.FONTS['axis_label'])
        
        # Add horizontal line at 0
        ax.axhline(y=0, color=self.styler.COLORS['text'], 
                  linestyle='-', linewidth=0.5, alpha=0.7)
        
        # Grid and spines
        ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_axisbelow(True)
        
        # Source note
        self.styler.add_source_note(fig, "Instituto Nacional de Estadísticas (INE)")
        
        # Save chart
        filename = "gender_gap_chart.png"
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        logger.info(f"Gender gap chart saved: {filepath}")
        return str(filepath)
    
    def create_comparison_chart(self, records: List[IncomeRecord],
                              title: str = None,
                              subtitle: str = None) -> str:
        """
        Create income comparison chart between genders.
        
        Args:
            records: List of income records
            title: Chart title
            subtitle: Chart subtitle
            
        Returns:
            Path to saved chart file
        """
        # Prepare data for latest year
        latest_year = max(record.year for record in records)
        latest_records = [r for r in records if r.year == latest_year and r.gender != Gender.BOTH]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.15)
        
        # Data for chart
        genders = [r.gender.display_name() for r in latest_records]
        values = [r.value for r in latest_records]
        colors = [self.styler.COLORS['primary'], self.styler.COLORS['secondary']]
        
        # Create horizontal bar chart
        bars = ax.barh(genders, values, color=colors, alpha=0.8)
        
        # Add value labels
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax.text(width + 10000, bar.get_y() + bar.get_height()/2,
                   f'${value:,.0f}',
                   ha='left', va='center',
                   fontsize=11,
                   fontweight='bold',
                   color=self.styler.COLORS['text'])
        
        # Styling
        self.styler.add_economist_title(
            ax,
            title or f"Comparación de Ingresos por Género ({latest_year})",
            subtitle or "Ingreso promedio mensual en pesos chilenos"
        )
        
        # Axis formatting
        ax.set_xlabel('Ingreso Promedio (CLP)', **self.styler.FONTS['axis_label'])
        self.styler.format_currency_axis(ax, 'x')
        
        # Grid and spines
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_axisbelow(True)
        
        # Source note
        self.styler.add_source_note(fig, "Instituto Nacional de Estadísticas (INE)")
        
        # Save chart
        filename = "income_comparison_chart.png"
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        logger.info(f"Income comparison chart saved: {filepath}")
        return str(filepath)
