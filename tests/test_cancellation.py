import requests
import time
from config.config import api_config
from utils import create_games, reset_db, \
    create_combo, mock_purchase, create_user, delete_users, get_active_draws, get_games_from_set, \
    get_ticket_owners, get_tickets_sold, get_fortune_keys_per_order, get_fortune_keys_per_user, remove_key_tickets


def test_cancel_tickets(user_id, app_env, db_connection):
    reset_db(db_connection)
    create_games(api_config[app_env])
    delete_users(db_connection)
    user = create_user(1, db_connection)

    body = create_combo(qty=1, is_multi=True, user_id=user)
    response = mock_purchase(api_config[app_env], body)
    assert response.status_code == 200

    order_id = response.json().get('orderId')
    tickets = get_ticket_owners(db_connection, order_id)
    keys = get_fortune_keys_per_order(db_connection, order_id)

    body = {
        'tickets': [ticket['id'] for ticket in tickets],
        'keys': [key['fkey_id'] for key in keys]
    }

    response = remove_key_tickets(api_config[app_env], body)
    assert response.status_code == 200

    tickets = get_ticket_owners(db_connection, order_id)
    keys = get_fortune_keys_per_user(db_connection, user)
    assert len(keys) == 16 and len(tickets) == 8

    assert sum(1 for t in tickets if t['type'] == 3) == 8

    assert sum(1 for k in keys if k['type'] == 1) == 8

    assert sum(1 for k in keys if k['type'] == 2) == 8
