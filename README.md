# Práctica 2 – Automatización con Selenium WebDriver (Python)

Sitio utilizado: `https://automationexercise.com`

## Ejercicios implementados
1. `ejercicio_2_login_correcto.py` — Inicio de Sesión Correcto
2. `ejercicio_3_login_incorrecto.py` — Inicio de Sesión Incorrecto
3. `ejercicio_4_busqueda_productos.py` — Búsqueda de Productos

## Requisitos incluidos
- 3 ejercicios de la guía sobre `https://automationexercise.com`.
- Localizadores utilizados: `ID`, `Name`, `XPath` y `CSS Selector`.
- 3 `assert` de validación por ejercicio.
- 1 captura de pantalla por ejercicio guardada en `capturas/`.

## Ejecución
```bash
pip install -r requirements.txt
python ejecutar_pruebas.py
```

Para ver el navegador abierto durante la ejecución:
```powershell
$env:HEADLESS="0"; python ejecutar_pruebas.py
```
