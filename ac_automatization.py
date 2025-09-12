from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

driver = webdriver.Chrome()
driver.get("https://w5.ab.ust.hk/njggt/app/home")

chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
chrome_options.add_experimental_option("prefs", prefs)

print("Please log in manually in the opened browser window...")

wait = WebDriverWait(driver, 300) 
button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']")))

print("Login complete! AC switch detected.")

for i in range(10000):  
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']")))
    button.click()
    print(f"Toggled AC, iteration {i+1}")
    try:
        alert = driver.switch_to.alert
        alert.accept()
        print("Popup accepted")
    except NoAlertPresentException:
        print("No popup appeared")
    time.sleep(600) 
