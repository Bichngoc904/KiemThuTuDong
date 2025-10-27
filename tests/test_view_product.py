
import pytest
from playwright.sync_api import sync_playwright
from pages.view_product_page import ViewProductPage
from utils.data_utils import load_data
from conftest import base_url

# Load dữ liệu từ file JSON
test_data = load_data("view_product_data.json")

@pytest.mark.parametrize("data", test_data)
def test_view_product_details(base_url, data):
    """Kiểm thử nhiều sản phẩm theo dữ liệu DDT"""
    slug = data["slug"]
    expected_name = data["expected_name"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        view_product = ViewProductPage(page, base_url)
        view_product.open(slug)

        view_product.verify_product_name(expected_name)
        view_product.verify_buy_button_visible()

        browser.close()

test_data_price_filter = load_data("filter_product_data.csv")
@pytest.mark.parametrize("price_label, expected_first_price", test_data_price_filter)
def test_filter_by_price_range(base_url, price_label, expected_first_price):
    """Kiểm thử lọc sản phẩm theo khoảng giá và verify giá sản phẩm đầu tiên"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        view_product = ViewProductPage(page, base_url)
        view_product.filter_by_price_range(price_label, expected_first_price)