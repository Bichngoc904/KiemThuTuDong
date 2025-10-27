import pytest
from pages.login_page import LoginPage
from conftest import setup, base_url
from playwright.sync_api import expect

def test_login_success_username(setup, base_url):
    page = setup
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login("b18ngocie@gmail.com", 'Ngoc1809@')
    # msg_tc = login_page.get_logged()
    # assert "Tài khoản của tôi" in login_page.get_logged().inner_text().strip(), "Login failed!"
def test_login_pass_empty_fields(setup, base_url):
    page = setup
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login("b18ngocie@gmail.com", "")
   # Chờ thông báo lỗi xuất hiện
    expect(login_page.error_password).to_be_visible(timeout=20000)

    # Kiểm tra nội dung thông báo lỗi
    actual = login_page.error_password.inner_text().strip()
    expected = "Vui lòng nhập Mật khẩu"
    assert actual == expected, f"Nội dung thông báo không đúng! expected: {expected!r}, got: {actual!r}"

def test_login_email_empty_fields(setup, base_url):
    page = setup
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login("", "Ngoc1809@")
   # Chờ thông báo lỗi xuất hiện
    expect(login_page.error_email).to_be_visible(timeout=20000)

    # Kiểm tra nội dung thông báo lỗi
    actual = login_page.error_email.inner_text().strip()
    expected = "Vui lòng nhập Email"
    assert actual == expected, f"Nội dung thông báo không đúng! expected: {expected!r}, got: {actual!r}"

def test_login_invalid_email(setup, base_url):
    page = setup
    login_page = LoginPage(page, base_url)
    login_page.open()
    login_page.login("bngocie@gmail", "Ngoc1809@")
   # Chờ thông báo lỗi xuất hiện
    expect(login_page.invalid_email_or_password).to_be_visible(timeout=20000)

    # Kiểm tra nội dung thông báo lỗi
    actual = login_page.invalid_email_or_password.inner_text().strip()
    expected = "Thông tin đăng nhập không chính xác"
    assert actual == expected, f"Nội dung thông báo không đúng! expected: {expected!r}, got: {actual!r}"