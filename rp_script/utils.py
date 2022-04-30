from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from webdriver_manager.firefox import GeckoDriverManager

# from selenium_stealth import stealth


class SeleniumBot():
    def __init__(self, url: str = None):
        # --- Setup & initialize browser
        options = Options()
        options.add_argument("start_maximized")
        # options.headless = True
        service = Service(GeckoDriverManager().install())

        self.browser = webdriver.Firefox(service=service, options=options)
        self.browser.set_window_size(1920, 1080)

        # TODO strealth browser

        self.browser.get(url)
    
    def login(self, rut: str = None, passwd: str = None):
        # Intro homepage
        dropdown_btn = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.CLASS_NAME, 'dropbtn')))
        dropdown_btn.click()

        goto_login = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='myDropdown']/a")))
        goto_login.click()

        self.browser.implicitly_wait(3)

        # Login Form
        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.ID, "uname")))
        rut_input.send_keys(rut)

        password_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.ID, "pword")))
        password_input.send_keys(passwd)

        login = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.ID, "login-submit")))
        login.click()
    
    def ingreso_dda_escrito(self):
        # Get current tab
        first_tab_handle = self.browser.current_window_handle 
        print(f"first table handle: {str(first_tab_handle)}")

        # Ingreso dda/escrito new page
        goto_search = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//a[@onclick='ingresoDemanYEscritos();']"))
        )
        goto_search.click()

        self.browser.implicitly_wait(3)

        # Switch tabs to new open tab
        self.browser.switch_to.window(self.browser.window_handles[1])
        second_tab_handle = self.browser.current_window_handle
        print(f"second table handle: {str(second_tab_handle)}")

        # Ingreso recurso menu btn 
        ingreso_form_display_btn = self.browser.find_element(By.XPATH, "//div[@class='list-group-item list-group-item-action p-2 pg_menu_lt'][3]")
        self.browser.execute_script("arguments[0].scrollIntoView();", ingreso_form_display_btn)
        self.browser.execute_script("arguments[0].click();", ingreso_form_display_btn)

        self.browser.implicitly_wait(3)

        # Competencia dropdown
