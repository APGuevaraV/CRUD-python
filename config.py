import sys

DATABASE_PATH= "clientes.csv"

"""
verifica que en el nombre del primero argumento ejecutado con terminal se haya mencionado
a pytest haciendo referencia a que se estan ejecutando pruebas
"""
if "pytest" in sys.argv[0]:
    DATABASE_PATH = "tests/clientes_test.csv"