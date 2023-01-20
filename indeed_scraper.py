# # Scrape job data from Indeed
# indeed_url = 'https://www.indeed.com/jobs?q=Data+Scientist'
import time
from loguru import logger

import pandas as pd
from pandas import DataFrame, Series
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger.level("DEBUG")


def scrape_listings(role: str = 'data scientist'):
    driver = _load_driver()
    results_df = _scrape_results_for_all_pages(driver, role)
    results_df.to_csv('dice_data_scientist_roles.csv')
    driver.quit()


def _load_driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.get("https://www.indeed.com/jobs?q=Data+Scientist")
    driver.implicitly_wait(10)
    return driver


def _scrape_results_for_all_pages(driver, role) -> DataFrame:
    with open('indeed_data_scientist_roles.csv', 'a') as f:
        f.write('position,rating,location,company_name,salary,posted_date,description\n')
    for page in range(150):
        logger.info(f'scraping page: {page}')
        _scrape_listings_on_page(driver)
        try:
            _scroll_to_next_page(driver)
        except Exception as error:
            print(error)


def _scrape_listings_on_page(driver: WebDriver) -> None:
    i = 0
    for posting in driver.find_elements(By.CLASS_NAME, "job_seen_beacon"):
        position, rating, location, company_name, salary, posted_date, description = '', '', '', '', '', '', ''
        if posting.find_elements(By.CLASS_NAME, "jobTitle"):
            position = posting.find_element(By.CLASS_NAME, "jobTitle").text
        if posting.find_elements(By.CLASS_NAME, "ratingsDisplay withRatingLink"):
            rating = posting.find_element(By.CLASS_NAME, "ratingsDisplay withRatingLink").text
        if posting.find_elements(By.CLASS_NAME, "companyLocation"):
            location = posting.find_element(By.CLASS_NAME, "companyLocation").text
        if posting.find_elements(By.CLASS_NAME, "companyName"):
            company_name = posting.find_element(By.CLASS_NAME, "companyName").text
        if posting.find_elements(By.CLASS_NAME, "attribute_snippet"):
            salary = posting.find_elements(By.CLASS_NAME, "attribute_snippet")[0].text
        if not salary and posting.find_elements(By.CLASS_NAME, "estimated-salary"):
            salary = posting.find_element(By.CLASS_NAME, "estimated-salary").text
        if posting.find_elements(By.CLASS_NAME, "date"):
            posted_date = posting.find_element(By.CLASS_NAME, "date").text
        if posting.find_elements(By.CLASS_NAME, "job-snippet"):
            description = posting.find_element(By.CLASS_NAME, "job-snippet").text
        _save_posting(position, rating, location, company_name, salary, posted_date, description)
        print(f'{i} posting on page')
        i += 1


def _save_posting(position, rating, location, company_name, salary, posted_date, description):
    position = ' '.join(position.split()).replace('~', '-')
    rating = ' '.join(rating.split()).replace('~', '-')
    location = ' '.join(location.split()).replace('~', '-')
    company_name = ' '.join(company_name.split()).replace('~', '-')
    salary = ' '.join(salary.split()).replace('~', '-')
    posted_date = ' '.join(posted_date.split()).replace('~', '-')
    description = ' '.join(description.split()).replace('~', '-')
    posting = f'{position}~{rating}~{location}~{company_name}~{salary}~{posted_date}~{description}\n'
    with open('indeed_data_scientist_roles.csv', 'a') as f:
        f.write(posting)
    print(posting)


def _scroll_to_next_page(driver: WebDriver) -> None:
    # scroll to next page by clicking button identified with data-testid="pagination-page-next"
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next Page"]')))
    next_button.click()
    time.sleep(5)  # program needs to wait for website to catch up


if __name__ == "__main__":
    scrape_listings()
