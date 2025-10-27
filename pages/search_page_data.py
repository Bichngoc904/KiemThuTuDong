from playwright.sync_api import Page
from playwright.sync_api import expect
from pages.base_page import BasePage

class SearchPageData(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

        self._search_input = "form.search-bar input[name='query']"
        self._search_button = "form.search-bar button"
        self._search_results = "header.page-header h2"

   # --- Mở trang ---
    def open(self):
        """Mở trang chủ hoặc trang tìm kiếm"""
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=60000)

    # --- Thao tác tìm kiếm ---
    def search(self, keyword: str):
        """Điền từ khóa và click tìm kiếm"""
        self.page.locator(self._search_input).fill(str(keyword))
        self.page.locator(self._search_button).click()

    def click_search_button(self):
        """Click nút tìm kiếm"""
        self.page.locator(self._search_button).click()

    # --- Property để truy xuất locator ---
    @property
    def search_input(self):
        return self.page.locator(self._search_input)

    @property
    def search_button(self):
        return self.page.locator(self._search_button)

    @property
    def search_results(self):
        """Locator cho header kết quả tìm kiếm"""
        return self.page.locator(self._search_results)

    # --- Lấy giá trị ô tìm kiếm hiện tại ---
    def get_search_input_value(self) -> str:
        """Lấy giá trị đang có trong ô tìm kiếm"""
        return self.page.locator(self._search_input).input_value().strip()
    def verify_search_result(self, expected_text: str):
        """Kiểm tra header kết quả chứa expected substring"""
        expect(self.search_results).to_contain_text(expected_text, timeout=5000)