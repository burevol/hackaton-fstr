import psycopg2
import json

import utils.config as config


def send_data(raw_data):
    images = "{}"
    conn = psycopg2.connect(dbname=config.FSTR_DB_NAME, user=config.FSTR_DB_LOGIN,
                            password=config.FSTR_DB_PASS, host=config.FSTR_DB_HOST, port=config.FSTR_DB_PORT)
    cur = conn.cursor()
    cur.execute('INSERT INTO "public"."pereval_added" ("raw_data", "images") VALUES (%s, %s) RETURNING id', (json.dumps(raw_data), images))
    last_row_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return last_row_id
