# models.py — QUÉ ES una transacción (el "esquema").
#
# Cada transacción tiene SIEMPRE estos campos:
#   id        -> texto único, ej. "T001"
#   date      -> fecha ISO, ej. "2026-09-04"
#   kind      -> "expense" o "income"
#   category  -> de una lista fija (ver ALLOWED_CATEGORIES)
#   amount    -> número decimal mayor que 0, ej. 18.50
#   currency  -> código ISO, ej. "EUR"
#
# TODO:
#   1. Define ALLOWED_KINDS y ALLOWED_CATEGORIES.
#   2. Escribe una función que cree el diccionario de una transacción.
