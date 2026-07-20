set -e

PORT=8005

# echo "Running scraper..."
# python -m scrape.dau.main

# echo "Initializing database..."
# python main.py

echo "Starting FastAPI..."
uvicorn FastAPI:app --host 0.0.0.0 --port $PORT
