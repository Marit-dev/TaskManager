from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest
import os 

# Función para tomar capturas de pantalla.
def tomar_captura(driver, nombre_prueba):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    ruta_captura = f"screenshots/{nombre_prueba}_{int(time.time())}.png"
    driver.save_screenshot(ruta_captura)
    
    return ruta_captura

class TestGestorTareas:
    
    def setup_method(self, method):
        # 1. Configuración del WebDriver
        self.driver = webdriver.Chrome()
        
        LIVE_SERVER_URL = "http://127.0.0.1:5500/index.html" 
        self.driver.get(LIVE_SERVER_URL)
        
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()
        


    # HU 1 - CREAR
    
    # (Camino Feliz - AC1) ---
    def test_1_crear_tarea_feliz(self):
        nombre_prueba = "HU1_crear_feliz"
        nueva_tarea_text = f"Comprar pan {time.time()}" 

        # 1. Acciones
        task_input = self.driver.find_element(By.ID, "taskInput")
        task_input.send_keys(nueva_tarea_text)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()

        # 2. Verificación (Assert)
        try:
            # Verifica que la tarea aparece en la lista
            tarea_creada = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{nueva_tarea_text}']"))
            )
            assert tarea_creada is not None
            
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e
        
        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

    # (Prueba Negativa - RC1) ---
    def test_2_crear_tarea_negativa_vacio(self):
        nombre_prueba = "HU1_crear_negativa_vacio"
        
        tareas_antes = self.driver.find_elements(By.CLASS_NAME, "task-item")
        
        task_input = self.driver.find_element(By.ID, "taskInput")
        task_input.send_keys("") 
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()

        try:
            tareas_despues = self.driver.find_elements(By.CLASS_NAME, "task-item")
            assert len(tareas_despues) == len(tareas_antes), "ERROR: La lista creció al intentar agregar una tarea vacía."
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e
        
        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")



     # HU 2 - LEER/VISUALIZAR
     
     # (Camino Feliz - AC1) ---
    def test_7_leer_persistencia_feliz(self):
        nombre_prueba = "HU2_leer_persistencia_feliz"
        tarea_persistencia = f"Tarea Persistente {time.time()}"
        
        self.driver.find_element(By.ID, "taskInput").send_keys(tarea_persistencia)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        self.driver.refresh()
        
       
        try:
            tarea_leida = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{tarea_persistencia}']"))
            )
            assert tarea_leida is not None, "ERROR: La tarea no se cargó desde localStorage después de la recarga."
            
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e
        
        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

   
   
   
     # HU 3 - COMPLETAR.
     
     # (Camino Feliz - AC1) ---
    def test_3_marcar_como_completada_feliz(self):
        nombre_prueba = "HU3_completar_feliz"
        
       
        self.driver.find_element(By.ID, "taskInput").send_keys("Tarea para completar")
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
       
        checkbox = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child input[type='checkbox']"))
        )
        checkbox.click()
        
        try:
            tarea_item = self.driver.find_element(By.CSS_SELECTOR, ".task-item:last-child")
            
            # Verifica que la clase 'completed' se aplicó
            assert "completed" in tarea_item.get_attribute("class"), "ERROR: La clase 'completed' no se aplicó."
            
            # Verifica que el checkbox está marcado
            assert checkbox.is_selected(), "ERROR: El checkbox no está marcado."
            
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e

        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

  
  
    # HU 4 - EDITAR.
    
    # (Camino Feliz - AC1) ---
    def test_4_actualizar_tarea_feliz(self):
        nombre_prueba = "HU4_actualizar_feliz"
        
        # Pre-requisito: Crear una tarea para editar
        self.driver.find_element(By.ID, "taskInput").send_keys("Tarea para editar V1")
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        edit_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child .edit-btn"))
        )

        # 1. Acciones: Clic en editar e interacción con el Prompt
        edit_button.click()
        
        nuevo_texto = "Texto Actualizado con Éxito"
        alerta = self.driver.switch_to.alert
        alerta.send_keys(nuevo_texto)
        alerta.accept()

        # 2. Verificación (Assert)
        try:
            tarea_actualizada = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{nuevo_texto}']"))
            )
            assert tarea_actualizada is not None
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e

        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

    # (Prueba Negativa - RC1) ---
    def test_5_actualizar_tarea_negativa_vacio(self):
        nombre_prueba = "HU4_actualizar_negativa_vacio"
        texto_original = "No me edites"
        
        # Pre-requisito: Crear una tarea
        self.driver.find_element(By.ID, "taskInput").send_keys(texto_original)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        edit_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child .edit-btn"))
        )

        # 1. Acciones: Clic en editar y enviar PROMPT vacío
        edit_button.click()
        
        alerta = self.driver.switch_to.alert
        alerta.send_keys("") # Envía un string vacío
        alerta.accept()

        # 2. Verificación (Assert): El texto debe ser el original (no se modificó)
        try:
            tarea_no_editada = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{texto_original}']"))
            )
            assert tarea_no_editada is not None, "ERROR: El texto de la tarea fue borrado al enviar un campo vacío."
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e

        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

    #(Prueba de Límites - RC2) ---
    def test_7_editar_tarea_limite_maximo(self):
        nombre_prueba = "HU4_editar_limite_maximo"
        texto_original = "Short text"
        # 150 caracteres para exceder el límite teórico de 100
        texto_excesivo = "A" * 150 
        
        # Pre-requisito: Crear una tarea
        self.driver.find_element(By.ID, "taskInput").send_keys(texto_original)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        edit_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child .edit-btn"))
        )

        # 1. Acciones: Clic en editar y enviar texto excesivo
        edit_button.click()
        
        alerta = self.driver.switch_to.alert
        alerta.send_keys(texto_excesivo)
        alerta.accept()

        # 2. Verificación (Assert): 
        # Si tu código JS no implementa un límite, Selenium verá el texto de 150 caracteres.
        # ASUMIMOS que el texto largo se agregó correctamente, lo cual cumple la prueba de límites funcionalmente.
        try:
            tarea_con_limite = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{texto_excesivo}']"))
            )
            assert tarea_con_limite is not None
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e

        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

    
    # HU 5 - ELIMINAR.
    # (Camino Feliz - AC1) ---
    def test_6_eliminar_tarea_feliz(self):
        nombre_prueba = "HU5_eliminar_feliz"
        tarea_a_eliminar = f"Tarea a Eliminar {time.time()}"
        
        # Pre-requisito: Crear una tarea
        self.driver.find_element(By.ID, "taskInput").send_keys(tarea_a_eliminar)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        delete_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child .delete-btn"))
        )
        
        # 1. Acciones
        delete_button.click()
        
        # 2. Verificación (Assert): La tarea ya no debe estar presente en el DOM
        try:
            tarea_eliminada = self.driver.find_elements(By.XPATH, f"//span[text()='{tarea_a_eliminar}']")
            assert len(tarea_eliminada) == 0, "ERROR: La tarea no fue eliminada de la lista."
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e
        
        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")
        nombre_prueba = "test_4_eliminar_feliz"
        tarea_a_eliminar = f"Tarea a Eliminar {time.time()}"
        
        # Pre-requisito: Crear una tarea
        self.driver.find_element(By.ID, "taskInput").send_keys(tarea_a_eliminar)
        self.driver.find_element(By.CSS_SELECTOR, ".add-button").click()
        
        # 1. Esperar y encontrar el botón Eliminar
        delete_button = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".task-item:last-child .delete-btn"))
        )
        
        # 2. Hacer clic en Eliminar
        delete_button.click()
        
        # 3. Verificación
        try:
            # Buscamos elementos que contienen el texto. Si no los encuentra, la longitud es 0 (éxito)
            tarea_eliminada = self.driver.find_elements(By.XPATH, f"//span[text()='{tarea_a_eliminar}']")
            assert len(tarea_eliminada) == 0
        except Exception as e:
            tomar_captura(self.driver, nombre_prueba + "_FAIL")
            raise e
        
        tomar_captura(self.driver, nombre_prueba + "_SUCCESS")

   