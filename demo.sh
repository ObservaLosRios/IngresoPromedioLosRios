#!/bin/bash

# Quick Demo Script - Income Analysis ETL Pipeline
# =================================================

echo "🚀 Demo: Análisis de Ingresos - Región de Los Ríos"
echo "================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "data/raw/IngresoPromedio.csv" ]; then
    echo "❌ Error: Archivo de datos no encontrado"
    echo "   Asegúrate de estar en el directorio del proyecto"
    exit 1
fi

echo "📊 Ejecutando pipeline ETL completo..."
echo "   - Extrayendo datos del CSV"
echo "   - Transformando y analizando" 
echo "   - Generando visualizaciones estilo The Economist"
echo ""

# Run the ETL pipeline
python src/main.py data/raw/IngresoPromedio.csv

echo ""
echo "🎨 Abriendo visualizaciones generadas..."

# Open the generated charts (macOS)
if command -v open &> /dev/null; then
    open outputs/income_trend_chart.png
    sleep 1
    open outputs/gender_gap_chart.png
    sleep 1
    open outputs/income_comparison_chart.png
fi

echo ""
echo "📁 Archivos generados en outputs/:"
ls -la outputs/

echo ""
echo "✅ Demo completado exitosamente!"
echo "   Revisa los gráficos que se abrieron y los archivos en outputs/"
