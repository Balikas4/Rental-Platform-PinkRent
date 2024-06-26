import os
import logging
from time import time, sleep
import psycopg2

# Import credentials from local_settings.py
from PinkRent.local_settings import DATABASES

# tikrinimo dažnumas, pagal nutylėjimą laukiame 30 sekundžių, ir nepavykus po sekundės laukiame iš naujo.
check_timeout = os.getenv("POSTGRES_CHECK_TIMEOUT", 30)
check_interval = os.getenv("POSTGRES_CHECK_INTERVAL", 1)

# duomenų bazės konfigūracija - pagal nutylėjimą turėtų sutapti su Django nustatymais.
config = {
    "dbname": DATABASES["default"]["NAME"],
    "user": DATABASES["default"]["USER"],
    "password": DATABASES["default"]["PASSWORD"],
    "host": DATABASES["default"]["HOST"],
    "port": DATABASES["default"]["PORT"]
}

# sukonfigūruojame logerį
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.info(
    f"DB config {config['dbname']} {config['user']} {config['host']} ...")

# įsimename dabartinį laiką
start_time = time()

# prisijungimo į duomenų bazę tikrinimo funkcija
def pg_isready(host, user, password, dbname, port):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready! ✨ 💅")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(
                f"Postgres isn't ready. Waiting for {check_interval} sec...")
            sleep(check_interval)

    logger.error(
        f"We could not connect to Postgres within {check_timeout} seconds.")
    return False

pg_isready(**config)
