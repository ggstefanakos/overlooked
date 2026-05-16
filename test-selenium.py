from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

service = Service(executable_path="geckodriver.exe")
driver = webdriver.Firefox(service=service)

### Letterboxd Scrape

driver.get("https://letterboxd.com/imdb/tt0816692")

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "fc-button-label"))
# )
# cookies_button = driver.find_elements(By.CLASS_NAME, "fc-button-label")[1]
# cookies_button.click()

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "averagerating tooltip"))
# )

# score_info = driver.find_element(By.CLASS_NAME, "averagerating tooltip")

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "ratings"))
)

score_info = driver.find_element(By.PARTIAL_LINK_TEXT, "ratings")

print(score_info.get_attribute('data-original-title'))
print(score_info.get_property('data-original-title'))

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Interstellar"))
# )

# link = driver.find_element(By.PARTIAL_LINK_TEXT, "Interstellar")
# link.click()


### IMDB Scrape

# driver.get("https://www.imdb.com/title/tt0816692")

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "ipc-rating-star--rating"))
# )
# imdb_score = driver.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text

# WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "vote-count"))
# )

# imdb_count = driver.find_element(By.CLASS_NAME, "vote-count").text


sleep(0.5)

driver.quit()

# if 'K' in imdb_count:
#     imdb_count = float(imdb_count[:-1]) * 1e3
# elif 'M' in imdb_count:
#     imdb_count = float(imdb_count[:-1]) * 1e6
# else:
#     imdb_count = float(imdb_count)