from selenium.webdriver.common.by import By
from conftest import *
# ДО ВХОДА В АККАУНТ
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

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_all_button_display(open_page):
    all_button = open_page.find_elements(By.CSS_SELECTOR, ".all-buttons > *")
    assert len(all_button) == 5

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_cards_of_menu(open_page):
    cards = open_page.find_elements(By.CSS_SELECTOR, ".menu-cards-row > *")
    assert len(cards) == 4

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_cards_of_promotions(open_page):
    cards = open_page.find_elements(By.CSS_SELECTOR, ".promotions-cards-row > *")
    assert len(cards) == 3

@pytest.mark.parametrize('open_page', ['main'], indirect=True)
def test_map_displayed(open_page):
    map = open_page.find_element(By.TAG_NAME, "iframe")
    assert map.is_displayed()

