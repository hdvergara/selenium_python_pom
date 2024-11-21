# Proyecto de automatización de pruebas

### **Descripción del Proyecto**

Este proyecto tiene como objetivo automatizar tareas en navegadores web utilizando Python y Selenium WebDriver. Se ha
implementado el patrón de diseño Page Object Model (POM) para mejorar la mantenibilidad y la organización del código.

**Principales dependencias**

1. **Allure:** Se utiliza para la generación de reportes, se debe tener el binario de Allure y configurada su variable de
   entorno para la visualización de los reportes
2. **Pytest:** Se utiliza para ejecutar los test
3. **Loguru:** Se utiliza para la generación de logs por consola sin tener una configuración específica de logs
4. **Pydantic:** Se utiliza para validar datos y gestionar configuraciones

**Estructura del Proyecto**

* **utils:** Esta carpeta contiene las principales funciones que se requieren para la
  preparación del browser, contiene las principales funciones con las que se ve a interacturar en el navegador. Estas
  clases mencionadas se detallan a continuación:
    * **web_actions -> actions.py:** Contiene las acciones comunes que se realizan en Selenium, como encontrar
      elementos, hacer clics, enviar
      texto, etc.
    * **browser_settings -> browser_settings.py:** Permite seleccionar el navegador a utilizar (Chrome, Firefox, Edge) a
      través de
      webdriver-manager.
* **pages:** Paquete que contiene el mapeo de todos los elementos de cada vista de la aplicación con los cuales vamos a
  interactuar
* **test:** Paquete que contiene las pruebas unitarias individuales.

**Requisitos Previos**

* **Python:** Asegúrate de tener instalado Python 3.10 o superior.
* **Pipenv:** Asegúrate de tener instalado la dependencia *Pipenv*. Es utilizado para gestionar las dependencias del
  proyecto.
    ```python
   pip install pipenv

**Nota:** Se recomienda trabajar con el IDE PyCharm dado que es un IDE nativo para trabajar con Python, aunque si se
quiere trabajar con Visual Studio Code no hay ningún problema siempre y cuando se tengo configurado para Python.

**Instalación**

1. **Clonar el repositorio**
2. **Crear y activar el entorno virtual:**
   ```python
   pipenv install

**Ejecución de pruebas**

Las pruebas se pueden ejecutar de las siguientes formas:

1. Abriendo la clase Test que queremos ejecutar y si se esta usando PyCharm hacemos clic en la opción Run que nos
   muestra en la clase o en cada test dentro de la clase. Esta opción ejecuta los test pero no genera ningun reporte,
   solamente veremos un log por consola de lo que se esta ejecutando.
2. Abriendo la terminal dentro del proyecto, ejecutamos el siguiente comando:
   ```python
   pytest -s    

El anterior comando ejecuta todos los test que se encuentran en la carpeta **test** en la raíz del proyecto. Esta
ejecución tampoco genera ningún tipo de reporte.

3. Abriendo la terminal dentro del proyecto, ejecutamos el siguiente comando:
    ```python
   pytest --alluredir=reports/allure-results

Esta opción ejecuta todos los test que se encuentran en la carpeta **test** en la raíz del proyecto, esta ejecución crea
una carpeta en la raíz del proyecto llamada reports, dentro contendrá información necesaria para la generación y
visualización del reporte.

Para visualizar el reporte debemos ejecutar el siguiente comando:

    allure serve reports/allure-results

Este comando nos abre un reporte en formato HTML el cual contiene la información de la ejecución de las pruebas.