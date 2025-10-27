import pytest
from playwright.sync_api import sync_playwright, expect
from utils.data_utils import load_data
from pages.login_page_data import LoginPageData
from utils.report_helper import log_test_result
from conftest import base_url  

# Load data từ Excel
test_data = load_data("login_cases.xlsx")

@pytest.mark.parametrize("email,password,expected", test_data)
def test_login_ddt(email, password, expected, base_url):   
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = LoginPageData(page, base_url)
        login_page.open()
        login_page.login(email or "", password or "")

        if expected == "success":
            phone_locator = login_page.page.locator(login_page._phone_number)
            expect(phone_locator).to_have_text("096.2828.242", timeout=5000)

        elif expected == "error_email":
            assert login_page.error_email, "Vui lòng nhập Email"
        elif expected == "error_password":
            assert login_page.error_password, "Vui lòng nhập Mật khẩu"
        elif expected == "invalid_login":
            assert login_page.invalid_login, "Thông tin đăng nhập không chính xác"
        
        
        
