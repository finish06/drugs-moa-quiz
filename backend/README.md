# Drugs MOA Quiz - FastAPI Backend

FastAPI backend for the Drugs Mechanism of Action (MOA) quiz application.

## Features

- RESTful API with FastAPI
- Drug database with 25+ top prescribed medications
- MOA (Mechanism of Action) lookup
- CORS enabled for React frontend
- Environment-based configuration

## Prerequisites

- Python 3.11+
- pip or pipenv

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env if needed (default values work for local development)
   ```

## Running the Server

**Development mode (with auto-reload):**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Or using the main module:
```bash
cd backend
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### 1. Get All MOAs
```
GET /api/drug/moa/?format=json
```

Response:
```json
[
  {"id": 1, "moa": "ACE Inhibitor"},
  {"id": 2, "moa": "Beta-1 Selective Blocker"},
  ...
]
```

### 2. Get Drug by Generic Name
```
GET /api/drug/drugs/?format=json&generic=lisinopril
```

Response:
```json
[
  {
    "id": 1,
    "generic_name": "lisinopril",
    "brand_name": "Prinivil, Zestril",
    "moa": [{"moa": "ACE Inhibitor"}]
  }
]
```

### 3. Get All Drugs
```
GET /api/drug/drugs/all
```

Returns all drugs in the database.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app and routes
│   ├── models.py       # Pydantic models
│   └── data.py         # Drug database
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Adding More Drugs

Edit `app/data.py` and add entries to the `DRUGS_DATABASE` list:

```python
{
    "id": 26,
    "generic_name": "drug_name",
    "brand_name": "Brand Name",
    "moa": [{"moa": "Mechanism of Action"}]
}
```

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (React dev server)
- Custom URL via `FRONTEND_URL` environment variable

To modify CORS settings, edit `app/main.py`.

## Testing

### Setup Test Environment

1. **Install test dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run all tests:**
   ```bash
   pytest
   ```

3. **Run tests with coverage:**
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

4. **Run tests with HTML coverage report:**
   ```bash
   pytest --cov=app --cov-report=html
   # Open htmlcov/index.html in your browser
   ```

### Test Organization

```
backend/tests/
├── unit/               # Unit tests for individual modules
├── integration/        # API endpoint integration tests
├── performance/        # Performance and benchmark tests
├── conftest.py         # Shared fixtures and test configuration
└── test_setup.py       # Basic setup verification test
```

### Running Specific Test Types

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run a specific test file
pytest tests/unit/test_data.py

# Run a specific test function
pytest tests/unit/test_data.py::test_get_all_moas

# Run tests in verbose mode
pytest -v

# Run tests in parallel (faster)
pytest -n auto
```

### Test Coverage Goals

- **Overall Backend Coverage:** 80% minimum
- **Data Layer (app/data.py):** 90% minimum
- **Models (app/models.py):** 95% minimum
- **API Endpoints (app/main.py):** 100% endpoint coverage

### Writing Tests

All tests have access to shared fixtures defined in `tests/conftest.py`:

```python
def test_example(client, sample_drug):
    """Example test using fixtures."""
    response = client.get(f"/api/drug/drugs/?generic={sample_drug.generic}")
    assert response.status_code == 200
```

See `TESTING_QUICKSTART.md` in the project root for detailed testing examples.

## Production Deployment

For production, use a production-grade ASGI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn:
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
