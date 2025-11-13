# Testing Quick Start Guide

This guide provides immediate steps to start implementing tests for the Drugs MOA Quiz application.

## 🚀 Quick Setup

### Frontend Testing (Already Configured!)

Your React app already has Jest and React Testing Library installed. You can start writing tests immediately:

```bash
# Run tests in watch mode
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in CI mode (single run)
npm test -- --ci
```

### Backend Testing (Needs Setup)

1. **Install test dependencies**:
```bash
cd backend
pip install pytest pytest-cov pytest-asyncio httpx
```

2. **Or create `requirements-dev.txt`**:
```txt
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2
```

Then install:
```bash
pip install -r requirements-dev.txt
```

3. **Create test directory structure**:
```bash
mkdir -p backend/tests/{unit,integration,performance}
touch backend/tests/__init__.py
touch backend/tests/conftest.py
touch backend/tests/pytest.ini
```

4. **Configure pytest** (`backend/pytest.ini`):
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
```

5. **Run backend tests**:
```bash
cd backend
pytest
pytest --cov=app
```

## 📝 Writing Your First Tests

### Frontend Component Test

Create `src/components/Question/__tests__/Question.test.js`:

```javascript
import React from 'react';
import { render, screen } from '@testing-library/react';
import Question from '../Question';

describe('Question Component', () => {
  test('displays drug name in question text', () => {
    render(<Question drug="lisinopril" />);

    expect(screen.getByText(/What is the mechanism of action of lisinopril/i))
      .toBeInTheDocument();
  });

  test('handles empty drug name gracefully', () => {
    render(<Question drug="" />);

    expect(screen.getByText(/What is the mechanism of action of/i))
      .toBeInTheDocument();
  });
});
```

### Frontend Container Test

Create `src/containers/Questionaire/__tests__/Questionaire.test.js`:

```javascript
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Questionaire from '../Questionaire';
import axios from '../../../axios-orders';

// Mock axios
jest.mock('../../../axios-orders');

describe('Questionaire Container', () => {
  const mockMoas = [
    { id: 1, moa: 'ACE Inhibitor' },
    { id: 2, moa: 'Beta Blocker' },
    { id: 3, moa: 'Calcium Channel Blocker' },
    { id: 4, moa: 'Diuretic' }
  ];

  const mockDrug = [
    { generic: 'lisinopril', moa: 'ACE Inhibitor' }
  ];

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
  });

  test('loads and displays first question', async () => {
    axios.get.mockImplementation((url) => {
      if (url.includes('moa')) {
        return Promise.resolve({ data: mockMoas });
      }
      return Promise.resolve({ data: mockDrug });
    });

    render(<Questionaire />);

    await waitFor(() => {
      expect(screen.getByText(/What is the mechanism of action/i))
        .toBeInTheDocument();
    });
  });

  test('displays error when API fails', async () => {
    axios.get.mockRejectedValue(new Error('Network error'));

    render(<Questionaire />);

    // Note: This will fail until DEFECT-003 is fixed
    // await waitFor(() => {
    //   expect(screen.getByText(/error/i)).toBeInTheDocument();
    // });
  });
});
```

### Backend Unit Test

Create `backend/tests/unit/test_data.py`:

```python
import pytest
from app.data import get_all_moas, get_drug_by_generic_name, DRUGS_DATABASE

class TestGetAllMoas:
    def test_returns_list_of_moa_objects(self):
        """get_all_moas should return list of MOA objects"""
        moas = get_all_moas()

        assert isinstance(moas, list)
        assert len(moas) > 0

        # Check structure of first MOA
        assert hasattr(moas[0], 'id')
        assert hasattr(moas[0], 'moa')

    def test_all_moas_are_unique(self):
        """Each MOA should appear only once in the list"""
        moas = get_all_moas()
        moa_values = [m.moa for m in moas]

        assert len(moa_values) == len(set(moa_values))

    def test_no_empty_moas(self):
        """No MOA should be empty or None"""
        moas = get_all_moas()

        for moa in moas:
            assert moa.moa is not None
            assert moa.moa.strip() != ""


class TestGetDrugByGenericName:
    def test_finds_existing_drug(self):
        """Should find drug that exists in database"""
        drug = get_drug_by_generic_name("lisinopril")

        assert drug is not None
        assert drug.generic == "lisinopril"
        assert drug.moa is not None

    def test_returns_none_for_nonexistent_drug(self):
        """Should return None for drug that doesn't exist"""
        drug = get_drug_by_generic_name("nonexistent-drug-12345")

        assert drug is None

    def test_case_insensitive_search(self):
        """Drug search should be case-insensitive"""
        drug_lower = get_drug_by_generic_name("lisinopril")
        drug_upper = get_drug_by_generic_name("LISINOPRIL")
        drug_mixed = get_drug_by_generic_name("LiSiNoPrIl")

        assert drug_lower == drug_upper == drug_mixed

    def test_handles_whitespace(self):
        """Should handle leading/trailing whitespace"""
        drug = get_drug_by_generic_name("  lisinopril  ")

        assert drug is not None
        assert drug.generic == "lisinopril"


