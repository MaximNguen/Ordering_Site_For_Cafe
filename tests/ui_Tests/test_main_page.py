from selenium.webdriver.common.by import By
from conftest import *

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_home_title(open_page, alert_about_ui_tests):
    title = open_page.find_element(By.CLASS_NAME, "logo-link-header")
    assert title.is_displayed()

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_display_number_correct(open_page):
    number = open_page.find_element(By.CSS_SELECTOR, "a.phone-link").text
    assert number == "+7 (123) 456-78-90"

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_display_login(open_page):
    button = open_page.find_element(By.CSS_SELECTOR, "a.button-header-login").text
    assert button == "Вход"
