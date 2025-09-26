from selenium.webdriver.common.by import By
from conftest import *

@pytest.mark.parametrize('open_page', ['promo'], indirect=True)
def test_home_title(open_page, alert_about_ui_tests):
    open_page.implicitly_wait(5)
    title = open_page.find_element(By.CLASS_NAME, "logo-link-header")
    assert title.is_displayed()