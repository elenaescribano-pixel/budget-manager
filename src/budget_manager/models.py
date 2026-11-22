# models.py — QUÉ ES una transacción, como una clase.
#
# Cada transacción tiene SIEMPRE estos 6 atributos:
#   id        -> texto único, ej. "T001"
#   date      -> fecha ISO, ej. "2026-09-04"
#   kind      -> "expense" o "income"
#   category  -> de una lista fija (ver validation.ALLOWED_CATEGORIES)
#   amount    -> número decimal mayor que 0, ej. 18.50
#   currency  -> código ISO, ej. "EUR"

from budget_manager import validation

# Orden de las columnas en el archivo CSV.
FIELDS = ["id", "date", "kind", "category", "amount", "currency"]


class Transaction:
    def __init__(self, transaction_id, date, kind, category, amount, currency, existing_ids=()):
        # La validación se hace AL CREAR el objeto: si algún dato está mal,
        # se lanza ValueError y el objeto no llega a existir.
        # existing_ids = ids que ya están en uso (por defecto, ninguno).
        self.id = validation.validate_id(transaction_id, existing_ids)
        self.date = validation.validate_date(date)
        self.kind = validation.validate_kind(kind)
        self.category = validation.validate_category(category)
        self.amount = validation.validate_amount(amount)
        self.currency = validation.validate_currency(currency)

    def to_dict(self):
        # Diccionario con las mismas claves que las columnas del CSV.
        return {
            "id": self.id,
            "date": self.date,
            "kind": self.kind,
            "category": self.category,
            "amount": self.amount,
            "currency": self.currency,
        }

    def __str__(self):
        # Texto que se muestra al hacer print(transaccion).
        return f"{self.id}  {self.date}  {self.kind:<8} {self.category:<10} {self.amount:>9.2f} {self.currency}"
