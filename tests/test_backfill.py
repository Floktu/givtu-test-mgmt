import requests
from config.config import api_config


# Test Objective: Ensure that backfill is working for games where clone_end_date is in future
# 1. Purchase enough orders to close out a game
# 2. Cancel enough tickets to cause that game to open up again
# 3. Purchase another order and confirm that tickets are put into the right game
def test_backfill_working_before_clone_end_date(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that backfill is working where clone_end_date < time_now < end_date
# 1. Purchase enough orders to close out a game
# 2. Ensure no new game is cloned since clone_end_date lapsed
# 3. Cancel enough tickets to cause that game to open up again
# 4. Purchase another order and confirm that tickets are put into the right game
def test_backfill_working_before_end_date(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that cancelling tickets in a previously closed game does not open up the game and set
# 1. Purchase enough orders to close out a game
# 2. Update the set configuration so that the end_date has passed
# 3. Cancel tickets in the closed out game
# 4. Ensure game and set are not opened up again
def test_backfill_drawn_set(user_id, app_env, db_connection):
    pass
