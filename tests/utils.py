import requests
from datetime import datetime

SERVICE_PERCTENT_FEE = 0.03
SERVICE_FLAT_FEE = 0.44
TICKET_PRICE = 1


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
    return (qty * SERVICE_PERCTENT_FEE) + SERVICE_FLAT_FEE


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
