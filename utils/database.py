import json
from datetime import datetime

import psycopg2
import requests

import utils.config as config


def get_filtered_data(fio, telephone, email):
    params = []
    params_str = []
    if fio is not None:
        params.append(fio)
        params_str.append("raw_data::json->'user'->>'id' = %s")
    if telephone is not None:
        params.append(telephone)
        params_str.append("raw_data::json->'user'->>'phone' = %s")
    if email is not None:
        params.append(email)
        params_str.append("raw_data::json->'user'->>'email' = %s")
    params_str = " AND ".join(params_str)
    query = f'SELECT raw_data FROM "public"."pereval_added" WHERE {params_str}'
    return execute_query(query, params, fetchall=True)


def update_data(data_id, raw_data):
    query = 'UPDATE "public"."pereval_added" SET raw_data = %s WHERE id = %s;'
    execute_query(query, (raw_data, data_id), onlyexecute=True)


def get_status(data_id):
    query = 'SELECT status FROM "public"."pereval_added" WHERE id = %s'
    return execute_query(query, (data_id,))


def get_data_by_id(data_id):
    query = 'SELECT raw_data FROM "public"."pereval_added" WHERE id = %s'
    return execute_query(query, (data_id,))


def send_data(data, images_dict):
    images = json.dumps(images_dict)
    raw_data = json.dumps(data)
    dt = datetime.now()
    query = 'INSERT INTO "public"."pereval_added" ("raw_data", "date_added", "status", "images") VALUES (%s, %s, ' \
            '%s, %s) RETURNING id '
    return execute_query(query, (raw_data, dt, 'new', images))


def send_image(url):
    response = requests.get(url)
    dt = datetime.now()
    query = 'INSERT INTO "public"."pereval_images" ("date_added", "img") VALUES (%s, %s) RETURNING id'
    return execute_query(query, (dt, response.content))


def execute_query(query, params, fetchall=False, onlyexecute=False):
    conn = psycopg2.connect(dbname=config.FSTR_DB_NAME, user=config.FSTR_DB_LOGIN,
                            password=config.FSTR_DB_PASS, host=config.FSTR_DB_HOST, port=config.FSTR_DB_PORT)
    cur = conn.cursor()
    cur.execute(query, params)
    if onlyexecute:
        conn.commit()
        cur.close()
        conn.close()
        return
    if fetchall:
        result = cur.fetchall()
    else:
        result = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return result
