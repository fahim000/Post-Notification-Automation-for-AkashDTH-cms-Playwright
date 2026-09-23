from pathlib import Path
from math import ceil
import re

from playwright.sync_api import sync_playwright

# ==================================================
# CONFIG
# ==================================================

KV_FOLDER = Path(
    r"C:\Users\mfm\OneDrive - AKASH Digital TV\Pictures\Akash\KV"
)

CDN_PREFIX = (
    "https://cdnhost.akashbd.net/assets/uploads/pack_cate/"
)

OUTPUT_FILE = "output.txt"

# ==================================================
# HELPERS
# ==================================================

def get_last_page(page):
    """
    Reads:
    Displaying : 631 To 634 Of 634

    Returns:
    64
    """

    body_text = page.locator("body").inner_text()

    match = re.search(r"Displaying\s*:\s*\d+\s*To\s*\d+\s*Of\s*(\d+)", body_text)

    if not match:
        raise Exception("Could not determine total record count.")

    total_records = int(match.group(1))

    return ceil(total_records / 10)

# ==================================================
# START
# ==================================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        channel="msedge",
        headless=False
    )

    context = browser.new_context(
        storage_state="state.json"
    )

    page = context.new_page()

    # Fresh output file every run
    open(OUTPUT_FILE, "w", encoding="utf-8").close()

    images = []

    for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
        images.extend(KV_FOLDER.glob(ext))

    print(f"\nFound {len(images)} image(s)\n")

    for image_file in images:

        print("=" * 60)
        print("Uploading:", image_file.name)

        # ------------------------------------------
        # OPEN IMAGE LINKS
        # ------------------------------------------

        page.goto(
            "https://akashdth.com/admin_panel/imagelink"
        )

        page.wait_for_load_state("networkidle")

        # ------------------------------------------
        # CREATE
        # ------------------------------------------

        page.locator(
            'a[data-original-title="Create"]'
        ).click()

        page.wait_for_timeout(1000)

        # ------------------------------------------
        # UPLOAD IMAGE
        # ------------------------------------------

        page.set_input_files(
            "#image_1",
            str(image_file)
        )

        print("File selected")

        # ------------------------------------------
        # SAVE
        # ------------------------------------------

        page.locator(
            'button[type="submit"]'
        ).click()

        print("Save clicked")

        page.wait_for_timeout(3000)

        # ------------------------------------------
        # GO TO LAST PAGE
        # ------------------------------------------

        last_page = get_last_page(page)

        print("Last page =", last_page)

        page.get_by_text(
            str(last_page),
            exact=True
        ).click()

        page.wait_for_timeout(2000)

        # ------------------------------------------
        # LAST ROW = NEWEST IMAGE
        # ------------------------------------------

        last_row = page.locator(
            "tr.editable"
        ).last

        image_cell = last_row.locator(
            '[data-field="image_1"]'
        )

        filename = image_cell.get_attribute(
            "data-values"
        )

        if not filename:
            raise Exception(
                f"Could not extract filename for {image_file.name}"
            )

        # ------------------------------------------
        # BUILD URL
        # ------------------------------------------

        final_url = CDN_PREFIX + filename

        print("Filename :", filename)
        print("URL      :", final_url)

        # ------------------------------------------
        # WRITE OUTPUT
        # ------------------------------------------

        with open(
            OUTPUT_FILE,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(final_url + "\n")

    print("\n" + "=" * 60)
    print("DONE!")
    print(f"URLs saved to: {OUTPUT_FILE}")
    print("=" * 60)

    browser.close()