# conftest.py
# Pytest fixtures for browser setup/teardown
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from utils.report_helper import log_test_result


@pytest.fixture(scope="session")
def base_url():
    return "https://kunmiu.com/"

@pytest.fixture(scope="function")
def setup(base_url):
    """
    Fixture Playwright: mở Chromium có giao diện full 1920x1080.
    (Để bật quay video: bỏ comment record_video_dir/record_video_size)
    """
    with sync_playwright() as p:
        # Ép kích thước cửa sổ + bỏ qua lỗi HTTPS
        # browser = p.chromium.launch(
        #     headless=False,
        #     args=[
        #         "--window-size=1920,1080",
        #         "--ignore-certificate-errors"   # fix ERR_ABORTED nếu site SSL không chuẩn
        #     ]
        # )
        browser = p.chromium.launch(
        headless=False,
        channel="chrome",        # chuyển từ msedge -> chrome
        args=["--window-size=1920,1080"]
    )

        # Context với viewport + bỏ qua HTTPS errors
        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            ignore_https_errors=True
            # record_video_dir="videos",
            # record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        # Dùng domcontentloaded thay vì load để tránh timeout khi site có script chậm
        page.goto(base_url, wait_until="domcontentloaded", timeout=60000)

        # Đăng nhập trước khi chạy test
        # login_page = LoginPage(page, base_url)
        # login_page.login("b18ngocie@gmail.com", "Ngoc1809@")

        yield page  # trả page cho test

        # Đóng và giải phóng tài nguyên
        context.close()
        browser.close()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tự động log kết quả test (PASS/FAIL) sau khi chạy"""
    outcome = yield
    result = outcome.get_result()

    # Chỉ log sau khi phần "call" (test chính) hoàn tất
    if result.when == "call":
        test_name = item.name
        # Lấy toàn bộ tham số test (email, password, expected...)
        test_data = {
            name: value
            for name, value in item.funcargs.items()
            if not name.startswith("request")
        }

        if result.failed:
            log_test_result(test_name, test_data, "FAIL", str(result.longrepr))
        else:
            log_test_result(test_name, test_data, "PASS")
