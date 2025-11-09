# Drugs MOA Quiz Application

An interactive quiz application to help medical students and healthcare professionals learn drug mechanisms of action (MOA). Built with React (frontend) and FastAPI (backend).

## Features

- Interactive quiz interface
- 25+ top prescribed medications
- Real-time feedback
- RESTful API backend
- Environment-based configuration
- Comprehensive error handling

## Tech Stack

**Frontend:**
- React 18
- Bootstrap 5
- Axios
- React Bootstrap

**Backend:**
- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn

## Prerequisites

- Node.js 16+ and npm
- Python 3.11+
- pip or pipenv

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd drugs-moa-quiz
```

### 2. Setup Backend (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the backend server
python -m uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

API Documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Setup Frontend (React)

Open a new terminal:

```bash
# From project root directory
cd drugs-moa-quiz

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Frontend Environment Variables

Create a `.env` file in the project root:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
PORT=8000
HOST=0.0.0.0
FRONTEND_URL=http://localhost:3000
```

## Project Structure

```
drugs-moa-quiz/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app and routes
│   │   ├── models.py        # Pydantic models
│   │   └── data.py          # Drug database
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── src/
│   ├── components/
│   │   ├── Answers/
│   │   ├── Banner/
│   │   ├── Layout/
│   │   └── Question/
│   ├── containers/
│   │   └── Questionaire/    # Main quiz logic
│   ├── App.js
│   └── index.js
├── public/
├── package.json
├── .env.example
└── README.md
```

## API Endpoints

### Get All MOAs
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

### Get Drug by Generic Name
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

### Get All Drugs
```
GET /api/drug/drugs/all
```

## Available Scripts

### Frontend Scripts

#### `npm start`
Runs the React app in development mode at [http://localhost:3000](http://localhost:3000)

#### `npm test`
Launches the test runner in interactive watch mode

#### `npm run build`
Builds the app for production to the `build` folder

### Backend Scripts

#### `python -m uvicorn app.main:app --reload`
Runs the FastAPI server in development mode with auto-reload

#### `python -m app.main`
Alternative way to start the server

## Development

### Adding New Drugs

Edit `backend/app/data.py` and add entries to the `DRUGS_DATABASE` list:

```python
{
    "id": 26,
    "generic_name": "drug_name",
    "brand_name": "Brand Name",
    "moa": [{"moa": "Mechanism of Action"}]
}
```

### Running Tests

```bash
# Frontend tests
npm test

# Backend tests (if configured)
cd backend
pytest
```

## Security Improvements

This project has been updated to fix critical P0 issues:

✅ **Fixed Issues:**
1. Created FastAPI backend with required endpoints
2. Removed hardcoded IP addresses
3. Implemented environment-based configuration
4. Added comprehensive error handling
5. Added data validation with optional chaining
6. Updated dependencies (209 → 9 vulnerabilities)
   - axios: 0.19.2 → 1.6.7
   - react: 16.13.1 → 18.2.0
   - react-scripts: 3.4.1 → 5.0.1

**Remaining:** 9 moderate/high vulnerabilities in dev dependencies (react-scripts 5.0.1 transitive deps)

## Deployment

### Backend Deployment

For production, use a production ASGI server:

```bash
# Using uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with gunicorn
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment

```bash
npm run build
# Deploy the build/ folder to your hosting service
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Check that port 8000 is not in use
- Verify virtual environment is activated

### Frontend shows connection errors
- Ensure backend is running on port 8000
- Check `.env` file has correct `REACT_APP_API_URL`
- Verify CORS is configured in backend

### Module not found errors
- Run `npm install` in the frontend directory
- Run `pip install -r requirements.txt` in the backend directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Learn More

- [React Documentation](https://reactjs.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Create React App Documentation](https://facebook.github.io/create-react-app/docs/getting-started)
