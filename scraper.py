# # Scrape job data from Hired
# hired_url = 'https://www.hired.com/search?q=software+developer&l=Seattle%2C+WA'
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


def scrape_dice_listings(role: str = 'data scientist'):
    driver = _load_driver()
    _load_page_for_role(driver, role)
    _scrape_results_for_all_pages(driver, role)
    driver.quit()


def _load_driver() -> WebDriver:
    driver = webdriver.Chrome()
    driver.get("https://www.dice.com")
    driver.implicitly_wait(10)
    return driver


def _load_page_for_role(driver: WebDriver, role: str) -> None:
    search_input = driver.find_element(By.XPATH, "//*[@placeholder='Job title, skills or company']")
    search_input.send_keys(role)
    search_input.submit()
    search_button = driver.find_element(By.ID, "submitSearch-button")
    search_button.click()
    driver.implicitly_wait(25)


def _scrape_results_for_all_pages(driver, role) -> DataFrame:
    results_df = DataFrame()
    for page in range(50):
        logger.info(f'scraping page: {page}')
        page_results_df = _scrape_listings_on_page(driver)
        if _is_role_not_present_on_page(page_results_df.positions, role):
            return results_df
        results_df = pd.concat([results_df, page_results_df], axis=0)
        try:
            _scroll_to_next_page(driver)
        except Exception as error:
            print(error)


def _is_role_not_present_on_page(positions_on_page: Series, role: str) -> bool:
    return all(positions_on_page.str.lower().apply(lambda row: role not in row))


def _scrape_listings_on_page(driver: WebDriver) -> DataFrame:
    results_df = DataFrame()
    results_df['positions'] = _get_positions(driver)
    results_df['locations'] = _get_locations(driver)
    results_df['company_names'] = _get_company_names(driver)
    results_df['posted_dates'] = _get_posted_dates(driver)
    results_df['descriptions'] = _get_descriptions(driver)
    return results_df


def _get_positions(driver: WebDriver) -> list[str]:
    position_elements = driver.find_elements(By.CSS_SELECTOR, ".card-title-link.bold")
    return [position.text for position in position_elements]


def _get_locations(driver: WebDriver) -> list[str]:
    location_elements = driver.find_elements(By.CLASS_NAME, "search-result-location")
    return [loc.text for loc in location_elements]


def _get_company_names(driver: WebDriver) -> list[str]:
    company_names_elements = driver.find_elements(By.XPATH, "//*[@data-cy='search-result-company-name']")
    return [x.text for x in company_names_elements]


def _get_posted_dates(driver: WebDriver) -> list[str]:
    posted_dates_elements = driver.find_elements(By.XPATH, "//*[@data-cy='card-posted-date']")
    return [x.text for x in posted_dates_elements]


def _get_descriptions(driver: WebDriver) -> list[str]:
    descriptions_elements = driver.find_elements(By.XPATH, "//*[@data-cy='card-summary']")
    return [x.text for x in descriptions_elements]


def _scroll_to_next_page(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.pagination-next.page-item.ng-star-inserted > a.page-link"))
    )
    next_button.click()
    time.sleep(1)  # program needs to wait for website to catch up


if __name__ == "__main__":
    scrape_dice_listings()
