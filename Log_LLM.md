# Backend Data Engineering Project

A complete data engineering workflow demonstrating database design, CSV data ingestion, and FastAPI backend development. This project serves as both a functional application and a learning documentation of the entire development process.

## 🎯 Project Overview

This project implements a normalized SQLite database for managing faculty information, including their specializations, teaching assignments, and research areas. The system includes a CSV ingestion pipeline and a FastAPI backend for data access.

## ✨ Features

- ✅ Fully normalized SQLite database with proper relationships
- ✅ CSV to database ingestion pipeline
- ✅ FastAPI REST API backend
- ✅ Many-to-many relationship handling
- ✅ Comprehensive error handling and validation

## 🛠️ Tech Stack

- **Database**: SQLite
- **Backend**: FastAPI
- **Language**: Python 3.x
- **Libraries**: pandas, uvicorn

## 📁 Project Structure

```
.
├── DbUtility/          # Database logic and utilities
├── main.py             # FastAPI application entry point
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 📊 Database Schema

### Core Tables
- **Faculty**: Main faculty information
- **Specialization**: Academic specializations
- **Teaching**: Teaching subjects/courses
- **Research**: Research areas

### Junction Tables
- **Faculty_Specialization**: Links faculty to their specializations
- **Faculty_Teaching**: Links faculty to teaching assignments
- **Faculty_Research**: Links faculty to research areas

## 🚀 Getting Started

### Prerequisites

```bash
python --version  # Python 3.7+
```

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 Development Journey

This README documents the complete learning process, including challenges faced and solutions implemented.

### 🗓️ Phase 1: Project Initialization

**✓ Decisions Made**
- Used SQLite for lightweight relational storage
- Structured project with separate DB utility layer
- Adopted class-based design for table operations

**📌 Learning**
- SQLite is ideal for prototyping and learning database design
- Keeping DB logic separate improves maintainability

---

### 🗓️ Phase 2: Database Schema Design

**✓ Tables Designed**
- Core entity tables with proper primary keys
- Junction tables for many-to-many relationships

**❌ Error Faced**
```
sqlite3.OperationalError: incomplete input
```

**🔧 Fix**
- Missing closing parenthesis in CREATE TABLE statement
- Learned to inspect SQL carefully as SQLite error messages are minimal

**❌ Error Faced**
```
unknown column "Specialization_id" in foreign key definition
```

**🔧 Fix**
- Column name and referenced primary key mismatch
- Ensured foreign keys reference existing columns exactly

**📌 Learning**
- Foreign key definitions require exact naming consistency
- Order of table creation matters for dependencies

---

### 🗓️ Phase 3: CSV Data Handling

**✓ CSV Structure**
- Multi-value columns stored as comma-separated strings
- Example: `['Computer Vision', 'Image Processing']`

**❌ Problem**
- CSV values read as strings, not Python lists
- Lost datatype information during CSV parsing

**🔧 Fix**
- Implemented manual CSV string parsing
- Split values before inserting into junction tables

**📌 Learning**
- CSV does not preserve Python datatypes
- Many-to-many relationships must not be stored as comma-separated strings in DB

---

### 🗓️ Phase 4: Data Insertion Logic

**❌ Error Faced**
```
sqlite3.IntegrityError: datatype mismatch
```

**🔧 Fix**
- Ensured IDs are integers, not strings
- Implemented `get_or_create()` logic for lookup tables
- Insert values first, then retrieve IDs for foreign keys

**📌 Learning**
- Datatype mismatches usually originate from CSV ingestion
- Validation before insertion is critical

---

### 🗓️ Phase 5: Table Deletion & Recreation

**❌ Error Faced**
```
sqlite3.OperationalError: no such table
```

**🔧 Fix**
- Used `DROP TABLE IF EXISTS` for safer cleanup
- Ensured tables are created before any delete operations

**📌 Learning**
- Execution order matters in database lifecycle scripts
- Always use conditional drops in reset scripts

---

### 🗓️ Phase 6: Python Code Quality

**❌ Error Faced**
```
PEP 8: E302 expected 2 blank lines
```

**📌 Learning**
- PEP 8 enforces Python code readability standards
- Class and function definitions need proper spacing

**❌ Error Faced**
```
Parameter 'self' unfilled
```

**📌 Learning**
- Class methods must be called using object instances
- Common beginner mistake in OOP

---

### 🗓️ Phase 7: Environment & Dependency Issues

**❌ Error Faced**
```
ModuleNotFoundError: No module named 'pandas.util'
```

**🔧 Root Cause**
- Python interpreter mismatch
- Corrupted or partial package installation

**🔧 Fix**
- Verified interpreter path with `which python`
- Reinstalled pandas using correct Python version
- Checked installed packages with `python -m pip list`

**📌 Learning**
- Python environment issues are real-world blockers
- Always verify active Python environment

---

### 🗓️ Phase 8: FastAPI Setup

**❌ Error Faced**
```
Error loading ASGI app. Import string "FastAPI" must be in format "<module>:<attribute>"
```

**🔧 Fix**
- Corrected Uvicorn command: `uvicorn main:app --reload`
- Module name must match Python file name

**📌 Learning**
- ASGI apps require explicit module:attribute reference
- FastAPI setup errors are often command-related

---

### 🗓️ Phase 9: API Data Aggregation

**❌ Problem**
- SQL joins produced duplicate rows
- One-to-many relationships flattened hierarchical data

**🔧 Fix**
- Aggregated rows manually in Python
- Converted relational tabular data into hierarchical JSON
- Implemented proper grouping logic

**📌 Learning**
- Databases return tabular data naturally
- APIs require structured, nested JSON
- Backend transformation layer is essential

---

### 🗓️ Phase 10: Version Control & Documentation

**✓ Decisions**
- Added `requirements.txt` for dependency management
- Learned `.env` is for environment variables, not Python packages
- Structured README as both documentation and learning log

**📌 Learning**
- Reproducibility matters for collaboration
- Documentation reflects engineering maturity

---

## ✅ Final Outcome

- ✓ Fully normalized SQLite database
- ✓ CSV → Database ingestion pipeline
- ✓ FastAPI backend for data access
- ✓ Strong debugging and environment handling experience
- ✓ End-to-end data engineering workflow

## 🧠 Key Skills Gained

- SQL schema design and normalization
- Many-to-many relationship implementation
- CSV preprocessing and validation
- Python OOP patterns and best practices
- Debugging SQLite and Python errors
- Environment and dependency management
- FastAPI backend development
- API design and data transformation

## 🤝 Contributing

This is a learning project, but suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 📬 Contact

For questions or feedback, please open an issue in the repository.

---

**Note**: This README serves as both project documentation and a learning tracker, documenting the entire development journey including challenges, solutions, and key takeaways.