# Proyecto Urban Routes - Pruebas Automatizadas (Sprint 9)

## Descripción del Proyecto
Este proyecto contiene una suite de pruebas automatizadas de extremo a extremo (End-to-End) para la plataforma web **Urban Routes**. La automatización cubre todo el proceso de solicitud de un taxi, desde la configuración de la ruta hasta la selección de tarifas y requisitos adicionales.

## Cobertura de las Pruebas Automatizadas
Las pruebas verifican las siguientes funcionalidades en la aplicación:
1. Configuración de la dirección de origen y destino.
2. Selección de la tarifa *Comfort*.
3. Confirmación del número de teléfono mediante código SMS.
4. Vinculación de una tarjeta de crédito como método de pago.
5. Inclusión de un mensaje/comentario para el conductor.
6. Solicitud de elementos opcionales (manta y pañuelos).
7. Adición de 2 helados al pedido.
8. Despliegue del modal de búsqueda de taxi.

## Tecnologías y Herramientas Utilizadas
- **Lenguaje:** Python 3
- **Framework de Pruebas:** Pytest
- **Automatización Web:** Selenium WebDriver
- **Patrón de Diseño:** Page Object Model (POM)
- **Sincronización:** Esperas explícitas (`WebDriverWait` y `expected_conditions`)
- **Control de Versiones:** Git y GitHub

## Instrucciones de Ejecución

### Pre-requisitos
Tener instalado Python 3 y los paquetes de Selenium y Pytest:
```bash
pip install selenium pytest
