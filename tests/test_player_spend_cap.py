import requests
from config.config import api_config


# Test Objective: Ensure that max player spend cap rules are working for multi ticket purchase
# 1. Clear DB or figure out how many ticket's player currently has for set 1
# 2. Purchase enough tickets to reach player spend cap (250 single tickets)
# 3. Purchase another order and confirm that player spend cap rule is reached (will return error code)
def test_player_spend_cap_single_tickets(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that max player spend cap rules are working for single ticket purchases
# 1. Clear DB or figure out how many ticket's player currently has for set 1
# 2. Purchase enough tickets to reach player spend cap (250 multi tickets)
# 3. Purchase another order and confirm that player spend cap rule is reached (will return error code)
def test_player_spend_cap_multi_tickets(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that max player spend cap rules are working for single and multi ticket purchases in same cart
# 1. Clear DB or figure out how many ticket's player currently has for set 1
# 2. Purchase enough tickets to reach player spend cap (combination of single and multi to reach 250 tickets)
# 3. Purchase another order and confirm that player spend cap rule is reached (will return error code)
def test_player_spend_cap_single_multi_combo_cart(user_id, app_env, db_connection):
    pass
