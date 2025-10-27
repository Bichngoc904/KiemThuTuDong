
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ViewProductPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

        # Locators
        self._menu_san_pham = self.page.get_by_role("link", name="SẢN PHẨM", exact=True).first
        self._product_name = "div.product-name h1"
        self._verify_price = "p.special-price span.price"
        self._verify_buy_button = "button.button.btn-cart.add_to_cart:has-text('Mua hàng')"

        # ===== Locators cho lọc khoảng giá =====
        self._filter_price_group = self.page.locator(
            "div.filter-group:has(.filter-group-title:has-text('Khoảng giá'))"
        )

    # Thêm hàm locator động cho checkbox khoảng giá
    def _filter_price_checkbox(self, price_label: str):
        """Trả về locator checkbox tương ứng với khoảng giá"""
        return self.page.locator(f"label:has-text('{price_label}') input[type='checkbox']")

    def open(self, product_id: str):
        """Mở trực tiếp trang chi tiết sản phẩm"""
        self.page.goto(f"{self.base_url}{product_id}", wait_until="domcontentloaded", timeout=60000)

    def get_button_chi_tiet(self, slug: str):
        """Locator cho nút Chi tiết"""
        return f"a.button.btn-cart[href='/{slug}']:has-text('Chi tiết')"

    def view_product_details(self, slug: str):
        """Đi từ menu SẢN PHẨM đến trang chi tiết"""
        self._menu_san_pham.click()

        self.page.wait_for_selector("div#category-products .row.masonry-container", timeout=20000)

        chi_tiet_btn = self.page.locator(self.get_button_chi_tiet(slug))
        expect(chi_tiet_btn).to_be_visible(timeout=10000)
        chi_tiet_btn.click()

    def get_product_name(self) -> str:
        """Lấy tên sản phẩm"""
        return self.page.locator(self._product_name).inner_text().strip()

    def get_product_price(self) -> str:
        """Lấy giá sản phẩm"""
        return self.page.locator(self._verify_price).inner_text().strip()

    def get_buy_button(self):
        """Lấy locator nút Mua hàng"""
        return self.page.locator(self._verify_buy_button)

    def verify_product_name(self, expected_name: str):
        actual_name = self.get_product_name()
        assert actual_name.lower() == expected_name.lower(), (
            f"Tên sản phẩm không đúng!\nExpected: {expected_name!r}\nGot: {actual_name!r}"
        )

    def verify_product_price(self, expected_price: str):
        actual_price = self.get_product_price()
        assert actual_price == expected_price, (
            f"Giá sản phẩm không đúng! expected: {expected_price!r}, got: {actual_price!r}"
        )

    def verify_buy_button_visible(self):
        """Kiểm tra nút Mua hàng hiển thị"""
        buy_button = self.get_buy_button()
        expect(buy_button).to_be_visible()

    
    def filter_by_price_range(self, price_label: str, expected_first_price: str):
        """Chọn khoảng giá (VD: '0đ - 50000đ') và kiểm tra giá sản phẩm đầu tiên hiển thị"""
        # Vào trang chủ
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=60000)
        # Click menu SẢN PHẨM
        self._menu_san_pham.wait_for(state="visible", timeout=20000)
        self._menu_san_pham.click()
        # Chờ nhóm lọc khoảng giá hiển thị
        self._filter_price_group.wait_for(state="visible", timeout=10000)
        # Lấy label checkbox theo price_label
        price_label_locator = self._filter_price_group.locator(f"label:has-text('{price_label}')")
        expect(price_label_locator).to_be_visible(timeout=10000)
        # Lấy giá sản phẩm đầu tiên trước khi filter
        first_price_locator = self.page.locator("div.col-item").first.locator("div.price-box span.price")
        old_price = first_price_locator.inner_text().strip() if first_price_locator.count() > 0 else ""
        # Scroll và click label
        price_label_locator.scroll_into_view_if_needed()
        price_label_locator.click()
        # chờ sp hiển thị
        self.page.wait_for_timeout(2000)
        # Lấy giá sản phẩm đầu tiên sau khi lọc
        first_price_locator = self.page.locator("div.col-item").first.locator("div.price-box span.price")
        first_price = first_price_locator.inner_text().strip()
        # Kiểm tra giá
        assert first_price == expected_first_price, (
            f"Giá sản phẩm đầu tiên không đúng!\nExpected: {expected_first_price!r}\nGot: {first_price!r}"
        )

