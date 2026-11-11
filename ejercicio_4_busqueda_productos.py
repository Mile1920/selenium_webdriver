"""Ejercicio 4 - Búsqueda de Productos en https://automationexercise.com."""

from __future__ import annotations

import sys
from pathlib import Path
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    create_driver,
    dismiss_consent_if_present,
    take_screenshot,
    wait_clickable,
    wait_for,
)

PRODUCTS_URL = "https://automationexercise.com/products"
SEARCH_TERM = "Jeans"


def ejecutar() -> Path:
    """Busca productos por criterio y valida que los resultados coincidan."""
    driver = create_driver()

    try:
        driver.get(PRODUCTS_URL)
        dismiss_consent_if_present(driver)

        # ID: ubicar el campo de búsqueda e ingresar el término
        search_input = wait_for(driver, (By.ID, "search_product"))
        search_input.clear()
        search_input.send_keys(SEARCH_TERM)

        # Name: validar el valor ingresado en el input de búsqueda
        search_by_name = driver.find_element(By.NAME, "search")
        assert search_by_name.get_attribute("value") == SEARCH_TERM

        # ID: presionar el botón de búsqueda
        wait_clickable(driver, (By.ID, "submit_search")).click()

        # XPath: verificar encabezado 'Searched Products'
        heading = wait_for(
            driver,
            (By.XPATH, "//h2[contains(@class, 'title') and contains(., 'Searched Products')]"),
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'start'});", heading)

        # CSS Selector: obtener nombres de productos encontrados
        product_titles = driver.find_elements(By.CSS_SELECTOR, ".features_items .productinfo p")
        nombres = [p.text.strip() for p in product_titles if p.text.strip()]

        # Asserts (validaciones)
        assert "SEARCHED PRODUCTS" in heading.text.upper()
        assert len(nombres) > 0, "No se encontraron productos."
        assert all(SEARCH_TERM.lower() in nombre.lower() for nombre in nombres), (
            f"Productos no coincidentes con '{SEARCH_TERM}': {nombres}"
        )

        return take_screenshot(driver, "ejercicio_4_busqueda_productos.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    captura = ejecutar()
    print(f"[PASS] Ejercicio 4 - Búsqueda de Productos | Captura: {captura}")
