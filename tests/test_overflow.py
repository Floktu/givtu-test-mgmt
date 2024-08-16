import requests
from config.config import api_config


# Test Objective: Ensure that overflow works correctly with single tickets
# 1. Clear DB or figure out what the current tickets sold and tickets remaining are for the first game
# 2. Purchase enough tickets to fill up game, confirm game is full
# 3. Purchase another order and confirm that a new game has been created
# 4. Confirm that new order tickets are allocated to new game
def test_overflow_single_tickets(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that overflow works correctly with multi tickets
# 1. Clear DB or figure out what the current tickets sold and tickets remaining are for the next 8 games
# 2. Purchase enough multi tickets to fill up games
# 3. Purchase another order and confirm that all games have been re-cloned
# 4. Confirm that new order tickets are allocated to new game
def test_overflow_multi_tickets(user_id, app_env, db_connection):
    pass