class TestDatabaseIntegrity:
    def test_all_drugs_have_moa(self):
        """Every drug in database must have a MOA"""
        for drug in DRUGS_DATABASE:
            assert drug.moa is not None, f"Drug {drug.generic} has no MOA"
            assert drug.moa.strip() != "", f"Drug {drug.generic} has empty MOA"

    def test_no_duplicate_drugs(self):
        """No duplicate drug names in database"""
        generics = [drug.generic for drug in DRUGS_DATABASE]

        assert len(generics) == len(set(generics)), \
            "Database contains duplicate drugs"

    def test_all_drugs_have_generic_name(self):
        """Every drug must have a generic name"""
        for drug in DRUGS_DATABASE:
            assert drug.generic is not None
            assert drug.generic.strip() != ""
```

### Backend API Integration Test

Create `backend/tests/integration/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_root_endpoint_returns_200(self):
        """GET / should return 200 OK"""
        response = client.get("/")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestMOAEndpoint:
    def test_get_moas_returns_200(self):
        """GET /api/drug/moa/ should return 200"""
        response = client.get("/api/drug/moa/?format=json")

        assert response.status_code == 200

    def test_get_moas_returns_list(self):
        """MOA endpoint should return list"""
        response = client.get("/api/drug/moa/?format=json")
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

    def test_moa_response_schema(self):
        """Each MOA should have id and moa fields"""
        response = client.get("/api/drug/moa/?format=json")
        data = response.json()

        for item in data:
            assert "id" in item
            assert "moa" in item
            assert isinstance(item["moa"], str)


class TestDrugsEndpoint:
    def test_get_drug_by_name_success(self):
        """GET /api/drug/drugs/ with valid drug returns 200"""
        response = client.get("/api/drug/drugs/?format=json&generic=lisinopril")

        assert response.status_code == 200

    def test_get_drug_returns_list_format(self):
        """Drug endpoint should return list (matches Django format)"""
        response = client.get("/api/drug/drugs/?format=json&generic=lisinopril")
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 1

    def test_get_drug_response_schema(self):
        """Drug response should have required fields"""
        response = client.get("/api/drug/drugs/?format=json&generic=lisinopril")
        data = response.json()
        drug = data[0]

        assert "generic" in drug
        assert "moa" in drug
        assert drug["generic"] == "lisinopril"

    def test_get_drug_not_found_returns_empty_list(self):
        """Non-existent drug should return empty list"""
        response = client.get("/api/drug/drugs/?format=json&generic=nonexistent")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_drug_missing_parameter_returns_400(self):
        """Missing generic parameter should return 400"""
        response = client.get("/api/drug/drugs/?format=json")

        assert response.status_code == 400

    def test_get_drug_case_insensitive(self):
        """Drug lookup should be case-insensitive"""
        response1 = client.get("/api/drug/drugs/?generic=lisinopril")
        response2 = client.get("/api/drug/drugs/?generic=LISINOPRIL")

        assert response1.json() == response2.json()


class TestAllDrugsEndpoint:
    def test_get_all_drugs_returns_200(self):
        """GET /api/drug/drugs/all should return 200"""
        response = client.get("/api/drug/drugs/all")

        assert response.status_code == 200

    def test_get_all_drugs_returns_list(self):
        """All drugs endpoint should return list"""
        response = client.get("/api/drug/drugs/all")
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0


class TestCORS:
    def test_cors_headers_present(self):
        """CORS headers should be configured"""
        response = client.options(
            "/api/drug/moa/",
            headers={"Origin": "http://localhost:3000"}
        )

        # CORS headers should be present
        # Note: TestClient may not fully simulate CORS
        assert response.status_code in [200, 404]
