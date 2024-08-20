import time

import requests

from config.config import api_config
from utils import create_games, reset_db, create_combo, mock_purchase, create_user, delete_users


def get_first_set_games(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from draws where draw_schedule_id = (SELECT id from draw_schedule where id = 1)")
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


def test_integration_clone_end_future(user_id, app_env, db_connection):
    reset_db(db_connection)
    create_games(api_config[app_env])
    # Create User1, User2, User3, User4
    delete_users(db_connection)
    user_ids = {}
    for i in range(1, 5):
        user_ids[i] = create_user(i, db_connection)

    # purchase 1 ticket
    body = create_combo(qty=1, is_multi=False, user_id=user_ids[1])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    # purchase 9 tickets, make sure game 1 is full
    body = create_combo(qty=9, is_multi=False, user_id=user_ids[2])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_2_id = response.json().get('orderId')
    order_2_tickets = get_ticket_owners(db_connection, order_2_id)

    time.sleep(5)
    draws = get_first_set_games(db_connection)

    first_draw = draws[0]
    tickets = get_tickets_sold(db_connection, first_draw['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 10
    assert revoked == 0

    # Create new game, assign 1 ticket
    body = create_combo(qty=1, is_multi=False, user_id=user_ids[1])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    time.sleep(5)
    draws = get_first_set_games(db_connection)

    assert len(draws) == 2
    assert draws[0]['active'] == 0
    assert draws[1]['active'] == 1
    tickets = get_tickets_sold(db_connection, draws[1]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 1

    # Overflow game
    body = create_combo(qty=10, is_multi=False, user_id=user_ids[2])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    time.sleep(5)
    draws = get_first_set_games(db_connection)

    assert len(draws) >= 2
    assert draws[0]['active'] == 0 and draws[1]['active'] == 0

    tickets = get_tickets_sold(db_connection, draws[1]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 11

    # Cancel 5 tickets in first game
    # Make sure tickets are cancelled
    body = {
        'tickets': [ticket['id'] for ticket in order_2_tickets[:5]],
        'keys': []
    }
    requests.post(f'{api_config[app_env]}/remove-tickets-fkeys',
                  json={'body': body})

    tickets = get_ticket_owners(db_connection, order_2_id)
    active, cancelled = 0, 0
    for t in tickets:
        if t['type'] == 1 or t['type'] == 2:
            active += 1
        if t['type'] == 3:
            cancelled += 1

    assert active == 4 and cancelled == 5

    time.sleep(5)
    draws = get_first_set_games(db_connection)

    assert len(draws) >= 2
    assert draws[0]['active'] == 1  # make sure draw is now considered active

    tickets = get_tickets_sold(db_connection, draws[0]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 10 and revoked == 5

    # Allocate 10 tickets, makes sure it overflows the first game
    body = create_combo(qty=10, is_multi=False, user_id=user_ids[2])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_5_id = response.json().get('orderId')
    order_5_tickets = get_ticket_owners(db_connection, order_5_id)

    time.sleep(5)
    draws = get_first_set_games(db_connection)
    assert len(draws) >= 2
    tickets = get_tickets_sold(db_connection, draws[0]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert draws[0]['active'] == 0  # make sure draw is now considered active
    assert sold == 20
    assert revoked == 5
    assert sold - revoked >= draws[0]['ticket_limit']
    # Buy enough tickets to fill up the final game

    # MULTI
    # Repeat the following steps but using multi tickets with different users (3,4)
    # Ensure that the new users get keys correctly
    # Ensure that the old previous users do not get keys (single no active fortune status)

    # SINGLE + MULTI
    # Repeat the following steps but using multi tickets with users (1,2)
    # Ensure that the new users get keys correctly
