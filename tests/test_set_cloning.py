import requests
from config.config import api_config


# Test Objective: Ensure that set cloning works correctly before end_date
# 1. Adjust set time so that first set clone_end_date < time_now < end_date
# 2. Purchase enough tickets to close out the game for this set
# 3. Trigger set cloning api (/apiv3/cron/clone-first-set)
# 4. Ensure that new set has been created (make sure that new set time is correct -> repeat_number)
# 5. Ensure previous set has an active status = 0 (inactive)
def test_set_cloning_after_clone_end_before_end_date(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that set cloning works correctly after end_date
# 1. Adjust set time so that first set time_now > end_date
# 2. Trigger set cloning api (/apiv3/cron/clone-first-set)
# 3. Ensure that new set has been created (make sure that new set time is correct -> repeat_number)
# 4. Ensure previous set has an active status = 0 (inactive)
def test_game_cloning_after_end_date(user_id, app_env, db_connection):
    pass

