"""
Test to verify pytest setup is working correctly.

This file can be deleted once actual tests are written.
"""

import pytest


def test_pytest_working():
    """Verify pytest is installed and working."""
    assert True


def test_imports():
    """Verify we can import from the app module."""
    from app.main import app
    from app.data import get_all_moas, get_drug_by_generic_name
    from app.models import Drug, MOAResponse

    assert app is not None
    assert callable(get_all_moas)
    assert callable(get_drug_by_generic_name)


@pytest.mark.unit
def test_markers_work():
    """Verify custom markers are working."""
    assert True
