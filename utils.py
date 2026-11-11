"""Utilidades compartidas de Selenium WebDriver para los ejercicios."""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

CARPETA_CAPTURAS = Path(__file__).resolve().parent / "capturas"

TEST_USER_NAME = "Maide QA"
TEST_USER_EMAIL = "maide.unifranz.qa2026@example.com"
TEST_USER_PASSWORD = "QaPassword2026!"


def create_driver() -> WebDriver:
    """Crea una instancia configurada de Chrome WebDriver."""
    headless = os.environ.get("HEADLESS", "1") != "0"
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    return driver


def wait_for(driver: WebDriver, locator: tuple[str, str], timeout: int = 15):
    """Espera hasta que el elemento sea visible."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_clickable(driver: WebDriver, locator: tuple[str, str], timeout: int = 15):
    """Espera hasta que el elemento sea clickeable."""
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def dismiss_consent_if_present(driver: WebDriver) -> None:
    """Cierra el banner de cookies si aparece."""
    try:
        btn = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-cta-consent, button.fc-primary-button"))
        )
        btn.click()
    except TimeoutException:
        pass


def take_screenshot(driver: WebDriver, filename: str) -> Path:
    """Guarda la captura de pantalla de evidencia dentro de la carpeta capturas/."""
    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    path = CARPETA_CAPTURAS / filename
    driver.save_screenshot(str(path))
    return path


def ensure_test_account() -> dict[str, str]:
    """Garantiza que exista la cuenta de prueba en automationexercise.com."""
    payload = urllib.parse.urlencode(
        {
            "name": TEST_USER_NAME,
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "title": "Mrs",
            "birth_date": "10",
            "birth_month": "5",
            "birth_year": "2000",
            "firstname": "Maide",
            "lastname": "Aviza",
            "company": "UNIFRANZ",
            "address1": "Av. Arce 123",
            "address2": "Zona Central",
            "country": "United States",
            "zipcode": "10001",
            "state": "NY",
            "city": "New York",
            "mobile_number": "70000000",
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://automationexercise.com/api/createAccount",
        data=payload,
        method="POST",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = json.loads(resp.read().decode("utf-8", errors="replace"))
        if body.get("responseCode") not in (201, 400):
            raise RuntimeError(f"No se pudo preparar la cuenta de prueba: {body}")

    return {"name": TEST_USER_NAME, "email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
