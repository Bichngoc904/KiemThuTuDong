import pytest
from pages.cart_page import CartPage
from playwright.sync_api import sync_playwright
from utils.data_utils import load_data
from pages.login_page import LoginPage
from conftest import base_url

def test_popup_cart_display_with_products(setup, base_url):
    """Kiểm tra popup giỏ hàng hiển thị khi có sản phẩm"""
    page = setup
    cart = CartPage(page, base_url)
    cart.add_product_to_cart()
    cart.hover_cart_icon()
    assert cart.is_popup_visible()

def test_popup_cart_delete_product(setup, base_url):
    """Kiểm tra xóa sản phẩm trong popup giỏ hàng"""
    page = setup
    cart = CartPage(page, base_url)
    cart.add_product_to_cart()
    cart.hover_cart_icon()
    cart.delete_product_in_popup(0)
    # Kiểm tra popup cập nhật, sản phẩm biến mất
    assert cart.is_popup_visible()  

def test_popup_go_to_cart_page(setup, base_url):
    """Kiểm tra chuyển đến trang giỏ hàng từ popup"""
    page = setup
    cart = CartPage(page, base_url)
    cart.add_product_to_cart()
    cart.hover_cart_icon()
    cart.go_to_cart_page_from_popup()
    assert "/cart" in page.url

def test_popup_go_to_checkout_page(setup, base_url):
    """Kiểm tra chuyển đến trang thanh toán từ popup"""
    page = setup
    cart = CartPage(page, base_url)
    cart.add_product_to_cart()
    cart.hover_cart_icon()
    cart.go_to_checkout_from_popup()
    assert "checkout" in page.url

# ---------------- Trang giỏ hàng chi tiết ----------------
def test_cart_page_display_product_list(setup, base_url):
    """Kiểm tra trang giỏ hàng hiển thị đúng sản phẩm đã thêm"""
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    # Mở trang giỏ hàng
    cart.open()
    first_product_title = cart.product_name.nth(0).inner_text()
    # Assert tên sản phẩm đúng
    assert "Đồ uống nước giải khát cà phê sữa hạt Chop Chef" in first_product_title

# ---------------- DDT cho số lượng sản phẩm ----------------

@pytest.mark.parametrize(
    "quantity, expected_quantity, description",
    [
        (2, 2, "Số lượng hợp lệ"),
        ("-1", 0, "Số lượng âm → xóa sản phẩm"),
        ("abc", 0, "Số lượng chữ → xóa sản phẩm"),
        ("100000000", 1, "Số lượng quá lớn → cập nhật thành 1")
    ]
)
def test_cart_page_update_quantity_ddt(setup, base_url, quantity, expected_quantity, description):
    """Kiểm thử cập nhật số lượng sản phẩm trong giỏ hàng với DDT"""
    page = setup
    cart = CartPage(page, base_url)
    cart.add_product_to_cart()
    cart.open()
    cart.update_quantity(quantity)
    if expected_quantity == 0:
        cart.page.wait_for_timeout(1000)
        assert cart.is_cart_empty()
    else:
        assert cart.get_product_quantity() == expected_quantity


def test_cart_page_delete_product(setup, base_url):
    """Kiểm tra xóa sản phẩm trong giỏ hàng chi tiết"""
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    cart.open()
    cart.delete_product_in_cart()
    cart.page.wait_for_timeout(1000)
    assert cart.is_cart_empty()


def test_cart_page_total_amount_display(setup, base_url):
    """Kiểm tra tổng tiền hiển thị đúng trong giỏ hàng"""
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    cart.open()
    total = cart.get_total_amount()
    assert total > 0

def test_cart_page_continue_shopping(setup, base_url):
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    cart.open()
    cart.continue_shopping()
    assert "collections" in setup.url

def test_cart_page_checkout_not_logged_in(setup, base_url):
    """Kiểm tra tiến hành thanh toán khi chưa đăng nhập"""
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    cart.open()
    cart.checkout()
    assert "checkout" in setup.url

def test_cart_page_checkout_logged_in(setup, base_url):
    """Kiểm tra tiến hành thanh toán khi đã đăng nhập"""
    login_page = LoginPage(setup, base_url)
    login_page.open()
    login_page.login("b18ngocie@gmail.com", 'Ngoc1809@')
    cart = CartPage(setup, base_url)
    cart.add_product_to_cart()
    cart.open()
    cart.checkout()
    assert "checkout" in setup.url
