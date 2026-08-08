from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("http://localhost:5000")

time.sleep(1)

# Start a game
driver.find_element(By.ID, "gridSize").send_keys("4")
driver.find_element(By.XPATH, "//button[contains(text(), 'Start Game')]").click()

time.sleep(1)

# Click Autoplay
autoplay_btn = driver.find_element(By.ID, "autoplayBtn")
autoplay_btn.click()

# Wait for game over
while True:
    status = driver.find_element(By.ID, "statusDisplay").text
    if status in ["DEAD", "ESCAPED"]:
        break
    time.sleep(1)

time.sleep(1)
sprite = driver.find_element(By.ID, "agent-sprite")
print(f"Status: {status}")
print(f"Sprite HTML: {sprite.get_attribute('innerHTML')}")

# Get state from API
cookies = driver.get_cookies()
s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])
resp = s.get("http://localhost:5000/api/state")
data = resp.json()
print(f"API Alive: {data['env']['agent_alive']}")
print(f"API Escaped: {data['env']['agent_escaped']}")

driver.quit()
