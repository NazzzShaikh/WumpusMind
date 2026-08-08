from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Navigating to http://localhost:5000")
        driver.get("http://localhost:5000")
        
        # Capture console logs
        for entry in driver.get_log('browser'):
            print("BROWSER LOG:", entry)
            
        print("Clicking Got it...")
        # Wait for rules modal to appear and click "Got it"
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Got it')]"))
        )
        btn.click()
        
        time.sleep(1) # wait for animation
        
        print("Clicking Start Game...")
        start_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Game')]"))
        )
        # Select AStar
        driver.execute_script("document.getElementById('algorithm').value = 'AStar';")
        start_btn.click()
        
        time.sleep(1) # wait for navigation
        print(f"Current URL: {driver.current_url}")
        
        for entry in driver.get_log('browser'):
            print("BROWSER LOG:", entry)
            
        print("Clicking Autoplay...")
        autoplay_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "autoplayBtn"))
        )
        autoplay_btn.click()
        
        # Check logs while autoplay is running
        for i in range(10):
            time.sleep(1)
            print(f"--- Second {i+1} ---")
            for entry in driver.get_log('browser'):
                print("BROWSER LOG:", entry)
                
            # Check score/status
            status = driver.find_element(By.ID, "statusDisplay").text
            score = driver.find_element(By.ID, "scoreDisplay").text
            print(f"Status: {status}, Score: {score}")
            if status != "Alive":
                print("Game ended.")
                break
                
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_test()
