# Faculty Finder

Live Link: https://facutlyfinder-5tnqrfu5mpkdwkvppg2f3x.streamlit.app/

![](./images/Screenshot-1.png)
****
## Objective

Build a data pipeline to crawl, extract, and clean faculty data (names, bios, research interests) from a college website to provide a clean dataset for a semantic search engine.

## Team 

* Team Name: InfoScale
* Team Members:
  1. 202518023 Meet Gandhi
  2. 202518036 Kashyap Patel

## Data Sources

* https://www.daiict.ac.in/faculty

## Process Overview

The project follows a structured, multi-stage data and application pipeline. It begins with the `scrape/dau/` module, which crawls the DAU faculty website to collect faculty profile URLs and detailed information such as names, bios, teaching areas, and research interests. The scraped content is stored as raw CSV files in the `data/` directory.

The raw data is then processed by the `preprocess/` module, which cleans, normalizes, and standardizes the extracted information to ensure consistency across records. After preprocessing, database management is handled in two layers: `dbConnection/` establishes and manages the SQLite database connection, while `dbOperations/` is responsible for creating tables and inserting the processed faculty records into the `faculty_managment.db` database located in the `database/` directory. The root `main.py` orchestrates this end-to-end workflow, from data preparation to database population.

Once the database is ready, the backend service defined in `FastAPI.py` exposes RESTful endpoints that allow client applications to retrieve faculty data in JSON format. These endpoints act as the data access layer for downstream applications.

On the frontend, the Streamlit client implemented in `client/app.py` consumes the FastAPI endpoints to fetch faculty data and provides an interactive semantic search interface. User queries describing research interests are converted into vector embeddings using a pre-trained SentenceTransformer model (`paraphrase-MiniLM-L3-v2`). Faculty profiles—constructed from specializations, teaching areas, and research descriptions—are also embedded into the same vector space. Cosine similarity is then used to rank faculty members based on semantic relevance to the user’s query, and the top matches are displayed along with match scores.

This architecture enables an end-to-end faculty recommendation system, integrating web scraping, data preprocessing, database management, API services, and semantic search into a unified pipeline.

## Folder Structure

```
FacultyFinder/
│
├── client/
│   └── app.py                 # Streamlit frontend
│
├── data/
│   ├── dau-faculty.csv
│   └── faculty.csv
│
├── database/
│   └── faculty_managment.db   # SQLite database
│
├── dbConnection/
│   └── db_connection.py       # Database connection utilities
│
├── dbOperations/
│   ├── get_data.py            # Data retrieval queries
│   ├── tables_create.py       # Table creation logic
│   └── tables_insert.py       # Data insertion logic
│
├── preprocess/
│   └── preprocess.py          # Data cleaning and normalization
│
├── scrape/
│   └── dau/
│       ├── __init__.py
│       ├── faculty_url.py     # Faculty URL extraction
│       ├── faculty_details.py # Faculty detail scraping
│       └── main.py            # Scraping entry point
│
├── images/
│   └── Screenshot-1.png       # Project screenshots
│
├── __pycache__/               # Python cache files
│
├── backend.sh                 # Script to start FastAPI backend
├── frontend.sh                # Script to start Streamlit frontend
├── FastAPI.py                 # FastAPI application
├── main.py                    # Pipeline orchestration script
├── Log_LLM.md                 # LLM interaction logs
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md
```

* **client/** – Streamlit-based frontend interface
* **scrape/** – Web scraping modules for faculty data
* **preprocess/** – Data cleaning and transformation logic
* **data/** – Raw and processed CSV datasets
* **database/** – SQLite database storage
* **dbConnection/** – Database connection handling
* **dbOperations/** – Table creation, insertion, and queries
* **images/** – Screenshots used in documentation
* **backend.sh / frontend.sh** – One-command scripts to run backend and frontend

## Statistics

* Names: 112 (all unique)
* Emails: 111 non-null, all unique
* Phone numbers: 80 non-null, 78 unique
* Faculty websites: 47 available
* Bios: 70 available
* Teaching info: 59 available
* Education field: 110 available
* Specialization: 109 available (some empty lists)
* Research info: mostly empty
* Room numbers: 75 available

**Education distribution**
* Most common degree: PhD (Computer Science) 16 faculty
* Total distinct education entries: 60

**Institutes**
* Most common education institute: DA-IICT Gandhinagar 7 faculty
* Teaching institute: DAU 75 faculty

**Countries (education)**
* Total countries: 16
* Top country: USA (13 faculty)

## How to Run

### Requirements

Install the required dependencies:
```
pandas>=2.0
beautifulsoup4>=4.12
fastapi>=0.110
uvicorn[standard]>=0.27
streamlit==1.53.1
sentence-transformers==5.2.2
torch
```

### Steps to run

#### Step 1: Scrape data

From the root directory, run:
```
python scrape.dau.main
```

#### Step 2: Create and populate the database

From the root directory, run:
```
python main.py
```

#### Step 3: Start the server

Run:
```
uvicorn FastAPI:app
```

#### Step 4: Start Client

Run:
```
streamlit run ./client/app.py
```

**IMPORTANT NOTE**: One can use `backend.sh` and `frontend.sh` scripts to run the application.
