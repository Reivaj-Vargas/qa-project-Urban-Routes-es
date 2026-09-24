import time
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import retrieve_phone_code


class UrbanRoutesPage:
    # ---------- Localizadores ----------
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, '//button[text()="Pedir un taxi"]')
    comfort_tariff_button = (By.XPATH, '//div[normalize-space(text())="Comfort"]')
    active_tariff = (By.XPATH, '//*[contains(@class, "active")]//*[normalize-space(text())="Comfort"]')
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, '//button[text()="Siguiente"]')
    code_input = (By.ID, 'code')
    confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    payment_method_value = (By.CSS_SELECTOR, '.pp-value-text')
    add_card_button = (By.XPATH, '//div[text()="Agregar tarjeta"]')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, '//input[@id="code" and @placeholder="12"]')
    link_card_button = (By.XPATH, '//button[normalize-space()="Enlazar" or normalize-space()="Agregar"]')
    close_payment_modal_button = (
        By.XPATH,
        '//div[contains(@class, "payment-picker") and contains(@class, "open")]'
        '//button[contains(@class, "close-button")]')
    comment_input = (By.CSS_SELECTOR, '#comment')  # estrategia CSS
    blanket_switch = (By.XPATH, '//span[@class="slider round"]')
    blanket_checkbox = (By.XPATH, '//div[contains(text(), "Manta")]/..//input[@class="switch-input"]')
    ice_cream_plus_button = (By.XPATH, '//div[contains(text(), "Helado")]/..//div[@class="counter-plus"]')
    ice_cream_counter = (By.XPATH, '//div[contains(text(), "Helado")]/..//div[@class="counter-value"]')
    order_taxi_button = (By.CLASS_NAME, 'smart-button-main')
    search_modal = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver

    def _wait(self, timeout=20):
        return WebDriverWait(self.driver, timeout)

    # ---------- Acciones ----------
    def set_route(self, from_address, to_address):
        self._wait().until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self._wait().until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

    def click_request_taxi(self):
        self._wait().until(EC.element_to_be_clickable(self.request_taxi_button)).click()

    def select_comfort_tariff(self):
        self._wait().until(EC.element_to_be_clickable(self.comfort_tariff_button)).click()

    def fill_phone_number(self, phone):
        self._wait().until(EC.element_to_be_clickable(self.phone_number_button)).click()
        self._wait().until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone)
        self._wait().until(EC.element_to_be_clickable(self.next_button)).click()

    def enter_confirmation_code(self, code):
        self._wait().until(EC.visibility_of_element_located(self.code_input)).send_keys(code)
        self._wait().until(EC.element_to_be_clickable(self.confirm_button)).click()

    def add_credit_card(self, card_number, card_code):
        self._wait().until(EC.element_to_be_clickable(self.payment_method_button)).click()
        self._wait().until(EC.element_to_be_clickable(self.add_card_button)).click()
        self._wait().until(EC.visibility_of_element_located(self.card_number_input)).send_keys(card_number)

        code_field = self._wait().until(EC.visibility_of_element_located(self.card_code_input))
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)  # quita el enfoque para activar el botón

        self._wait().until(EC.element_to_be_clickable(self.link_card_button)).click()
        self._wait().until(EC.element_to_be_clickable(self.close_payment_modal_button)).click()

    def set_comment(self, comment):
        element = self._wait().until(EC.visibility_of_element_located(self.comment_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.send_keys(comment)

    def select_blanket_and_handkerchiefs(self):
        element = self._wait().until(EC.element_to_be_clickable(self.blanket_switch))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()

    def add_ice_creams(self, amount=2):
        plus_btn = self._wait().until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", plus_btn)
        for _ in range(amount):
            plus_btn.click()

    def order_taxi(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.order_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()

    # ---------- Consultas (para los assert) ----------
    def get_from_address(self):
        return self.driver.find_element(*self.from_field).get_attribute('value')

    def get_to_address(self):
        return self.driver.find_element(*self.to_field).get_attribute('value')

    def get_selected_tariff(self):
        return self._wait().until(EC.visibility_of_element_located(self.active_tariff)).text.strip()

    def get_phone_number(self):
        return self._wait().until(EC.visibility_of_element_located(self.phone_number_button)).text.strip()

    def get_payment_method(self):
        return self._wait().until(EC.visibility_of_element_located(self.payment_method_value)).text.strip()

    def get_comment(self):
        return self.driver.find_element(*self.comment_input).get_attribute('value')

    def is_blanket_selected(self):
        return self.driver.find_element(*self.blanket_checkbox).is_selected()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text.strip()

    def is_search_modal_displayed(self):
        return self._wait().until(EC.visibility_of_element_located(self.search_modal)).is_displayed()


class TestUrbanRoutes:
    driver = None

    def setup_method(self):
        # Navegador limpio por prueba, con logs de rendimiento para recuperar el código SMS
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        if self.driver:
            self.driver.quit()

    def _prepare_route(self):
        """Precondición común: direcciones ingresadas y formulario de tarifas abierto."""
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_request_taxi()

    def _confirm_phone(self):
        self.routes_page.fill_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        self.routes_page.enter_confirmation_code(code)

    def test_set_route(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        assert self.routes_page.get_from_address() == data.address_from
        assert self.routes_page.get_to_address() == data.address_to

    def test_select_comfort_tariff(self):
        self._prepare_route()
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.get_selected_tariff() == "Comfort"

    def test_fill_phone_number(self):
        self._prepare_route()
        self._confirm_phone()
        assert self.routes_page.get_phone_number() == data.phone_number

    def test_add_credit_card(self):
        self._prepare_route()
        self.routes_page.add_credit_card(data.card_number, data.card_code)
        assert "tarjeta" in self.routes_page.get_payment_method().lower()

    def test_driver_comment(self):
        self._prepare_route()
        self.routes_page.set_comment(data.message_for_driver)
        assert self.routes_page.get_comment() == data.message_for_driver

    def test_order_blanket(self):
        self._prepare_route()
        self.routes_page.select_comfort_tariff()
        self.routes_page.select_blanket_and_handkerchiefs()
        assert self.routes_page.is_blanket_selected()

    def test_order_ice_cream(self):
        self._prepare_route()
        self.routes_page.select_comfort_tariff()
        self.routes_page.add_ice_creams(2)
        assert self.routes_page.get_ice_cream_count() == '2'

    def test_search_taxi_modal(self):
        self._prepare_route()
        self.routes_page.select_comfort_tariff()
        self._confirm_phone()
        self.routes_page.order_taxi()
        assert self.routes_page.is_search_modal_displayed()