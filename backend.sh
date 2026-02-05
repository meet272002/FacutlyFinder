set -e

echo "Running scraper..."
python -m scrape.dau.main.py

echo "Initializing database..."
python main.py &

echo "Starting FastAPI..."
uvicorn FastAPI:app --host 0.0.0.0 --port $PORT
