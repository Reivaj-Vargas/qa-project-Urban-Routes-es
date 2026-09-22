from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # --- LOCALIZADORES ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_tariff_button = (By.XPATH, '//div[contains(text(), "Comfort")]')
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_phone_button = (By.XPATH, '//button[text()="Siguiente"]')
    confirm_code_input = (By.ID, 'code')
    confirm_phone_button = (By.XPATH, '//button[text()="Confirmar"]')

    # Tarjeta de crédito
    payment_method_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.CLASS_NAME, 'pp-plus')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, '//input[@id="code" and @class="card-input"]')
    link_card_button = (By.XPATH, '//button[text()="Enlazar"]')
    close_payment_modal_button = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button round"]')

    # Requisitos adicionales
    driver_comment_input = (By.ID, 'comment')
    blanket_switch = (By.XPATH, '//span[@class="slider round"]')  # Ajusta según el selector de tu maqueta
    ice_cream_plus_button = (By.XPATH, '//div[text()="Helado"]/..//div[@class="counter-plus"]')
    ice_cream_counter = (By.XPATH, '//div[text()="Helado"]/..//div[@class="counter-value"]')
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    search_modal = (By.CLASS_NAME, 'order-body')
    driver_info_modal = (By.CLASS_NAME, 'order-header-title')  # Para el opcional

    def __init__(self, driver):
        self.driver = driver

    # --- MÉTODOS DE ACCIÓN ---
    def set_route(self, from_address, to_address):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.comfort_tariff_button)).click()

    def fill_phone_number(self, phone):
        self.driver.find_element(*self.phone_number_button).click()
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.phone_input)).send_keys(phone)
        self.driver.find_element(*self.next_phone_button).click()

    def enter_confirm_code(self, code):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.confirm_code_input)).send_keys(code)
        self.driver.find_element(*self.confirm_phone_button).click()

    def add_credit_card(self, card_number, card_code):
        self.driver.find_element(*self.payment_method_button).click()
        self.driver.find_element(*self.add_card_button).click()

        # Llenar número y CVV
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.card_number_input)).send_keys(
            card_number)
        code_field = self.driver.find_element(*self.card_code_input)
        code_field.send_keys(card_code)

        # TRUCO DEL TAB: Perder el enfoque para activar el botón 'Enlazar'
        code_field.send_keys(Keys.TAB)

        self.driver.find_element(*self.link_card_button).click()
        self.driver.find_element(*self.close_payment_modal_button).click()

    def set_driver_comment(self, comment):
        self.driver.find_element(*self.driver_comment_input).send_keys(comment)

    def order_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_switch).click()

    def add_two_ice_creams(self):
        plus_btn = self.driver.find_element(*self.ice_cream_plus_button)
        plus_btn.click()
        plus_btn.click()

    def click_order_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()

        import data
        from helpers import retrieve_phone_code  # Función provista por la plataforma
        from selenium import webdriver

        class TestUrbanRoutes:
            driver = None

            @classmethod
            def setup_class(cls):
                cls.driver = webdriver.Chrome()

            # 1. Configurar dirección
            def test_set_route(self):
                self.driver.get(data.urban_routes_url)
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.set_route(data.address_from, data.address_to)
                assert self.driver.find_element(*routes_page.from_field).get_attribute('value') == data.address_from
                assert self.driver.find_element(*routes_page.to_field).get_attribute('value') == data.address_to

            # 2. Seleccionar tarifa Comfort
            def test_select_comfort_tariff(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.select_comfort_tariff()
                # Agrega assert que valide la selección

            # 3. Rellenar número de teléfono
            def test_fill_phone_number(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.fill_phone_number(data.phone_number)
                code = retrieve_phone_code(self.driver)
                routes_page.enter_confirm_code(code)
                # Agrega assert para verificar que el número se guardó

            # 4. Agregar tarjeta de crédito
            def test_add_credit_card(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.add_credit_card(data.card_number, data.card_code)
                # Agrega assert para verificar la tarjeta añadida

            # 5. Escribir mensaje al conductor
            def test_driver_comment(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.set_driver_comment(data.message_for_driver)
                assert self.driver.find_element(*routes_page.driver_comment_input).get_attribute(
                    'value') == data.message_for_driver

            # 6. Pedir manta y pañuelos
            def test_order_blanket(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.order_blanket_and_tissues()

            # 7. Pedir 2 helados
            def test_order_ice_cream(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.add_two_ice_creams()
                assert self.driver.find_element(*routes_page.ice_cream_counter).text == "2"

            # 8. Aparece el modal para buscar taxi
            def test_search_taxi_modal(self):
                routes_page = UrbanRoutesPage(self.driver)
                routes_page.click_order_taxi()
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(routes_page.search_modal))

            @classmethod
            def teardown_class(cls):
                cls.driver.quit()