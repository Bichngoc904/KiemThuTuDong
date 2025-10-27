from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # @property
    # def goto_login(self):
    #     return self.page.locator('a[href="/account/login"]')
    @property
    def goto_login(self):
        return self.page.get_by_text("Đăng nhập", exact=True)

    @property
    def email_input(self):
        return self.page.locator("#email")

    @property
    def password_input(self):
        return self.page.locator("#pass")

    @property
    def login_button(self):
        return self.page.locator("#send2")

    @property
    def error_email(self):
        return self.page.locator("xpath=//li[contains(text(),'Vui lòng nhập Email')]")

    @property
    def error_password(self):
      return self.page.locator("xpath=//li[contains(text(),'Vui lòng nhập Mật khẩu')]")

    @property
    def invalid_email_or_password(self):
        return self.page.locator("xpath=//li[contains(text(),'Thông tin đăng nhập không chính xác')]")

    @property
    def forgot_password_link(self):
        return self.page.locator("#RecoverPassword")
    @property
    def get_logged(self):
        return self.page.locator("//div[@class='block-title' and text()='Tài khoản của tôi']")
    
    def open(self):
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=60000)
 
    def login(self, email: str, password: str):
        self.goto_login.wait_for(state="visible", timeout=50000)
        self.goto_login.click()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def email_empty(self, banner_type: str) -> str:
        return self.error_email.inner_text().strip()
    def password_empty(self, banner_type: str) -> str:
        return self.error_password.inner_text().strip()
    def get_error_message(self, banner_type: str) -> str:
        return self.invalid_email_or_password.inner_text().strip()

    def get_logged(self) -> str:
        return self.get_logged.inner_text().strip()
