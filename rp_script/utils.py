import os
import time

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

        print("Logged In...")
    
    def goto_ingreso_dda_escrito(self):
        # Get current tab
        first_tab_handle = self.browser.current_window_handle 
        print(f"first table handle: {str(first_tab_handle)}")

        # Ingreso dda/escrito
        goto_search = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//a[@onclick='ingresoDemanYEscritos();']"))
        )
        goto_search.click()  # Opens new tab

        self.browser.implicitly_wait(3)

        # Switch tabs to new open tab
        self.browser.switch_to.window(self.browser.window_handles[1])
        second_tab_handle = self.browser.current_window_handle
        print(f"second table handle: {str(second_tab_handle)}")

        # Ingreso recurso menu btn 
        ingreso_form_display_btn = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@class='list-group-item list-group-item-action p-2 pg_menu_lt'][3]"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView();", ingreso_form_display_btn)
        self.browser.execute_script("arguments[0].click();", ingreso_form_display_btn)

        time.sleep(5)  # TODO - randomize wait

    def fill_form(self):
        print("Start filling form for upload...")
        

        # Opened ingreso form
        # --- Competencia
        competencia_dropdown = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//select[@class='form-control']"))
        )
        competencia_dropdown.click()
        competencia = Select(competencia_dropdown)
        competencia.select_by_visible_text("Cortes de Apelaciones")

        # --- Corte
        corte_dropdown = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen21']/a[1]"))
        )
        corte_dropdown.click()
        # corte = Select(corte_dropdown)
        # corte.select_by_visible_text("C.A. de La Serena")
        corte = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-27']")
        corte.click()

        fijar_competencia_btn = self.browser.find_element(By.XPATH, "//input[@id='id_check_fijar_mod_tribunal']")
        fijar_competencia_btn.click()

        libro_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen40']/a[1]"))
        )
        libro_dropdown.click()
        libro = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-50']")
        libro.click()

        tipo_recurso_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen42']/a[1]"))
        )
        tipo_recurso_dropdown.click()
        tipo_recurso = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-57']")
        tipo_recurso.click()

        fijar_materia_btn = self.browser.find_element(By.XPATH, "//input[@id='id_check_fijar_mod_materia']")
        fijar_materia_btn.click()

        # --- Litigante - Ab Recurrente
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        )
        tipo_sujeto_dropdown.click()
        ab_recurrente = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-65']")
        ab_recurrente.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        rut_input.send_keys(str(os.environ['rut']) + Keys.RETURN)

        # self.browser.implicitly_wait(5)
        time.sleep(5)  # TODO - randomize wait

        fijar_datos_ab_recurrente_btn = self.browser.find_element(By.XPATH, "//input[@id='id_check_fijar_mod_lit']")
        fijar_datos_ab_recurrente_btn.click()

        agregar_litigante_btn = self.browser.find_element(By.XPATH, "//button[@data-bind='click: validarIngresoLitigante']")
        agregar_litigante_btn.click()

        # --- Litigante - Recurrente
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        )
        tipo_sujeto_dropdown.click()
        recurrente = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-71']")
        recurrente.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        rut_input.send_keys("18.354.881-6" + Keys.RETURN)  # TODO fix hardcode

        time.sleep(5)  # TODO - randomize wait

        agregar_litigante_btn = self.browser.find_element(By.XPATH, "//button[@data-bind='click: validarIngresoLitigante']")
        self.browser.execute_script("arguments[0].scrollIntoView();", agregar_litigante_btn)
        self.browser.execute_script("arguments[0].click();", agregar_litigante_btn)

        # --- Litigante - Recurrido
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        )
        tipo_sujeto_dropdown.click()
        recurrida = self.browser.find_element(By.XPATH, "//div[@id='select2-result-label-76']")
        recurrida.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        rut_input.send_keys("76.296.619-0" + Keys.RETURN)  # TODO fix hardcode

        time.sleep(5)  # TODO - randomize wait

        self.browser.execute_script("arguments[0].scrollIntoView();", agregar_litigante_btn)
        self.browser.execute_script("arguments[0].click();", agregar_litigante_btn)

        # Proof of work
        self.browser.save_screenshot("proof_of_work.png")
