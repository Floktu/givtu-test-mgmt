import requests
import time
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from config.config import db_config, api_config

SERVICE_PERCENT_FEE = 0.03
SERVICE_FLAT_FEE = 0.44
TICKET_PRICE = 1
WAIT_SECONDS = 10


def get_games_from_set(conn, i):
    time.sleep(10)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
    select * from draws where draw_schedule_id = (
        SELECT MAX(id) as id
        FROM (
            SELECT id 
            FROM draw_schedule 
            WHERE active = 1 
            LIMIT %s
        ) AS subquery);''', (i,))
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def reset_db(conn):
    cursor = conn.cursor(dictionary=True)
    truncate_queries = [
        "SET FOREIGN_KEY_CHECKS = 0;",
        "Truncate Table payment;",
        "Truncate Table ticket_owners;",
        "Truncate Table order_ticket;",
        "Truncate Table orders;",
        "Truncate Table order_group;",
        "Truncate Table draft_orders;",
        "Truncate Table vouchers_transaction;",
        "Truncate Table subscription;",
        "Truncate Table subscription_logs;",
        "Truncate Table subscription_has_custom;",
        "Truncate Table subscription_qty_adjustment;",
        "Truncate Table draw_winners;",
        "Truncate Table dreamlist;",
        "Truncate Table bank_accounts;",
        "Truncate Table user_interests;",
        "Truncate Table user_reset_token;",
        "Truncate Table user_numbers;",
        "Truncate Table fortune_key_audit;",
        "Truncate Table fortune_draws;",
        "Truncate Table vouchers;",
        "Truncate Table draw_schedule;",
        "Truncate Table draws;",
        "Truncate Table drawing_winner_conf;",
        "Truncate Table voucher_conf;",
        "SET FOREIGN_KEY_CHECKS = 1;"  # Enable foreign key checks again after truncating
    ]

    # Execute each query separately
    for qry in truncate_queries:
        cursor.execute(qry)
    conn.commit()


def create_games(app_url):
    requests.get(f'{app_url}/apiv3/cron/create-games')


def create_short_games(app_url):
    requests.get(f'{app_url}/apiv3/cron/create-short-games')


def calculate_service_fee(qty):
    return (qty * SERVICE_PERCENT_FEE) + SERVICE_FLAT_FEE


def create_combo(qty, is_multi, user_id):
    trans_service_fee = calculate_service_fee(qty)
    trans_total = qty + trans_service_fee

    body = {
        'transTotal': trans_total,
        'transServiceFee': trans_service_fee,
        'subdomain': "",
        'numOfGames': 8 if is_multi else 1,
        'userid': user_id,
        'cartlist': [
            {
                'isgroup': 0,
                'charityid': 35,
                'prizeid': 74,
                'qty': qty,
                'prize': 'LG Signature',
                'nfp': 'Backtrack',
                'amount': 1,
                'draw': 54,
                'image': '/prizes/prize_74/cubeImage20240812133802.png',
                'subscription': 1 if is_multi else 0,
                'customprize': "",
                'customnfp': "",
                'hascustom': 0
            }
        ]
    }
    return body


def delete_users(conn):
    cursor = conn.cursor(dictionary=True)
    query = """
            DELETE from user where password = "TEST";   
            """
    cursor.execute(query)
    conn.commit()


def create_user(i, conn):
    cursor = conn.cursor(dictionary=True)

    query = """
        INSERT INTO user (email, roles, password, is_verified, firstname, lastname, created)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

    # Define values for the fake user
    email = f"user{i}@example.com"
    roles = '["ROLE_USER"]'
    password = "TEST"
    is_verified = 1
    firstname = f"User{i}"
    lastname = f"Test{i}"
    created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Execute the query
    cursor.execute(query, (email, roles, password, is_verified, firstname, lastname, created))
    conn.commit()
    # Get the ID of the newly inserted user
    user_id = cursor.lastrowid

    return user_id


def mock_purchase(api, body):
    return requests.post(f'{api}/test-purchase', json=body)


def get_active_draws(conn):
    time.sleep(WAIT_SECONDS)
    cursor = conn.cursor(dictionary=True)
    grouped = {}
    draw_schedules = get_active_sets(conn)

    for idx, ds in enumerate(draw_schedules):
        cursor.execute(
            "SELECT * from draws where draw_schedule_id = %s order by launched_date",
            (ds['id'],))
        results = cursor.fetchall()
        grouped[idx + 1] = results

    cursor.close()
    conn.commit()
    return grouped


def get_active_sets(conn):
    time.sleep(WAIT_SECONDS)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from draw_schedule where active = 1")
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def get_ticket_owners(conn, order_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * from ticket_owners where order_ticket_id in (select id from order_ticket where orders_id = %s)",
        (order_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def get_tickets_sold(conn, draw_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * from ticket_owners where draw_id = %s",
        (draw_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def get_fortune_keys_per_order(conn, order_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * from fortune_key_audit where orders_id = %s",
        (order_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def get_fortune_keys_per_user(conn, user_id):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * from fortune_key_audit where user_id = %s",
        (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.commit()
    return results


def remove_key_tickets(api, body):
    return requests.post(f'{api}/remove-tickets-fkeys',
                         json={'body': body})


def sleep():
    time.sleep(WAIT_SECONDS)


if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(**db_config['staging'])
        reset_db(connection)
        create_games(api_config['staging'])
    except Error as e:
        print(f"Error: {e}")
        raise e
