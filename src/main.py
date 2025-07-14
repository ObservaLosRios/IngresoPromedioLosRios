"""
Main ETL Pipeline Runner
Entry point for the income data ETL system.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, List
from loguru import logger
import os
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))

from presentation.di_container import DIContainer


class ETLRunner:
    """
    Main runner for the ETL pipeline.
    Provides command-line interface and orchestrates the entire process.
    """
    
    def __init__(self):
        """Initialize ETL runner."""
        # Load environment variables
        load_dotenv()
        
        # Initialize dependency injection container
        self.container = DIContainer()
        
        # Setup paths
        self.base_path = Path(__file__).parent.parent
        self.data_path = self.base_path / "data"
        self.outputs_path = self.base_path / "outputs"
        
        # Ensure directories exist
        self.data_path.mkdir(exist_ok=True)
        self.outputs_path.mkdir(exist_ok=True)
        (self.data_path / "raw").mkdir(exist_ok=True)
        (self.data_path / "processed").mkdir(exist_ok=True)
    
    def run_full_pipeline(self, 
                         source_file: str,
                         output_formats: Optional[List[str]] = None) -> bool:
        """
        Run the complete ETL pipeline.
        
        Args:
            source_file: Path to source CSV file
            output_formats: List of output formats to generate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 60)
            logger.info("INICIANDO PIPELINE ETL - INGRESOS REGIÓN DE LOS RÍOS")
            logger.info("=" * 60)
            
            # Get ETL pipeline from DI container
            pipeline = self.container.get_full_etl_pipeline()
            
            # Resolve source file path
            source_path = Path(source_file)
            if not source_path.is_absolute():
                source_file = str(self.base_path / source_file)
            
            # Set default output formats
            output_formats = output_formats or ['csv', 'excel', 'charts']
            
            # Execute pipeline
            results = pipeline.execute(source_file, output_formats)
            
            # Display results
            self._display_results(results)
            
            return results['status'] == 'success'
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            return False
        finally:
            # Cleanup resources
            self.container.cleanup()
    
    def _display_results(self, results: dict) -> None:
        """Display pipeline execution results."""
        logger.info("=" * 60)
        logger.info("RESULTADOS DEL PIPELINE ETL")
        logger.info("=" * 60)
        
        if results['status'] == 'success':
            logger.info("✅ Pipeline ejecutado exitosamente")
            logger.info(f"📊 Registros procesados: {results['records_processed']}")
            
            # Display execution summary
            if 'execution_summary' in results:
                summary = results['execution_summary']
                logger.info("📋 Resumen de ejecución:")
                logger.info(f"   • Extract: {summary.get('extract', 'N/A')}")
                logger.info(f"   • Transform: {summary.get('transform', 'N/A')}")
                logger.info(f"   • Load: {summary.get('load', 'N/A')}")
            
            # Display generated files
            if 'generated_files' in results and results['generated_files']:
                logger.info("📁 Archivos generados:")
                for file_type, file_path in results['generated_files'].items():
                    logger.info(f"   • {file_type}: {file_path}")
            
            # Display analysis insights
            if 'analysis_results' in results:
                self._display_analysis_insights(results['analysis_results'])
                
        else:
            logger.error("❌ Pipeline falló")
            if 'error' in results:
                logger.error(f"Error: {results['error']}")
    
    def _display_analysis_insights(self, analysis_results: dict) -> None:
        """Display key insights from analysis."""
        logger.info("🔍 Principales hallazgos:")
        
        # Gender gap insights
        if 'gender_analyses' in analysis_results:
            gender_analyses = analysis_results['gender_analyses']
            if gender_analyses:
                latest_analysis = max(gender_analyses, key=lambda x: x.year)
                gap_percentage = latest_analysis.gender_gap_percentage
                
                logger.info(f"   • Brecha salarial {latest_analysis.year}: {gap_percentage:.1f}%")
                if gap_percentage > 0:
                    logger.info("   • Los hombres ganan más que las mujeres")
                else:
                    logger.info("   • Las mujeres ganan más que los hombres")
        
        # Trend insights
        if 'trend_analyses' in analysis_results:
            trends = analysis_results['trend_analyses']
            if '_T' in trends:  # Total population trend
                total_trend = trends['_T']
                logger.info(f"   • Crecimiento promedio anual: {total_trend.average_annual_growth:.1f}%")
                logger.info(f"   • Tendencia general: {total_trend.trend_direction}")
        
        # Summary statistics
        if 'summary_statistics' in analysis_results:
            stats = analysis_results['summary_statistics']
            if 'total_population' in stats and stats['total_population']:
                total_stats = stats['total_population']
                logger.info(f"   • Ingreso promedio histórico: ${total_stats['mean']:,.0f}")
                logger.info(f"   • Rango: ${total_stats['min']:,.0f} - ${total_stats['max']:,.0f}")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ETL Pipeline para Análisis de Ingresos - Región de Los Ríos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py IngresoPromedio.csv
  python main.py data/raw/IngresoPromedio.csv --output csv excel
  python main.py IngresoPromedio.csv --output charts --verbose
        """
    )
    
    parser.add_argument(
        'source_file',
        help='Archivo CSV con datos de ingresos'
    )
    
    parser.add_argument(
        '--output', '-o',
        nargs='*',
        choices=['csv', 'excel', 'charts', 'all'],
        default=['csv', 'excel', 'charts'],
        help='Formatos de salida a generar (default: todos)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada de ejecución'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='ETL Pipeline v1.0.0'
    )
    
    return parser


def main():
    """Main entry point."""
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Set log level based on verbosity
    if args.verbose:
        os.environ['LOG_LEVEL'] = 'DEBUG'
    
    # Handle 'all' output format
    if 'all' in args.output:
        args.output = ['csv', 'excel', 'charts']
    
    # Create and run ETL pipeline
    runner = ETLRunner()
    success = runner.run_full_pipeline(args.source_file, args.output)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
