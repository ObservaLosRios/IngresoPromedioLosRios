#!/bin/bash

# ETL Pipeline Setup Script
# Sets up the development environment and runs the pipeline

set -e  # Exit on any error

echo "🚀 Setting up Income Analysis ETL Pipeline"
echo "=========================================="

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/raw data/processed outputs logs

# Check if data file exists
DATA_FILE="data/raw/IngresoPromedio.csv"
if [ ! -f "$DATA_FILE" ]; then
    echo "⚠️  Warning: Data file not found at $DATA_FILE"
    echo "   Please ensure the CSV file is in the data/raw/ directory"
    exit 1
fi

echo "✅ Setup completed successfully!"
echo ""
echo "🔥 Running ETL Pipeline..."
echo "=========================="

# Run the ETL pipeline
python src/main.py data/raw/IngresoPromedio.csv --verbose

echo ""
echo "🎉 Pipeline execution completed!"
echo "📊 Check the outputs/ directory for results"
echo "📋 Check the logs/ directory for detailed logs"
