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

from pprint import pprint
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

        pprint("Logged In...")

    def goto_ingreso_dda_escrito(self):
        # Get current tab
        first_tab_handle = self.browser.current_window_handle
        # pprint(f"first table handle: {str(first_tab_handle)}")

        # Ingreso dda/escrito
        goto_search = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//a[@onclick='ingresoDemanYEscritos();']"))
        )
        goto_search.click()  # Opens new tab

        self.browser.implicitly_wait(3)

        # Switch tabs to new open tab
        self.browser.switch_to.window(self.browser.window_handles[1])
        second_tab_handle = self.browser.current_window_handle
        # print(f"second table handle: {str(second_tab_handle)}")

        # Ingreso recurso menu btn
        ingreso_form_display_btn = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@class='list-group-item list-group-item-action p-2 pg_menu_lt'][3]"))
        )
        self.browser.execute_script(
            "arguments[0].scrollIntoView();", ingreso_form_display_btn)
        self.browser.execute_script(
            "arguments[0].click();", ingreso_form_display_btn)

        time.sleep(5)  # TODO - randomize wait

    def fill_forms(self):
        pprint("Filling form...")

        # Opened ingreso form
        # --- Competencia
        competencia_dropdown = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//select[@class='form-control']"))
        )
        competencia_dropdown.click()
        competencia = Select(competencia_dropdown)
        competencia.select_by_visible_text("Cortes de Apelaciones")

        # --- Corte
        corte_dropdown = WebDriverWait(self.browser, timeout=25).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen21']/a[1]"))
        ).click()
        # corte_dropdown.click()
        # corte = Select(corte_dropdown)
        # corte.select_by_visible_text("C.A. de La Serena")
        corte = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-27']"
        ).click()
        # corte.click()

        fijar_competencia_btn = self.browser.find_element(
            By.XPATH, "//input[@id='id_check_fijar_mod_tribunal']"
        ).click()
        # fijar_competencia_btn.click()

        libro_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen40']/a[1]"))
        ).click()
        # libro_dropdown.click()
        libro = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-50']"
        )
        libro.click()

        tipo_recurso_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen42']/a[1]"))
        ).click()
        # tipo_recurso_dropdown.click()
        tipo_recurso = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-57']"
        ).click()
        # tipo_recurso.click()

        fijar_materia_btn = self.browser.find_element(
            By.XPATH, "//input[@id='id_check_fijar_mod_materia']"
        ).click()
        # fijar_materia_btn.click()

        # --- Litigante - Ab Recurrente
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        ).click()
        # tipo_sujeto_dropdown.click()
        ab_recurrente = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-65']"
        ).click()
        # ab_recurrente.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        # --- Rut abogad@ recurente
        rut_input.send_keys(str(os.environ['rut']) + Keys.RETURN)

        # self.browser.implicitly_wait(5)
        time.sleep(5)  # TODO - randomize wait

        # fijar_datos_ab_recurrente_btn = self.browser.find_element(
        #     By.XPATH, "//input[@id='id_check_fijar_mod_lit']"
        # ).click()
        # fijar_datos_ab_recurrente_btn.click()

        agregar_litigante_btn = self.browser.find_element(
            By.XPATH, "//button[@data-bind='click: validarIngresoLitigante']"
        ).click()
        # agregar_litigante_btn.click()

        # --- Litigante - Recurrente
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        ).click()
        # tipo_sujeto_dropdown.click()
        recurrente = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-71']"
        ).click()
        # recurrente.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        # --- Rut recurrente
        rut_input.send_keys("18.354.881-6" + Keys.RETURN)  # TODO fix hardcode

        time.sleep(5)  # TODO - randomize wait

        agregar_litigante_btn = self.browser.find_element(
            By.XPATH, "//button[@data-bind='click: validarIngresoLitigante']")
        self.browser.execute_script(
            "arguments[0].scrollIntoView();", agregar_litigante_btn)
        self.browser.execute_script(
            "arguments[0].click();", agregar_litigante_btn)

        # --- Litigante - Recurrido
        tipo_sujeto_dropdown = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//div[@id='s2id_autogen59']/a[1]"))
        ).click()
        # tipo_sujeto_dropdown.click()

        recurrida = self.browser.find_element(
            By.XPATH, "//div[@id='select2-result-label-76']"
        ).click()
        # recurrida.click()

        rut_input = WebDriverWait(self.browser, timeout=10).until(
            EC.element_to_be_clickable(self.browser.find_element(
                By.XPATH, "//input[@data-bind='value: rutSel, disable:bloqueoRutComp']"))
        )
        # --- Rut recurrido (Isapre)
        rut_input.send_keys("76.296.619-0" + Keys.RETURN)  # TODO fix hardcode

        time.sleep(5)  # TODO - randomize wait

        self.browser.execute_script(
            "arguments[0].scrollIntoView();", agregar_litigante_btn)
        self.browser.execute_script(
            "arguments[0].click();", agregar_litigante_btn)

        informacion_adicional_btn = self.browser.find_element(
            By.XPATH, "//button[@data-bind='click: showModalInformacionAdicional , enable: bloqueoInfoAdicional()']"
        ).click()
        # informacion_adicional_btn.click()

        precio_base_checkbox = self.browser.find_element(
            By.XPATH, "//input[@data-bind='checked: checkPrecioBase']"
        ).click()
        # precio_base_checkbox.click()

        time.sleep(5)  # TODO - randomize wait

        # --- Precio Base
        pb_input = self.browser.find_element(By.ID, "desdePrecioBase")
        pb_input.send_keys("2.87")  # TODO fix hardcode

        # --- Precio Base Reajustado
        pbr_input = self.browser.find_element(By.ID, "hastaPrecioBase")
        pbr_input.send_keys("3.9" + Keys.RETURN)

        agregar_info_adicional_btn = self.browser.find_element(
            By.XPATH, "//button[@data-bind='click: agregarInformacionAdicional, enable: validDesdeHasta']")
        agregar_info_adicional_btn.click()

        time.sleep(3)  # TODO - randomize wait

        ingresar_causa_btn = self.browser.find_element(
            By.XPATH, "//button[@data-bind='click: ingresarCausa, enable: validCausaLitiganteComp() ']"
        ).click()
        # ingresar_causa_btn.click()

        time.sleep(3)  # TODO - randomize wait

        # TODO - Upload adjuntos
        # upload_recurso = self.browser.find_element(
        #     By.XPATH, "//button[@data-bind='click: uploadDocumentoPrincipal, disable: flgShowMsnBrowserNoValid']"
        # )
        # upload_recurso.send_keys("pdf_autoescrito/C.A. DE LA SERENA - MANUEL ABARCA MEZA con BANMÉDICA.pdf" + Keys.RETURN)

        # Proof of work
        self.browser.save_screenshot("proof_of_work.png")
