# Backend Data Engineering Project

## 🎯 Project Overview

This project implements a normalized SQLite database for managing faculty information, including their specializations, teaching assignments, and research areas. The system includes a CSV ingestion pipeline and a FastAPI backend for data access.

## 📚 Development Journey

This README documents the complete learning process, including challenges faced and solutions implemented.

### 🗓️ Phase 1: Project Initialization

**✓ Decisions Made**
- Used SQLite for lightweight relational storage
- Structured project with separate DB utility layer
- Adopted class-based design for table operations

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


---

### 🗓️ Phase 5: Table Deletion & Recreation

**❌ Error Faced**
```
sqlite3.OperationalError: no such table
```

**🔧 Fix**
- Used `DROP TABLE IF EXISTS` for safer cleanup
- Ensured tables are created before any delete operations


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


---

### 🗓️ Phase 8: FastAPI Setup

**❌ Error Faced**
```
Error loading ASGI app. Import string "FastAPI" must be in format "<module>:<attribute>"
```

**🔧 Fix**
- Corrected Uvicorn command: `uvicorn main:app --reload`
- Module name must match Python file name

---

### 🗓️ Phase 9: API Data Aggregation

**❌ Problem**
- SQL joins produced duplicate rows
- One-to-many relationships flattened hierarchical data

**🔧 Fix**
- Aggregated rows manually in Python
- Converted relational tabular data into hierarchical JSON
- Implemented proper grouping logic

---

### 🗓️ Phase 10: Version Control & Documentation

**✓ Decisions**
- Added `requirements.txt` for dependency management
- Learned `.env` is for environment variables, not Python packages
- Structured README as both documentation and learning log

---

## ✅ Final Outcome

- ✓ Fully normalized SQLite database
- ✓ CSV → Database ingestion pipeline
- ✓ FastAPI backend for data access
- ✓ Strong debugging and environment handling experience
- ✓ End-to-end data engineering workflow
