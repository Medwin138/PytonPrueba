from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

class MainTest:
    def __init__(self):
        options = Options()
        # Elimina '--headless' para ver el navegador en acción
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()  # Maximizar la ventana del navegador

    def capture_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def main_method(self):
        try:
            self.driver.get("https://www.saucedemo.com/")
            self.capture_screenshot("screenshot_login.png")
            time.sleep(2)  # Pausa de 2 segundos para observar la página

            # Esperar a que aparezcan los elementos de nombre de usuario y contraseña
            username_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "user-name"))
            )
            password_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "password"))
            )
            usernames = "standard_user"  # username_input.get_attribute("value") si se deseara obtener el valor real
            password = "secret_sauce"    # password_input.get_attribute("value") si se deseara obtener el valor real

            # Ingresar los datos en el formulario de login y hacer login
            username_input.send_keys(usernames)
            self.capture_screenshot("screenshot_login_filled.png")
            time.sleep(1)  # Pausa de 1 segundo para observar la entrada de usuario
            password_input.send_keys(password)
            self.capture_screenshot("screenshot_password_filled.png")
            time.sleep(1)  # Pausa de 1 segundo para observar la entrada de contraseña

            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            self.capture_screenshot("screenshot_after_login.png")
            time.sleep(2)  # Pausa de 2 segundos para observar el clic en el botón de login

            # Esperar a que la página de productos cargue completamente
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))

            )

            # Obtener el título de la página de productos
            login_header = self.driver.title
            self.capture_screenshot("screenshot_lanpage.png")

            # Obtener los títulos de los primeros cinco productos
            product_titles = []
            product_elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
            for i in range(min(len(product_elements), 5)):
                product_titles.append(product_elements[i].text)
                time.sleep(1)  # Pausa de 1 segundo para observar cada título de producto

            data = {
                "usernames": usernames,
                "password": password,
                "login_header": login_header,
                "product_titles": product_titles
            }

            return data

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

        finally:
            time.sleep(3)  # Pausa de 3 segundos antes de cerrar el navegador
            self.driver.quit()

# Función para generar el reporte en PDF con capturas de pantalla
def generar_reporte_pdf(data):
    c = canvas.Canvas("reporte_selenium.pdf", pagesize=letter)
    width, height = letter

    # Título del reporte
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Reporte de Pruebas Selenium")

    # Datos obtenidos
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Username: {data['usernames']}")
    c.drawString(50, height - 120, f"Password: {data['password']}")
    c.drawString(50, height - 140, f"Login Header: {data['login_header']}")

    # Títulos de productos
    c.drawString(50, height - 180, "Títulos de Productos:")
    y_position = height - 200
    for title in data['product_titles']:
        c.drawString(70, y_position, title)
        y_position -= 20

    # Insertar capturas de pantalla
    c.drawString(50, height - 300, "Capturas de Pantalla:")
    screenshots = ["screenshot_login.png", "screenshot_login_filled.png", "screenshot_password_filled.png", "screenshot_after_login.png",screenshot_lanpage.png]
    y_position -= 20
    for screenshot in screenshots:
        try:
            img = Image.open(screenshot)
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width
            img_width = 400  # Ancho máximo para la imagen en el documento
            img_height = int(img_width * aspect_ratio)
            c.drawImage(screenshot, 50, y_position - img_height, width=img_width, height=img_height)
            y_position -= (img_height + 20)  # Espacio después de cada imagen
        except Exception as e:
            print(f"Error al insertar imagen {screenshot}: {str(e)}")

    c.save()
    print("Reporte generado: reporte_selenium.pdf")

# Ejemplo de uso
if __name__ == "__main__":
    test = MainTest()
    result = test.main_method()
    if result:
        print("Datos obtenidos:", result)
        generar_reporte_pdf(result)
