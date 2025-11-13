"""
Shared pytest fixtures for Drugs MOA Quiz Backend tests

This file contains fixtures that are available to all tests without
needing to import them explicitly.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.data import DRUGS_DATABASE, get_all_moas


# ============================================================================
# API Client Fixtures
# ============================================================================

@pytest.fixture(scope="module")
def client():
    """
    Create a FastAPI test client for integration tests.

    Scope: module - client is created once per test module

    Usage:
        def test_endpoint(client):
            response = client.get("/api/endpoint")
            assert response.status_code == 200
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def client_fresh():
    """
    Create a fresh FastAPI test client for each test.

    Scope: function - new client for each test function
    Use this when you need complete isolation between tests.

    Usage:
        def test_stateful_endpoint(client_fresh):
            response = client_fresh.post("/api/data", json={...})
            assert response.status_code == 201
    """
    with TestClient(app) as test_client:
        yield test_client


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_drug():
    """
    Return a sample drug from the database for testing.

    Returns:
        Drug: The first drug in the database (lisinopril)
    """
    return DRUGS_DATABASE[0]


@pytest.fixture
def sample_drug_name():
    """Return a valid drug name for testing."""
    return "lisinopril"


@pytest.fixture
def invalid_drug_name():
    """Return an invalid drug name for negative testing."""
    return "nonexistent-drug-xyz-12345"


@pytest.fixture
def sample_moas():
    """
    Return a list of all MOAs for testing.

    Returns:
        List[MOAResponse]: All mechanisms of action
    """
    return get_all_moas()


@pytest.fixture
def sample_moa_list():
    """Return a list of MOA strings for testing."""
    moas = get_all_moas()
    return [moa.moa for moa in moas]


# ============================================================================
# Mock Data Fixtures
# ============================================================================

@pytest.fixture
def mock_moa_response():
    """
    Return mock MOA API response data.

    Useful for testing frontend integration or mocking API responses.
    """
    return [
        {"id": 1, "moa": "ACE Inhibitor"},
        {"id": 2, "moa": "Beta Blocker"},
        {"id": 3, "moa": "Calcium Channel Blocker"},
        {"id": 4, "moa": "Diuretic"}
    ]


@pytest.fixture
def mock_drug_response():
    """Return mock drug API response data."""
    return [
        {
            "generic": "lisinopril",
            "moa": "ACE Inhibitor"
        }
    ]


# ============================================================================
# Test Parametrization Data
# ============================================================================

@pytest.fixture
def drug_variations():
    """
    Return various forms of the same drug name for testing case sensitivity.

    Returns:
        list: Different case variations of "lisinopril"
    """
    return [
        "lisinopril",
        "LISINOPRIL",
        "Lisinopril",
        "LiSiNoPrIl",
        "liSINopril"
    ]


@pytest.fixture
def whitespace_variations():
    """
    Return drug names with various whitespace for testing trimming.

    Returns:
        list: Drug names with leading/trailing/multiple spaces
    """
    return [
        "  lisinopril",
        "lisinopril  ",
        "  lisinopril  ",
        " lisinopril ",
        "  lisinopril   "
    ]


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers.

    This runs once at the start of the test session.
    """
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as a performance test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test items during collection.

    Automatically marks tests based on their location:
    - tests/unit/* -> unit marker
    - tests/integration/* -> integration marker
    - tests/performance/* -> performance marker
    """
    for item in items:
        # Get the test file path
        test_path = str(item.fspath)

        # Auto-mark based on directory
        if "/unit/" in test_path:
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in test_path:
            item.add_marker(pytest.mark.integration)
        elif "/performance/" in test_path:
            item.add_marker(pytest.mark.performance)
            item.add_marker(pytest.mark.slow)


# ============================================================================
# Session-level Fixtures
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Set up the test environment before any tests run.

    This runs once at the start of the test session and
    automatically applies to all tests.
    """
    # Setup code here
    print("\n" + "="*70)
    print("Setting up test environment for Drugs MOA Quiz Backend")
    print("="*70)

    yield  # Tests run here

    # Teardown code here
    print("\n" + "="*70)
    print("Tearing down test environment")
    print("="*70)


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def assert_valid_drug_schema():
    """
    Return a function to validate drug object schema.

    Usage:
        def test_drug(assert_valid_drug_schema):
            drug = get_drug_by_generic_name("lisinopril")
            assert_valid_drug_schema(drug)
    """
    def _assert(drug):
        assert hasattr(drug, "generic"), "Drug must have 'generic' attribute"
        assert hasattr(drug, "moa"), "Drug must have 'moa' attribute"
        assert drug.generic is not None, "Drug generic name cannot be None"
        assert drug.moa is not None, "Drug MOA cannot be None"
        assert drug.generic.strip() != "", "Drug generic name cannot be empty"
        assert drug.moa.strip() != "", "Drug MOA cannot be empty"
    return _assert


@pytest.fixture
def assert_valid_moa_schema():
    """
    Return a function to validate MOA object schema.

    Usage:
        def test_moa(assert_valid_moa_schema):
            moa = get_all_moas()[0]
            assert_valid_moa_schema(moa)
    """
    def _assert(moa):
        assert hasattr(moa, "id"), "MOA must have 'id' attribute"
        assert hasattr(moa, "moa"), "MOA must have 'moa' attribute"
        assert isinstance(moa.id, int), "MOA id must be an integer"
        assert isinstance(moa.moa, str), "MOA moa must be a string"
        assert moa.moa.strip() != "", "MOA value cannot be empty"
    return _assert
