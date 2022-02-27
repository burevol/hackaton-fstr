import json
from datetime import datetime

import psycopg2
import requests

import utils.config as config


def send_data(data, images_dict):
    images = json.dumps(images_dict)
    raw_data = json.dumps(data)
    dt = datetime.now()
    query = 'INSERT INTO "public"."pereval_added" ("raw_data", "date_added", "status", "images") VALUES (%s, %s, ' \
            '%s, %s) RETURNING id '
    row_id = execute_query(query, (raw_data, dt, 'new', images))
    return row_id


def send_image(url):
    response = requests.get(url)
    dt = datetime.now()
    query = 'INSERT INTO "public"."pereval_images" ("date_added", "img") VALUES (%s, %s) RETURNING id'
    row_id = execute_query(query, (dt, response.content))
    return row_id


def execute_query(query, params):
    conn = psycopg2.connect(dbname=config.FSTR_DB_NAME, user=config.FSTR_DB_LOGIN,
                            password=config.FSTR_DB_PASS, host=config.FSTR_DB_HOST, port=config.FSTR_DB_PORT)
    cur = conn.cursor()
    cur.execute(query, params)
    last_row_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return last_row_id
