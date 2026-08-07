import pytest


@pytest.fixture
def reset_database():
    from tests.support import clear_test_data

    clear_test_data()
    yield
    clear_test_data()
