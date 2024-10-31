import requests
import time
from config.config import api_config
from utils import create_games, reset_db, \
    create_combo, mock_purchase, create_user, delete_users, get_active_draws, get_games_from_set, \
    get_ticket_owners, get_tickets_sold, get_fortune_keys_per_order, get_fortune_keys_per_user, remove_key_tickets


def test_integration_clone_end_future(user_id, app_env, db_connection):
    """
    This test will break if not run before clone_end_date
    TESTING TIME -> current_time < clone_end_date < end_date
    """
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

    draws = get_games_from_set(db_connection, 1)

    first_draw = draws[0]
    tickets = get_tickets_sold(db_connection, first_draw['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 10
    assert revoked == 0

    # Create new game, assign 1 ticket
    body = create_combo(qty=1, is_multi=False, user_id=user_ids[1])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    draws = get_games_from_set(db_connection, 1)

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

    draws = get_games_from_set(db_connection, 1)

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

    response = remove_key_tickets(api_config[app_env], body)
    assert response.status_code == 200

    tickets = get_ticket_owners(db_connection, order_2_id)
    active, cancelled = 0, 0
    for t in tickets:
        if t['type'] == 1 or t['type'] == 2:
            active += 1
        if t['type'] == 3:
            cancelled += 1

    assert active == 4 and cancelled == 5

    draws = get_games_from_set(db_connection, 1)

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

    draws = get_games_from_set(db_connection, 1)
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
    body = create_combo(qty=1, is_multi=True, user_id=user_ids[3])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_6_id = response.json().get('orderId')
    order_6_tickets = get_ticket_owners(db_connection, order_6_id)
    order_6_keys = get_fortune_keys_per_order(db_connection, order_6_id)

    assert len(order_6_tickets) == len(order_6_keys) == 8
    assert len(set([t['draw_id'] for t in order_6_tickets])) == 8

    body = create_combo(qty=9, is_multi=True, user_id=user_ids[4])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_7_id = response.json().get('orderId')
    order_7_tickets = get_ticket_owners(db_connection, order_7_id)
    order_7_keys = get_fortune_keys_per_order(db_connection, order_7_id)

    assert len(order_7_tickets) == len(order_7_keys) == 8 * 9
    assert len(set([t['draw_id'] for t in order_7_tickets])) == 8

    user_1_keys, user_2_keys = get_fortune_keys_per_user(db_connection, user_ids[1]), get_fortune_keys_per_user(
        db_connection, user_ids[2])

    assert len(user_1_keys) == 0 and len(user_2_keys) == 0

    body = create_combo(qty=1, is_multi=True, user_id=user_ids[3])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    body = create_combo(qty=10, is_multi=True, user_id=user_ids[4])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    # Cancel 5 tickets in first game
    # Make sure tickets are cancelled
    body = {
        'tickets': [ticket['id'] for ticket in order_7_tickets[-5:]],
        'keys': [k['fkey_id'] for k in order_7_keys[-5:]]
    }
    response = requests.post(f'{api_config[app_env]}/remove-tickets-fkeys',
                  json={'body': body})
    assert response.status_code == 200

    tickets = get_ticket_owners(db_connection, order_7_id)
    active, cancelled = 0, 0
    cancelled_id = set()
    cancelled_tickets = [t for t in tickets if t['type'] == 3]
    for t in tickets:
        if t['type'] == 1 or t['type'] == 2:
            active += 1
        if t['type'] == 3:
            cancelled += 1
            cancelled_id.add(t['id'])

    assert set([t['id'] for t in order_7_tickets[-5:]]) == set([t['id'] for t in cancelled_tickets])
    assert active == (len(order_7_tickets) - cancelled) and cancelled == 5
    assert len(set([t['draw_id'] for t in cancelled_tickets])) == 1

    tickets_before_overflow = get_tickets_sold(db_connection, cancelled_tickets[0]['draw_id'])

    body = create_combo(qty=10, is_multi=True, user_id=user_ids[3])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    tickets_after_overflow = get_tickets_sold(db_connection, cancelled_tickets[0]['draw_id'])
    sold, revoked = len(tickets_after_overflow), sum(1 for t in tickets_after_overflow if t['type'] == 3)
    assert revoked == 5
    assert sold == 10 + len(tickets_before_overflow)


    # SINGLE + MULTI
    # Repeat the following steps but using multi tickets with users (1,2)
    # Ensure that the new users get keys correctly


def test_integration_clone_end_past(user_id, app_env, db_connection):
    """
       This test will break if not run before clone_end_date
       TESTING TIME -> clone_end_date < current_time < end_date
       """
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

    draws = get_games_from_set(db_connection, 1)

    first_draw = draws[0]
    assert first_draw['active'] == 0
    tickets = get_tickets_sold(db_connection, first_draw['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 10
    assert revoked == 0

    # Create new game, assign 1 ticket
    # Ticket should go into a new set
    body = create_combo(qty=1, is_multi=False, user_id=user_ids[1])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_3_id = response.json().get('orderId')
    order_3_tickets = get_ticket_owners(db_connection, order_3_id)
    assert len(set([t['draw_id'] for t in order_3_tickets])) == 1
    selected_draw = order_3_tickets[0]

    draws = get_games_from_set(db_connection, 2)
    assert len(draws) == 1
    draw = draws[0]
    assert draw['id'] == selected_draw['draw_id']
    assert draw['active'] == 1

    tickets = get_tickets_sold(db_connection, draw['id'])
    assert len(tickets) == 1

    # Overflow game
    body = create_combo(qty=10, is_multi=False, user_id=user_ids[2])
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    draws = get_games_from_set(db_connection, 2)

    assert len(draws) == 2
    assert draws[0]['active'] == 0 and draws[1]['active'] == 1

    tickets = get_tickets_sold(db_connection, draws[0]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert sold == 11

    # Cancel 5 tickets in first game
    # Make sure tickets are cancelled
    body = {
        'tickets': [ticket['id'] for ticket in order_2_tickets[:5]],
        'keys': []
    }

    response = remove_key_tickets(api_config[app_env], body)
    assert response.status_code == 200

    tickets = get_ticket_owners(db_connection, order_2_id)
    active, cancelled = 0, 0
    for t in tickets:
        if t['type'] == 1 or t['type'] == 2:
            active += 1
        if t['type'] == 3:
            cancelled += 1

    assert active == 4 and cancelled == 5

    draws = get_games_from_set(db_connection, 1)

    assert len(draws) == 1
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

    draws = get_games_from_set(db_connection, 1)
    assert len(draws) == 1
    tickets = get_tickets_sold(db_connection, draws[0]['id'])
    sold, revoked = len(tickets), sum(1 for t in tickets if t['type'] == 3)
    assert draws[0]['active'] == 0  # make sure draw is now considered active
    assert sold == 20
    assert revoked == 5
    assert sold - revoked >= draws[0]['ticket_limit']
