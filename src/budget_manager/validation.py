# validation.py — comprobar que los datos son correctos ANTES de aceptarlos.
#
# Regla: si algo está mal, lanza un error con un mensaje CLARO.
#   Bien: "amount must be > 0 (got -5.0)"
#   Mal:  "invalid input"
#
# Cada función recibe el valor tal cual llega (normalmente texto),
# lo comprueba y devuelve el valor limpio. Nunca corrige en silencio.

from datetime import date

ALLOWED_KINDS = ["expense", "income"]
ALLOWED_CATEGORIES = ["food", "transport", "housing", "leisure", "health", "salary", "other"]
ALLOWED_CURRENCIES = ["EUR"]  # Release 1: solo una moneda, para que el saldo tenga sentido


def validate_id(value, existing_ids):
    text = str(value).strip()
    if text == "":
        raise ValueError("id must not be empty")
    if text in existing_ids:
        raise ValueError(f"id must be unique ('{text}' is repeated)")
    return text


def validate_date(value):
    text = str(value).strip()
    try:
        date.fromisoformat(text)
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD (got '{text}')")
    return text


def validate_kind(value):
    text = str(value).strip().lower()
    if text not in ALLOWED_KINDS:
        raise ValueError(f"kind must be one of {ALLOWED_KINDS} (got '{text}')")
    return text


def validate_category(value):
    # Política: una categoría desconocida se RECHAZA (no se acepta en silencio).
    # Si no encaja en ninguna, el usuario puede usar "other".
    text = str(value).strip().lower()
    if text not in ALLOWED_CATEGORIES:
        raise ValueError(f"category must be one of {ALLOWED_CATEGORIES} (got '{text}')")
    return text


def validate_amount(value):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"amount must be a number (got '{value}')")
    if amount <= 0:
        raise ValueError(f"amount must be > 0 (got {amount})")
    return amount


def validate_currency(value):
    text = str(value).strip().upper()
    if text not in ALLOWED_CURRENCIES:
        raise ValueError(f"currency must be one of {ALLOWED_CURRENCIES} (got '{text}')")
    return text
