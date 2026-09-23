from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        channel="msedge",
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://akashdth.com/admin_panel")

    input(
        "\nLogin manually, open Image Links page, then press ENTER here..."
    )

    context.storage_state(path="state.json")

    print("Session saved to state.json")

    browser.close()