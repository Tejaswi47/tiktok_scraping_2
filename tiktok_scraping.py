from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import threading
from dotenv import load_dotenv
import os

load_dotenv()

import time


class SliderMonitor:
    def __init__(self, browser):
        self.browser = browser
        self.slider_detected = False
        self.stop_thread = False

    def monitor_slider(self):
        while not self.stop_thread:
            try:
                # Check for the presence of the slider every 2 seconds
                slider_close_button = WebDriverWait(self.browser, 2).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="verify-bar-close"]'))
                )
                print("Slider detected, attempting to close.")
                slider_close_button.click()
                self.slider_detected = True
            except Exception:
                # No slider found, keep looping
                pass

    def start_monitoring(self):
        # Start the monitoring in a background thread
        slider_thread = threading.Thread(target=self.monitor_slider)
        slider_thread.start()

    def stop_monitoring(self):
        # Stop the monitoring thread
        self.stop_thread = True


class Connection:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage") 
        # chrome_options.binary_location = os.path.join(os.getcwd(),'chrome')
        # chrome_driver_path = os.path.join(os.getcwd(),'chromedriver')
        # os.chmod(chrome_driver_path, 0o755)
        
        vpn_path = os.path.join(os.getcwd(),'JPLGFHPMJNBIGMHKLMMBGECOOBIFKMPA_1_2_2_0.crx')
        chrome_options.add_extension(vpn_path)
        # chrome_service = Service(chrome_driver_path)
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(options = chrome_options, service = service , keep_alive=True)
        self.browser.maximize_window()
        # self.browser.get(f"chrome-extension://JPLGFHPMJNBIGMHKLMMBGECOOBIFKMPA/popup.html")
        self.browser.get("https://account.proton.me/login")
        self.slider_monitor = SliderMonitor(self.browser)
        self.slider_monitor.start_monitoring()
                
    def sign_to_proton(self):
        
        username = os.getenv("EMAIL")
        password = os.getenv("pASSWORD")
        
        username_field = WebDriverWait(self.browser, 15).until(
            EC.visibility_of_element_located((By.ID, 'username')),
        )
        username_field.send_keys(username)
        
        
        password_field = WebDriverWait(self.browser, 15).until(
            EC.visibility_of_element_located((By.ID, 'password')),
        )
        password_field.send_keys(password)

        signin_button = WebDriverWait(self.browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[1]/main/div[1]/div[2]/form/button')),
        )
        
        signin_button.click()
    
    def sign_to_vpn(self):
        self.browser.execute_script('window.open('');')
        self.browser.switch_to.window(self.browser.window_handles[-1])  # Switch to the new tab
        self.browser.get(f"chrome-extension://JPLGFHPMJNBIGMHKLMMBGECOOBIFKMPA/popup.html")
        time.sleep(2)  # Allow time for the tab to open

        sign_in_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'sign-in-button')),
        )
        sign_in_button.click()
        self.browser.switch_to.window(self.browser.window_handles[0])
        
    def switch_vpn(self):
        print(len(self.browser.window_handles))
        self.browser.switch_to.window(self.browser.window_handles[-1])
        time.sleep(10)
        switch_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div/main/div/div[2]/div[1]/div/div[3]/div/div/div/button')),
        )
        switch_button.click()
        self.browser.switch_to.window(self.browser.window_handles[0])
    
    def connect_vpn(self):
        self.browser.execute_script('window.open('');')
        self.browser.switch_to.window(self.browser.window_handles[-1])  # Switch to the new tab
        self.browser.get(f"chrome-extension://JPLGFHPMJNBIGMHKLMMBGECOOBIFKMPA/popup.html")
        
        connect_button = WebDriverWait(self.browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="status"]/div[4]/button')),
        )
        connect_button.click()
        self.browser.switch_to.window(self.browser.window_handles[0])
    
    def search_tiktok_user(self,user):
        self.browser.execute_script('window.open('');')
        self.browser.switch_to.window(self.browser.window_handles[-1])  # Switch to the new tab
        self.browser.get(f"https://www.tiktok.com/search/user?q={user}")
        
        if self.slider_monitor.slider_detected:
            print("Slider closed successfully.")

    def extract_users(self):
        time.sleep(15)
        users_data = self.browser.find_elements(By.CLASS_NAME,'e10wilco10')
        users_list = []
        for i in users_data:
            users_list.append(i.text)
        if self.slider_monitor.slider_detected:
            print("Slider closed successfully.")
        return users_list
    
        
        
