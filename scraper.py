# # Scrape job data from Hired
# hired_url = 'https://www.hired.com/search?q=software+developer&l=Seattle%2C+WA'
import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_dice_listings(role: str = 'data scientist'):
    driver = webdriver.Chrome()
    driver.get("https://www.dice.com")
    driver.implicitly_wait(10)
    search_input = driver.find_element(By.XPATH, "//*[@placeholder='Job title, skills or company']")
    search_input.send_keys(role)
    search_input.submit()
    search_button = driver.find_element(By.ID, "submitSearch-button")
    search_button.click()
    driver.implicitly_wait(25)

    # Scrape job data from all pages
    for i in range(20):
        try:
            _scrape_listings_on_page(driver)
        except Exception as error:
            print(error)

        _scroll_to_next_page(driver)
    driver.quit()


def _scrape_listings_on_page(driver):
    _get_positions(driver)
    _get_locations(driver)
    _get_company_names(driver)
    _get_posted_dates(driver)
    _get_descriptions(driver)


def _get_positions(driver: WebDriver):
    position_elements = driver.find_elements(By.CSS_SELECTOR, ".card-title-link.bold")
    return [position.text for position in position_elements]


def _get_locations(driver: WebDriver):
    location_elements = driver.find_elements(By.CLASS_NAME, "search-result-location")
    return [loc.text for loc in location_elements]


def _get_company_names(driver: WebDriver):
    company_names_elements = driver.find_elements(By.XPATH, "//*[@data-cy='search-result-company-name']")
    return [x.text for x in company_names_elements]


def _get_posted_dates(driver: WebDriver):
    posted_dates_elements = driver.find_elements(By.XPATH, "//*[@data-cy='card-posted-date']")
    return [x.text for x in posted_dates_elements]


def _get_descriptions(driver: WebDriver):
    descriptions_elements = driver.find_elements(By.XPATH, "//*[@data-cy='card-summary']")
    return [x.text for x in descriptions_elements]


def _scroll_to_next_page(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.pagination-next.page-item.ng-star-inserted > a.page-link"))
    )
    next_button.click()
    time.sleep(5)  # program needs to wait for website to catch up


if __name__ == "__main__":
    scrape_dice_listings()
