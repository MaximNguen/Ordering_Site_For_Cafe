import pytest


@pytest.fixture(scope="session")
def alert_about_ui_tests():
    print("Alert About UI Tests")
    yield
    print("Alert About UI Tests END ----------")

# @pytest.fixture(scope="function")
# def open_browser_main_page():

