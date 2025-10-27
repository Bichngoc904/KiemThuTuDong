from playwright.sync_api import Page
from playwright.sync_api import sync_playwright, expect
from pages.base_page import BasePage

class LoginPageData(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

        # Locators
        self._goto_login = "//a[text()='Đăng nhập']"
        self._email_input = "#email"
        self._password_input = "#pass"
        self._login_button = "#send2"
        self._error_email = "//li[contains(text(),'Vui lòng nhập Email')]"
        self._error_password = "//li[contains(text(),'Vui lòng nhập Mật khẩu')]"
        self._invalid_email_or_password = "//li[contains(text(),'Thông tin đăng nhập không chính xác')]"
        self._phone_number = "//a[@href='tel:096.2828.242']/span"
        # self._logged_text = "//div[@class='block-title' and text()='Tài khoản của tôi']"

    def open(self):
        """Mở trang login"""
        self.page.goto(f"{self.base_url}account/login", wait_until="domcontentloaded", timeout=60000)


    def login(self, email: str, password: str):
        """Thực hiện login"""
        self.page.locator(self._goto_login).click()
        self.page.locator(self._email_input).fill(str(email or ""))  # ép kiểu sang string
        self.page.locator(self._password_input).fill(str(password or ""))  # ép kiểu sang string
        self.page.locator(self._login_button).click()

    @property
    def error_email(self):
        """Lấy text lỗi email"""
        return self.page.locator(self._error_email).inner_text().strip()

    @property
    def error_password(self):
        return self.page.locator(self._error_password).inner_text().strip()

    @property
    def invalid_login(self):
        return self.page.locator(self._invalid_email_or_password).inner_text().strip()

    @property
    def logged(self):
        return self.page.locator(self._phone_number)
   