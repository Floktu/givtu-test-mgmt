import requests
from config.config import api_config


# Test Objective: Ensure that game cloning works correctly before clone_end_date
# 1. Purchase enough orders to close out a game
# 2. Ensure new game is created on next purchase
def test_game_cloning_before_clone_end_date(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that game cloning works correctly after clone_end_date
# 1. Purchase enough orders to close out a game
# 2. Ensure that for that set no new game is created
def test_game_cloning_after_clone_end_date(user_id, app_env, db_connection):
    pass

# Write more tests but for different cart combinations
