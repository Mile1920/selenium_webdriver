"""Ejercicio 3 - Inicio de Sesión Incorrecto en https://automationexercise.com."""

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

LOGIN_URL = "https://automationexercise.com/login"


def ejecutar() -> Path:
    """Automatiza un login inválido y valida el mensaje de error mostrado."""
    driver = create_driver()

    try:
        driver.get(LOGIN_URL)
        dismiss_consent_if_present(driver)

        # CSS Selector: ingresar correo inexistente
        email_input = wait_for(driver, (By.CSS_SELECTOR, "input[data-qa='login-email']"))
        email_input.clear()
        email_input.send_keys("usuario_inexistente_qa@example.com")

        # Name: ingresar contraseña incorrecta
        password_input = wait_for(driver, (By.NAME, "password"))
        password_input.clear()
        password_input.send_keys("ClaveIncorrecta999")

        # XPath: pulsar botón Login
        wait_clickable(driver, (By.XPATH, "//button[@data-qa='login-button']")).click()

        # XPath: esperar mensaje de error
        error_msg = wait_for(
            driver,
            (By.XPATH, "//p[contains(text(), 'Your email or password is incorrect!')]"),
        )

        # Asserts (validaciones)
        assert error_msg.is_displayed(), "El mensaje de error no está visible."
        assert "Your email or password is incorrect!" in error_msg.text
        assert "/login" in driver.current_url, f"Se esperaba seguir en /login, URL actual: {driver.current_url}"

        return take_screenshot(driver, "ejercicio_3_login_incorrecto.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    captura = ejecutar()
    print(f"[PASS] Ejercicio 3 - Inicio de Sesión Incorrecto | Captura: {captura}")
