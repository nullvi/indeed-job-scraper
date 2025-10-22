"""
Indeed Job Listings Scraper
============================

A professional web scraper that extracts job listing data from Indeed.com
with advanced anti-bot detection and human-like behavior simulation.

Author: Ulvi Durmaz
GitHub: https://github.com/nullvi
License: MIT

Features:
- Automatic pagination
- Anti-bot detection bypass
- Human behavior simulation
- Configurable page limits
- JSON data export
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import random

# ============================================================
# CONFIGURATION
# ============================================================
# Maximum number of pages to scrape
# Set to None to scrape all available pages
# Example: MAX_PAGES = 10 (scrapes only first 10 pages)
#          MAX_PAGES = None (scrapes all pages)
MAX_PAGES = 10
# ============================================================

def scrape_indeed_jobs(url, max_pages=None):
    """
    Scrapes job listing data from Indeed
    
    Args:
        url (str): Indeed search URL
        max_pages (int, optional): Maximum number of pages to scrape. 
                                   If None, scrapes all available pages.
    
    Returns:
        list: List of job listings with title, company, location, and link
    """
    
    # Chrome settings - Anti-bot detection
    chrome_options = Options()
    
    # Window settings
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Disable automation flags
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Add realistic User-Agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Additional anti-detection settings
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Set preferences to avoid detection
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Start WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Hide webdriver property to avoid detection
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    try:
        print("Navigating to Indeed page...")
        driver.get(url)
        
        # Wait for page to fully load - increased time for Cloudflare
        print("Loading page and waiting for Cloudflare check...")
        time.sleep(8)  # Increased from 5 to 8 seconds
        
        # Simulate human behavior - scroll down and up
        print("Simulating human behavior...")
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1.5))
        
        job_listings = []
        page_number = 1
        
        # Loop through all pages
        while True:
            print(f"\n{'='*60}")
            print(f"Scraping Page {page_number}")
            print(f"{'='*60}\n")
            
            # Find job listings - with explicit wait
            print("Waiting for job listings...")
            wait = WebDriverWait(driver, 20)
            jobs = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
            )
            
            # Small random scroll to simulate reading
            driver.execute_script(f"window.scrollTo(0, {random.randint(200, 400)});")
            time.sleep(random.uniform(0.5, 1))
            
            print(f"Found {len(jobs)} job listings on this page.\n")
            
            for index, job in enumerate(jobs, 1):
                try:
                    job_data = {}
                    
                    # Job Title
                    title = ""
                    # Method 1: Using id pattern (jobTitle-)
                    try:
                        title_element = job.find_element(By.CSS_SELECTOR, "span[id^='jobTitle-']")
                        title = title_element.text
                    except:
                        pass
                    
                    # Method 2: XPath with id pattern
                    if not title:
                        try:
                            title_element = job.find_element(By.XPATH, ".//span[starts-with(@id,'jobTitle-')]")
                            title = title_element.text
                        except:
                            pass
                    
                    # Method 3: h2 with jobTitle class
                    if not title:
                        try:
                            title_element = job.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]")
                            title = title_element.text
                        except:
                            pass
                    
                    # Method 4: Any h2 tag
                    if not title:
                        try:
                            title_element = job.find_element(By.TAG_NAME, "h2")
                            title = title_element.text
                        except:
                            pass
                    
                    job_data['title'] = title if title else "Title not found"
                    
                    # Company Name - Using data-testid
                    company = ""
                    
                    # Method 1: data-testid (most reliable)
                    try:
                        company = job.find_element(By.CSS_SELECTOR, "span[data-testid='company-name']").text
                        if company:
                            company = company.strip()
                    except:
                        pass
                    
                    # Method 2: XPath with data-testid
                    if not company:
                        try:
                            company = job.find_element(By.XPATH, ".//span[@data-testid='company-name']").text
                            if company:
                                company = company.strip()
                        except:
                            pass
                    
                    # Method 3: JavaScript with data-testid
                    if not company:
                        try:
                            company = driver.execute_script(
                                "return arguments[0].querySelector('span[data-testid=\"company-name\"]')?.textContent?.trim();", 
                                job
                            )
                        except:
                            pass
                    
                    # Method 4: Legacy method - companyName class (fallback)
                    if not company:
                        try:
                            company = job.find_element(By.CSS_SELECTOR, "span.companyName").text
                        except:
                            pass
                    
                    # Method 5: XPath contains class
                    if not company:
                        try:
                            company = job.find_element(By.XPATH, ".//span[contains(@class, 'companyName')]").text
                        except:
                            pass
                    
                    job_data['company'] = company if company else "Company not found"
                    
                    # Location - Using data-testid
                    location = ""
                    
                    # Method 1: data-testid (most reliable)
                    try:
                        location = job.find_element(By.CSS_SELECTOR, "div[data-testid='text-location']").text
                        if location:
                            location = location.strip()
                    except:
                        pass
                    
                    # Method 2: XPath with data-testid
                    if not location:
                        try:
                            location = job.find_element(By.XPATH, ".//div[@data-testid='text-location']").text
                            if location:
                                location = location.strip()
                        except:
                            pass
                    
                    # Method 3: JavaScript with data-testid
                    if not location:
                        try:
                            location = driver.execute_script(
                                "return arguments[0].querySelector('div[data-testid=\"text-location\"]')?.textContent?.trim();", 
                                job
                            )
                        except:
                            pass
                    
                    # Method 4: Legacy method - companyLocation class (fallback)
                    if not location:
                        try:
                            location = job.find_element(By.CSS_SELECTOR, "div.companyLocation").text
                        except:
                            pass
                    
                    # Method 5: XPath contains class
                    if not location:
                        try:
                            location = job.find_element(By.XPATH, ".//div[contains(@class, 'companyLocation')]").text
                        except:
                            pass
                    
                    job_data['location'] = location if location else "Location not found"
                    
                    # Job Link
                    try:
                        link_element = job.find_element(By.XPATH, ".//h2[contains(@class, 'jobTitle')]//a")
                        job_data['link'] = link_element.get_attribute("href")
                    except:
                        job_data['link'] = "Link not found"
                    
                    job_listings.append(job_data)
                    
                    # Print job information
                    print(f"=== Job {index} (Page {page_number}) ===")
                    print(f"Title: {job_data['title']}")
                    print(f"Company: {job_data['company']}")
                    print(f"Location: {job_data['location']}")
                    print(f"Link: {job_data['link']}")
                    print()
                    
                except Exception as e:
                    print(f"Error for job {index}: {str(e)}")
                    continue
            
            # Check if we've reached the maximum number of pages
            if max_pages is not None and page_number >= max_pages:
                print(f"\n✓ Reached the maximum page limit ({max_pages} pages).")
                print("Stopping scraper as configured.")
                break
            
            # Try to go to next page
            print(f"\nFinished scraping page {page_number}. Looking for next page...")
            
            try:
                # Find and click the 'Next Page' button
                next_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")
                
                # Scroll to the button to make sure it's visible
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                
                # Random wait to mimic human behavior (1-3 seconds)
                time.sleep(random.uniform(1.5, 3.0))
                
                # Click the next button
                next_button.click()
                print(f"✓ Moving to page {page_number + 1}...")
                
                # Wait for the next page to load - increased and randomized
                wait_time = random.uniform(6, 9)
                print(f"Waiting {wait_time:.1f} seconds for page to load...")
                time.sleep(wait_time)
                page_number += 1
                
            except Exception as e:
                # No next button found - we're on the last page
                print(f"✓ Reached the last page (Page {page_number}).")
                print("No more pages to scrape.")
                break
        
        # Save data to JSON file
        with open('job_listings.json', 'w', encoding='utf-8') as f:
            json.dump(job_listings, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Successfully scraped {len(job_listings)} job listings!")
        print("✓ Data saved to 'job_listings.json'.")
        
        return job_listings
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []
        
    finally:
        # Close browser
        print("\nClosing browser...")
        driver.quit()


if __name__ == "__main__":
    url = "https://www.indeed.com/jobs?q=software%20developer&vjk=7b8ec8506fc0214d"
    
    print("=" * 60)
    print("Indeed Job Listings Scraper")
    print("=" * 60)
    
    if MAX_PAGES:
        print(f"Configuration: Scraping first {MAX_PAGES} pages")
    else:
        print("Configuration: Scraping all available pages")
    
    print()
    
    jobs = scrape_indeed_jobs(url, max_pages=MAX_PAGES)
    
    print("\nProgram completed!")
