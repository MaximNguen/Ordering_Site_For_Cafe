import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope="session")
def alert_about_ui_tests():
    print("Alert About UI Tests --------------")
    yield
    print("Alert About UI Tests END ----------")

@pytest.fixture()
def open_page(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    param = request.param
    if param == "main":
        driver.get("http://127.0.0.1:8000/")
    elif param == "promo":
        driver.get("http://127.0.0.1:8000/")
        driver.implicitly_wait(2)
        promoButton = driver.find_element(By.CSS_SELECTOR, ".button-promotions").click()
    return driver



