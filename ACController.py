import atexit
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoAlertPresentException
import threading
import time

class ACController:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.ac_on = False
        self.auto_toggle_active = False
        self.auto_toggle_thread = None
        self.auto_toggle_interval = 600  # 10 minutes default
        self.logger = logging.getLogger('ACController')
        self.setup_selenium()
        atexit.register(self.on_exit)
    
    def setup_selenium(self):
        """Initialize Chrome driver and navigate to AC control page"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.logger.info("Initializing Chrome driver...")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://w5.ab.ust.hk/njggt/app/home")
        self.wait = WebDriverWait(self.driver, 300)
        
        self.logger.info("Please log in manually in the opened browser window...")
        print("Please log in manually in the opened browser window...")  # Keep this as print for user interaction
        
        # Wait for login and AC switch to be available
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']")))
        self.logger.info("Login complete! AC switch detected.")
        print("Login complete! AC switch detected.")  # Keep this as print for user confirmation
    
    def toggle_ac(self):
        """Toggle the AC switch once"""
        try:
            if not(self.wait):
                self.logger.error("WebDriverWait not initialized")
                return False
            button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='switch']")))
            button.click()
            self.ac_on = not self.ac_on
            self.logger.info(f"AC toggled. AC is now: {'ON' if self.ac_on else 'OFF'}")
            
            # Handle any popup
            try:
                if not(self.driver):
                    self.logger.error("WebDriver not initialized")
                    return False
                alert = self.driver.switch_to.alert
                alert.accept()
                self.logger.info("Popup accepted")
            except NoAlertPresentException:
                self.logger.debug("No popup appeared")
                
            return True
        except Exception as e:
            self.logger.error(f"Error toggling AC: {e}")
            return False
    
    def start_auto_toggle(self, interval=600):
        """Start automatic AC toggling every specified interval (seconds)"""
        if self.auto_toggle_active:
            self.logger.warning("Auto-toggle is already active")
            return False
            
        self.auto_toggle_interval = interval
        self.auto_toggle_active = True
        self.auto_toggle_thread = threading.Thread(target=self._auto_toggle_worker)
        self.auto_toggle_thread.daemon = True
        self.auto_toggle_thread.start()
        self.logger.info(f"Auto-toggle started with {interval} second interval")
        return True
    
    def stop_auto_toggle(self):
        """Stop automatic AC toggling"""
        if not self.auto_toggle_active:
            self.logger.warning("Auto-toggle is not active")
            return False
            
        self.auto_toggle_active = False
        if self.auto_toggle_thread:
            self.auto_toggle_thread.join(timeout=1)
        self.logger.info("Auto-toggle stopped")
        return True
    
    def _auto_toggle_worker(self):
        """Worker thread for auto-toggling"""
        iteration = 0
        self.logger.info("Auto-toggle worker thread started")
        while self.auto_toggle_active:
            if iteration > 0:  # Don't toggle immediately on start
                self.toggle_ac()
                self.logger.info(f"Auto-toggle iteration {iteration}")
            
            # Sleep in small chunks to allow for quick stopping
            sleep_time = 0
            while sleep_time < self.auto_toggle_interval and self.auto_toggle_active:
                time.sleep(1)
                sleep_time += 1
            
            iteration += 1
        self.logger.info("Auto-toggle worker thread ended")
    
    def get_status(self):
        """Get current AC status"""
        return {
            "ac_on": self.ac_on,
            "auto_toggle_active": self.auto_toggle_active,
            "auto_toggle_interval": self.auto_toggle_interval
        }
    
    def on_exit(self):
        """Cleanup on exit"""
        self.logger.info("Script is exiting!")
        self.stop_auto_toggle()
        if self.ac_on:
            self.logger.info("Turning off AC before exit...")
            self.toggle_ac()
        if self.driver:
            self.driver.quit()
            self.logger.info("WebDriver closed")
