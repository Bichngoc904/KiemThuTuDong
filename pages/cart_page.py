from playwright.sync_api import Page
from playwright.sync_api import Page, expect

class CartPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        #Thêm sản phẩm
        self._menu_san_pham = self.page.get_by_role("link", name="SẢN PHẨM", exact=True).first
        self.button_chiTiet = self.page.locator(".eye-img").first
        self.button_muaHang = self.page.get_by_role("button", name="Mua hàng")
        # Popup giỏ hàng
        self.icon_cart = self.page.get_by_role("link", name="Kún Miu Pet shop & grooming 1").locator("div").first
        self.popup_cart = self.page.locator("div.top-cart-content.arrow_box")
        self.popup_title = self.page.get_by_text("Sản phẩm đã cho vào giỏ hàng")
        self.popup_product_list = self.page.locator("div.top-cart-content.arrow_box ul#cart-sidebar li.item")
        self.popup_delete_icon = self.page.get_by_role("link", name="")
        self.popup_button_cart = self.page.locator("button.view-cart")
        self.popup_button_checkout = self.page.get_by_role("button", name="Thanh toán")
        # Trang giỏ hàng chi tiết
        #self.product_rows = self.page.locator("css=.cart-page .cart-item")
        self.product_name = self.page.locator("td h2.product-name a")
        self.product_price = self.page.get_by_text("₫").nth(2)
        self.product_quantity_input = self.page.get_by_role("textbox", name="Qty")
        self.product_subtotal = self.page.get_by_text("₫").nth(3)
        self.product_delete = self.page.get_by_role("link", name="")
        self.total_amount = self.page.locator("#shopping-cart-totals-table").get_by_role("cell", name="₫")
        self.update_quantity_button = self.page.get_by_role("button", name="Cập nhật số lượng")
        self.continue_shopping_button = self.page.get_by_role("button", name="Tiếp tục mua hàng")
        self.checkout_button = self.page.get_by_role("button", name="Tiến hành thanh toán")
        self.empty_cart_message = self.page.locator("text=Không có sản phẩm nào trong giỏ hàng")

    # ---------------- Popup Giỏ Hàng ----------------
    def add_product_to_cart(self):
        """Thêm sản phẩm vào giỏ hàng từ trang chi tiết sản phẩm"""
        self._menu_san_pham.click()
        self.page.goto(self.base_url, wait_until="domcontentloaded", timeout=60000)
        self.page.evaluate("window.scrollTo(0, 500)")
        self.button_chiTiet.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)
        self.button_chiTiet.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.button_muaHang.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(500)
        self.button_muaHang.click()
        self.page.wait_for_timeout(2000)

    def hover_cart_icon(self):
        """Hover chuột vào icon giỏ hàng để hiện popup"""
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        if self.icon_cart.is_visible(timeout=2000):
            self.icon_cart.hover()
        else:
            print("Popup cart icon is not visible (giỏ hàng có thể trống)")

    def is_popup_visible(self):
        """Kiểm tra xem popup giỏ hàng có hiển thị hay không"""
        return self.popup_cart.is_visible()
    def delete_product_in_popup(self, index=0):
        """Xóa sản phẩm trong popup giỏ hàng"""
        self.popup_delete_icon.nth(index).click()
    def go_to_cart_page_from_popup(self):
        """Đi đến trang giỏ hàng từ popup"""
        self.popup_button_cart.click()
    def go_to_checkout_from_popup(self):
        """Đi đến trang thanh toán từ popup"""
        self.popup_button_checkout.click()
    
    # ---------------- Trang Giỏ Hàng Chi Tiết ----------------
    def get_product_name(self) -> str:
        """Lấy tên sản phẩm trong giỏ hàng"""
        return self.product_name.inner_text().strip()
    def get_product_price(self) -> str:
        """Lấy giá sản phẩm trong giỏ hàng"""
        return self.product_price.inner_text().strip()
    def get_product_quantity(self) -> str:
        """Lấy số lượng sản phẩm trong giỏ hàng"""
        #return self.product_quantity_input.input_value().strip()
        quantity_value = self.product_quantity_input.input_value()
        return int(quantity_value) if quantity_value.isdigit() else 0
    def get_product_subtotal(self) -> str:
        """Lấy thành tiền sản phẩm trong giỏ hàng"""
        return self.product_subtotal.inner_text().strip()
    def delete_product_in_cart(self):
        """Xóa sản phẩm trong giỏ hàng chi tiết"""
        self.product_delete.click()
    def get_total_amount(self) -> str:
        """Lấy tổng tiền trong giỏ hàng"""
        # return self.total_amount.inner_text().strip()
        text = self.total_amount.inner_text()
        digits = ''.join(filter(str.isdigit, text))
        return int(digits) if digits else 0
    def update_quantity(self, quantity: str):
        """Cập nhật số lượng sản phẩm trong giỏ hàng"""
        self.product_quantity_input.fill(str(quantity))
        self.update_quantity_button.click()
    def continue_shopping(self):
        """Tiếp tục mua sắm"""
        self.continue_shopping_button.click()
    def checkout(self):
        """Tiến hành thanh toán"""
        self.checkout_button.click()
    def is_cart_empty(self) -> bool:
        """Kiểm tra giỏ hàng có trống hay không"""
        return self.empty_cart_message.is_visible()
    def open(self):
        """Mở trang giỏ hàng"""
        self.page.goto(f"{self.base_url}cart", wait_until="domcontentloaded", timeout=60000)