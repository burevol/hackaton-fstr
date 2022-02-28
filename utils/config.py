import os

FSTR_DB_HOST = os.getenv('FSTR_DB_HOST', '127.0.0.1')
FSTR_DB_PORT = os.getenv('FSTR_DB_PORT', 5432)
FSTR_DB_LOGIN = os.getenv('FSTR_LOGIN', 'postgres')
FSTR_DB_PASS = os.getenv('FSTR_PASS', 'postgres')
FSTR_DB_NAME = os.getenv('FSTR_DB_NAME', 'pereval')


