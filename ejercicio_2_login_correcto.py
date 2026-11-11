"""Ejercicio 2 - Inicio de Sesión Correcto en https://automationexercise.com."""

from __future__ import annotations

import sys
from pathlib import Path
from selenium.webdriver.common.by import By

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    create_driver,
    dismiss_consent_if_present,
    ensure_test_account,
    take_screenshot,
    wait_clickable,
    wait_for,
)

BASE_URL = "https://automationexercise.com"


def ejecutar() -> Path:
    """Automatiza un login válido y verifica el ingreso correcto al sistema."""
    cuenta = ensure_test_account()
    driver = create_driver()

    try:
        driver.get(BASE_URL)
        dismiss_consent_if_present(driver)

        # CSS Selector: ir a la pantalla de Login
        wait_clickable(driver, (By.CSS_SELECTOR, "a[href='/login']")).click()

        # CSS Selector: ingresar correo válido
        email_input = wait_for(driver, (By.CSS_SELECTOR, "input[data-qa='login-email']"))
        email_input.clear()
        email_input.send_keys(cuenta["email"])

        # Name: ingresar contraseña válida
        password_input = wait_for(driver, (By.NAME, "password"))
        password_input.clear()
        password_input.send_keys(cuenta["password"])

        # XPath: pulsar botón Login
        wait_clickable(driver, (By.XPATH, "//button[@data-qa='login-button']")).click()

        # XPath y CSS Selector: validar sesión iniciada
        logged_user = wait_for(driver, (By.XPATH, "//a[contains(., 'Logged in as')]"))
        logout_link = wait_for(driver, (By.CSS_SELECTOR, "a[href='/logout']"))

        # Asserts (validaciones)
        assert "Logged in as" in logged_user.text, f"Texto inesperado: {logged_user.text}"
        assert cuenta["name"] in logged_user.text, f"Usuario esperado '{cuenta['name']}' no encontrado"
        assert logout_link.is_displayed() and "/login" not in driver.current_url

        return take_screenshot(driver, "ejercicio_2_login_correcto.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    captura = ejecutar()
    print(f"[PASS] Ejercicio 2 - Inicio de Sesión Correcto | Captura: {captura}")