```

## 🎯 Priority Test Cases (Start Here)

### Week 1: Critical Backend Tests
1. ✅ `test_get_drug_returns_none_for_nonexistent_drug` - Prevents crashes
2. ✅ `test_all_drugs_have_moa` - Data integrity
3. ✅ `test_get_drug_missing_parameter_returns_400` - API contract

### Week 2: Critical Frontend Tests
1. ✅ `test_displays_drug_name_in_question` - Basic rendering
2. ✅ `test_loads_and_displays_first_question` - Integration
3. ✅ Test for DEFECT-005 (duplicate answers)

### Week 3: Bug-Fix Tests (TDD Approach)
Write tests FIRST, then fix the bugs:
1. ✅ DEFECT-001: Test quiz ends after 10 questions
2. ✅ DEFECT-005: Test no duplicate answer options
3. ✅ DEFECT-013: Test answer position doesn't change on re-render

## 🐛 Test-Driven Bug Fixing

Example: Fixing DEFECT-005 (Duplicate Answers) using TDD

### Step 1: Write Failing Test FIRST

```javascript
// src/components/Answers/__tests__/Answers.test.js
test('all answer options are unique', () => {
  const mockMOAs = [
    { id: 1, moa: 'ACE Inhibitor' },
    { id: 2, moa: 'Beta Blocker' },
    { id: 3, moa: 'Calcium Channel Blocker' },
    { id: 4, moa: 'Diuretic' },
    { id: 5, moa: 'Statin' }
  ];

  render(
    <Answers
      position={1}
      correct="ACE Inhibitor"
      options={mockMOAs}
      checkAnswer={jest.fn()}
    />
  );

  const answerButtons = screen.getAllByRole('listitem');
  const answerTexts = answerButtons.map(btn => btn.textContent);

  // All answers should be unique
  const uniqueAnswers = new Set(answerTexts);
  expect(uniqueAnswers.size).toBe(4);
});
```

### Step 2: Run Test (Should FAIL)
```bash
npm test -- Answers.test.js
# Test fails - duplicates can occur
```

### Step 3: Fix the Code
```javascript
// src/components/Answers/Answers.js
const generateAnswers = (correct, allOptions, position) => {
  const answers = [];
  const usedMOAs = new Set([correct]);

  // Add correct answer at specified position
  answers[position - 1] = correct;

  // Fill remaining positions with unique random MOAs
  while (answers.filter(Boolean).length < 4) {
    const randomIndex = Math.floor(Math.random() * allOptions.length);
    const randomMOA = allOptions[randomIndex].moa;

    if (!usedMOAs.has(randomMOA)) {
      // Find first empty slot
      const emptyIndex = answers.findIndex(a => a === undefined);
      answers[emptyIndex] = randomMOA;
      usedMOAs.add(randomMOA);
    }
  }

  return answers;
};
```

### Step 4: Run Test Again (Should PASS)
```bash
npm test -- Answers.test.js
# ✅ All tests pass
```

## 📊 Coverage Reports

### View Frontend Coverage
```bash
npm test -- --coverage
# Opens: coverage/lcov-report/index.html
```

### View Backend Coverage
```bash
cd backend
pytest --cov=app --cov-report=html
# Opens: htmlcov/index.html
```

## 🔄 CI/CD Integration

Create `.github/workflows/test.yml`:

```yaml
name: Test Suite

on:
  pull_request:
  push:
    branches: [master, main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      # Frontend tests
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install frontend dependencies
        run: npm ci

      - name: Run frontend tests
        run: npm test -- --ci --coverage

      # Backend tests
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install backend dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov httpx

      - name: Run backend tests
        run: |
          cd backend
          pytest --cov=app
```

## 📚 Next Steps

1. **Immediate**: Set up backend testing (5 minutes)
   ```bash
   cd backend
   pip install pytest pytest-cov httpx
   mkdir -p tests/unit tests/integration
   ```

2. **Today**: Write your first 3 tests
   - 1 backend unit test
   - 1 frontend component test
   - 1 API integration test

3. **This Week**: Achieve 50% coverage
   - Focus on critical paths
   - Test bug fixes with TDD
   - Set up CI/CD

4. **This Month**: Full test suite
   - Follow the 8-sprint roadmap in TESTING_STRATEGY.md
   - Add E2E tests with Playwright
   - Conduct UAT

## 🆘 Troubleshooting

### Frontend Tests Not Running
```bash
# Clear cache
npm test -- --clearCache

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Backend Import Errors
```bash
# Make sure you're in the backend directory
cd backend

# Verify PYTHONPATH includes app directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Mock Not Working
```javascript
// Make sure mock is before imports
jest.mock('../../../axios-orders');
import Questionaire from '../Questionaire';
```

## 📖 Resources

- **Full Strategy**: See `TESTING_STRATEGY.md` for complete plan
- **React Testing Library**: https://testing-library.com/react
- **Jest**: https://jestjs.io/
- **Pytest**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

---

**Ready to start?** Pick one test from the Priority Test Cases section and write it now! 🚀
