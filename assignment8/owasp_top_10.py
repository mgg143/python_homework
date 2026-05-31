import os
import json
import shutil
import pandas as pd

# Selenium imports for browser automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_headless_driver():
    """Creates a headless Selenium driver using the best available browser."""
    if shutil.which("firefox"):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        options = webdriver.EdgeOptions()
        options.add_argument("--headless")
        options.binary_location = edge_path
        return webdriver.Edge(options=options)

    if shutil.which("chrome") or shutil.which("chrome.exe"):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=options)

    raise RuntimeError("No usable browser found.")


def scrape_owasp_top_10():
    target_url = "https://owasp.org/Top10/2025/"

    print("[INFO] Starting browser...")
    driver = initialize_headless_driver()
    results = []

    try:
        print(f"[INFO] Navigating to: {target_url}")
        driver.get(target_url)

        # Wait up to 10 seconds for the vulnerability list structure to appear
        print("[INFO] Waiting for page content to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article ol li a"))
        )

        # Find all 10 vulnerability link elements
        vulnerability_links = driver.find_elements(By.CSS_SELECTOR, "article ol li a")
        print(f"[SUCCESS] Found {len(vulnerability_links)} items in the list.")

        # Loop through the links and extract information
        for idx, link in enumerate(vulnerability_links, start=1):
            try:
                vulnerability_name = link.text.strip()
                vulnerability_url = link.get_attribute("href")

                print(f"  Scraped #{idx}: {vulnerability_name}")

                results.append(
                    {
                        "Rank": idx,
                        "Vulnerability": vulnerability_name,
                        "URL": vulnerability_url,
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


if __name__ == "__main__":
    # Run the scraper
    top_10_data = scrape_owasp_top_10()

    if top_10_data:
        # Convert to DataFrame
        df = pd.DataFrame(top_10_data)

        print("\n--- Scraped Data Preview ---")
        print(df.to_string(index=False))

        # Save to CSV
        csv_filename = "owasp_top_10.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"\n[SUCCESS] Saved CSV file: {csv_filename}")

        # Save to JSON
        json_filename = "owasp_top_10.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(top_10_data, json_file, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Saved JSON file: {json_filename}")
    else:
        print("[WARNING] No data was collected. Files were not overwritten.")