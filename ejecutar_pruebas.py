"""Ejecuta los 3 ejercicios seleccionados de la Práctica 2 en Selenium WebDriver."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ejercicio_2_login_correcto
import ejercicio_3_login_incorrecto
import ejercicio_4_busqueda_productos


def main() -> int:
    ejercicios = [
        ("Ejercicio 2 - Inicio de Sesión Correcto", ejercicio_2_login_correcto.ejecutar),
        ("Ejercicio 3 - Inicio de Sesión Incorrecto", ejercicio_3_login_incorrecto.ejecutar),
        ("Ejercicio 4 - Búsqueda de Productos", ejercicio_4_busqueda_productos.ejecutar),
    ]

    fallos = 0
    for nombre, fn in ejercicios:
        try:
            captura = fn()
            print(f"[PASS] {nombre} -> {captura.name}")
        except Exception as exc:
            fallos += 1
            print(f"[FAIL] {nombre}: {exc}", file=sys.stderr)

    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
