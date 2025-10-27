import pytest
from playwright.sync_api import sync_playwright, expect
from utils.data_utils import load_data
from pages.search_page_data import SearchPageData
from conftest import base_url  

# Load data từ Excel
test_data = load_data("Search_data.xlsx")

@pytest.mark.parametrize("Search,Expected", test_data)
def test_search_ddt(Search, Expected, base_url):   
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_page = SearchPageData(page, base_url)
        search_page.open()
        search_page.search("" if Search is None else str(Search))
        search_page.verify_search_result(Expected)

