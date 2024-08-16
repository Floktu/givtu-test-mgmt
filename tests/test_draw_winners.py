import requests
from config.config import api_config


# Test Objective: Ensure that drawing of winners is correct
# 1. Purchase enough tickets to create a few games for the first set, use different user_ids (grab from db)
# 2. Adjust time so end date has passed
# 3. Trigger the draw winners api for that set (/apiv3/cron/run/set/{setId}) insert set id
# 4. Ensure that winners are draw correctly depending on winner config
#    - Check that major winners are draw for the qty of major winners
#    - Check that minor winners are drawn for minor winners
#    - Ensure that minor winners are have distinct winning tickets (ticket_owner_id) for each game in set
# 5. Ensure previous set has an active status = -1 (DRAWN)
def test_draw_winners(app_env, db_connection):
    pass


# Test Objective: Ensure that drawing of winners is correct before end_date
# 1. Trigger the draw winners api for that set (/apiv3/cron/run/set/{setId}) insert set id
# 2. Ensure that no winners are drawn (check db for winners in the set you attempted to draw winners from)
def test_draw_winners_before_end_date(app_env, db_connection):
    pass
