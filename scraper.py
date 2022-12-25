# # Scrape job data from Hired
# hired_url = 'https://www.hired.com/search?q=software+developer&l=Seattle%2C+WA'
# hired_jobs = scrape_jobs('hired', hired_url)


from selenium import webdriver
from selenium.webdriver.common.by import By

# # Set up the webdriver
# driver = webdriver.Chrome()
#
# # Navigate to the webpage
# driver.get('https://www.dice.com/jobs?q=data%20science&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en&eid=S2Q_,bw_0')

# Set up the webdriver
driver = webdriver.Chrome()

# Navigate to the Dice homepage
driver.get("https://www.dice.com")

# Wait for the page to load
driver.implicitly_wait(15)

# Find the search form and search input field
search_input = driver.find_element(
    By.XPATH, "//*[@placeholder='Job title, skills or company']"
)
# search_input = search_form.find_element(By.NAME, 'q')

# Enter "data scientist" in the search input field
search_input.send_keys("data scientist")

# Submit the search form
search_input.submit()
# Wait for the page to load
driver.implicitly_wait(15)

# Find all a elements with the card-title-link bold class
positions = driver.find_elements(By.CSS_SELECTOR, ".card-title-link.bold")
print([position.text for position in positions])

locations = driver.find_elements(By.CLASS_NAME, "search-result-location")
print([loc.text for loc in locations])

company_names = driver.find_elements(
    By.XPATH, "//*[@data-cy='search-result-company-name']"
)
print([x.text for x in company_names])

posted_dates = driver.find_elements(By.XPATH, "//*[@data-cy='card-posted-date']")
print([x.text for x in posted_dates])

descriptions = driver.find_elements(By.XPATH, "//*[@data-cy='card-summary']")
print([x.text for x in descriptions])

# Close the webdriver
driver.quit()


# if __name__ == '__main__':
#     scrape_dice()
