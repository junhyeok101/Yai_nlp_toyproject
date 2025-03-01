import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def scrape_airbnb_review_urls(base_url, max_urls=5000):
    """Scrapes Airbnb review URLs until reaching the target count (5,000)."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    time.sleep(random.uniform(4, 7))
    
    review_urls = set()
    page_num = 0
    
    while len(review_urls) < max_urls:
        page_num += 1
        print(f"Scraping page {page_num}... (Collected: {len(review_urls)} URLs)")
        
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/rooms/") and not(contains(@href, "reviews"))]')))
            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/rooms/") and not(contains(@href, "reviews"))]')
            
            for listing in listings:
                try:
                    listing_url = listing.get_attribute("href")
                    if listing_url and listing_url.startswith("http"):
                        review_url = listing_url.split("?")[0] + "/reviews"
                        review_urls.add(review_url)
                except:
                    continue
            
            if len(review_urls) >= max_urls:
                break
            
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@aria-label, "다음") or contains(@aria-label, "Next")]')))
            next_button.send_keys(Keys.ENTER)
            time.sleep(random.uniform(4, 7))
            wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/rooms/") and not(contains(@href, "reviews"))]')))
        except:
            print("No more pages found or unable to load next page.")
            break
    
    driver.quit()
    
    with open("airbnb_review_urls7.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Review URL"])
        for url in list(review_urls)[:max_urls]:  # Ensure only 5000 URLs are saved
            writer.writerow([url])
    
    print(f"\nSuccessfully saved {len(review_urls)} review URLs to airbnb_review_urls7.csv")

# User Input
base_url = input("Enter the Airbnb search URL: ").strip()
scrape_airbnb_review_urls(base_url)
