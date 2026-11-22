# models.py — QUÉ ES una transacción (el "esquema").
#
# Cada transacción es un diccionario que tiene SIEMPRE estos 6 campos:
#   id        -> texto único, ej. "T001"
#   date      -> fecha ISO, ej. "2026-09-04"
#   kind      -> "expense" o "income"
#   category  -> de una lista fija (ver validation.ALLOWED_CATEGORIES)
#   amount    -> número decimal mayor que 0, ej. 18.50
#   currency  -> código ISO, ej. "EUR"

from budget_manager import validation

FIELDS = ["id", "date", "kind", "category", "amount", "currency"]


def make_transaction(id, date, kind, category, amount, currency, existing_ids=()):
    # Esta es la ÚNICA forma de crear una transacción.
    # Así todas pasan por la validación y todas tienen los mismos campos.
    return {
        "id": validation.validate_id(id, existing_ids),
        "date": validation.validate_date(date),
        "kind": validation.validate_kind(kind),
        "category": validation.validate_category(category),
        "amount": validation.validate_amount(amount),
        "currency": validation.validate_currency(currency),
    }
