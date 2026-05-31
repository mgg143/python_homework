# ==============================================================================
# FILE: get_books.py
# DESCRIPTION:
#   This script automatically opens a web browser (in invisible "headless" mode),
#   visits the Durham County Library website, searches for books about
#   "learning Spanish", extracts book information, and saves the results to
#   both CSV and JSON files.
#
#   The script is designed to work on ANY computer:
#       1. It first tries to use Firefox if installed.
#       2. If Firefox is not installed, it tries Microsoft Edge.
#       3. If Edge is not installed, it tries Google Chrome.
#       4. If NO browser is installed, it uses a fallback:
#          a portable version of Firefox (FirefoxPortable + geckodriver.exe)
#
#   This makes the script extremely portable and beginner‑friendly.
# ==============================================================================

import os
import json
import shutil
import pandas as pd

# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Browser‑specific driver services
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService


# ==============================================================================
# FUNCTION: initialize_headless_driver()
# PURPOSE:
#   Creates a "headless" (invisible) web browser for Selenium to control.
#   The function tries several browsers in order of reliability.
#
#   WHY HEADLESS?
#       - The browser runs in the background.
#       - No window pops up.
#       - Uses fewer system resources.
#
#   WHY MULTIPLE BROWSER OPTIONS?
#       - Different computers have different browsers installed.
#       - This script adapts automatically.
# ==============================================================================

def initialize_headless_driver():
    """
    Creates a headless Selenium driver using the best available browser.
    Priority order:
        1. System Firefox
        2. System Edge
        3. System Chrome
        4. Portable Firefox fallback (bundled)
    """

    # ----------------------------------------------------------------------
    # 1. Try using system‑installed Firefox
    # ----------------------------------------------------------------------
    # shutil.which("firefox") checks if "firefox" exists on the system PATH.
    if shutil.which("firefox"):
        print("[INFO] Using system Firefox (best option)")
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # Run invisibly
        return webdriver.Firefox(options=options)

    # ----------------------------------------------------------------------
    # 2. Try using system‑installed Microsoft Edge
    # ---------------------------------------------------------------------- 
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    if os.path.exists(edge_path):
        print("[INFO] Using system Edge (manual path)")
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")
        options.binary_location = edge_path
        return webdriver.Edge(options=options)

    # ----------------------------------------------------------------------
    # 3. Try using system‑installed Google Chrome
    # ----------------------------------------------------------------------
    # Chrome is less reliable because ChromeDriver versions must match,
    # but we include it as a fallback.
    if shutil.which("chrome") or shutil.which("chrome.exe"):
        print("[INFO] Using system Google Chrome")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)

    # ----------------------------------------------------------------------
    # 4. FINAL FALLBACK — Portable Firefox
    # ----------------------------------------------------------------------
    # This allows the script to run even on a computer with NO browsers installed.
    portable_firefox = r"FirefoxPortable\FirefoxPortable.exe"
    gecko_driver = r"geckodriver.exe"

    if os.path.exists(portable_firefox) and os.path.exists(gecko_driver):
        print("[INFO] Using bundled Firefox Portable fallback")
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.binary_location = portable_firefox  # Tell Selenium where FirefoxPortable lives
        service = FirefoxService(executable_path=gecko_driver)
        return webdriver.Firefox(service=service, options=options)

    # ----------------------------------------------------------------------
    # If we reach this point, no browser is available at all.
    # ----------------------------------------------------------------------
    raise RuntimeError(
        "No usable browser found. Install Firefox, Edge, Chrome, or include FirefoxPortable + geckodriver.exe."
    )


# ==============================================================================
# FUNCTION: scrape_library_catalog()
# PURPOSE:
#   - Opens the library website
#   - Waits for the page to load
#   - Extracts book titles, authors, and format/year
#   - Returns a list of dictionaries
# ==============================================================================

def scrape_library_catalog():
    # The URL we want to scrape
    target_url = (
        "https://durhamcounty.bibliocommons.com/v2/search?"
        "query=learning%20spanish&searchType=smart"
    )

    print("[INFO] Starting browser...")
    driver = initialize_headless_driver()
    results = []

    try:
        print(f"[INFO] Navigating to: {target_url}")
        driver.get(target_url)

        # The page loads content dynamically using JavaScript.
        # We wait up to 10 seconds for the book list to appear.
        print("[INFO] Waiting for page content to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'li[data-test-id="searchResultItem"]')
            )
        )

        # Find all book result items on the page
        book_elements = driver.find_elements(
            By.CSS_SELECTOR, 'li[data-test-id="searchResultItem"]'
        )
        print(f"[SUCCESS] Found {len(book_elements)} books.")

        # Loop through each book result and extract details
        for idx, book in enumerate(book_elements, start=1):
            try:
                # -------------------------
                # Extract the book title
                # -------------------------
                title_element = book.find_element(
                    By.CSS_SELECTOR, '.title-content'
                )
                title_text = title_element.text.strip()

                # -------------------------
                # Extract authors (may be multiple)
                # -------------------------
                author_elements = book.find_elements(
                    By.CSS_SELECTOR, '.author-link'
                )

                if author_elements:
                    author_names = [
                        a.text.strip() for a in author_elements if a.text.strip()
                    ]
                    author_text = "; ".join(author_names)
                else:
                    author_text = "Unknown Author"

                # -------------------------
                # Extract format + year
                # -------------------------
                try:
                    format_element = book.find_element(
                        By.CSS_SELECTOR, ".display-info-primary"
                    )
                    format_year_text = (
                        format_element.text.strip().replace("\n", " ")
                    )
                except Exception:
                    format_year_text = "Format details unavailable"

                # Print progress
                print(f"  Scraped #{idx}: '{title_text}' by [{author_text}]")

                # Save the extracted data
                results.append(
                    {
                        "Title": title_text,
                        "Author": author_text,
                        "Format-Year": format_year_text,
                    }
                )

            except Exception as item_error:
                print(f"  [WARNING] Skipping item #{idx}: {item_error}")
                continue

    except Exception as global_error:
        print(f"[ERROR] Scraping failed: {global_error}")

    finally:
        print("[INFO] Closing browser...")
        driver.quit()

    return results


# ==============================================================================
# MAIN PROGRAM EXECUTION
# PURPOSE:
#   - Runs the scraper
#   - Converts results into a DataFrame
#   - Saves results to CSV and JSON files
# ==============================================================================

if __name__ == "__main__":
    # Run the scraping function
    scraped_books = scrape_library_catalog()

    # Convert results into a table-like structure
    df = pd.DataFrame(scraped_books)

    print("\n--- Scraped Data Preview ---")
    print(df.to_string())

    # Save to CSV
    csv_filename = "get_books.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"\n[SUCCESS] Saved CSV file: {csv_filename}")

    # Save to JSON
    json_filename = "get_books.json"
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(scraped_books, json_file, indent=4, ensure_ascii=False)
    print(f"[SUCCESS] Saved JSON file: {json_filename}")
