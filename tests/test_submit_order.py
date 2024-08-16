import requests
from config.config import api_config
from reset_app import reset_db


# Test Objective: Ensure that a single payment and ticket order is processed correctly.
# Steps to Implement:
# 1. Reset the database to a known state using `reset_db`.
# 2. Construct the API request body with a single ticket order.
# 3. Make an API call to create the order.
# 4. Assert that the API response is successful (HTTP 200) and contains a valid order ID.
# 5. Verify the order's details in the database:
#    - Check that the order exists and matches the expected data.
#    - Validate the associated `order_group` and `order_ticket` records.
#    - Ensure that the correct `ticket_owner` entries are created.
# 6. Close the database cursor.

def test_submit_order_single_ticket(user_id, app_env, db_connection):
    cursor = db_connection.cursor(dictionary=True)

    # 2. Prepare the request payload with order details
    body = {
        'transTotal': 1.47,
        'transServiceFee': 0.47,
        'subdomain': "",
        'numOfGames': 8,
        'userid': user_id,
        'cartlist': [
            {
                'isgroup': 0,
                'charityid': 35,
                'prizeid': 74,
                'qty': 1,
                'prize': 'LG Signature',
                'nfp': 'Backtrack',
                'amount': 1,
                'draw': 54,
                'image': '/prizes/prize_74/cubeImage20240812133802.png',
                'subscription': 0,
                'customprize': "",
                'customnfp': "",
                'hascustom': 0
            }
        ]
    }

    # 3. Make the API request to create the order
    response = requests.post(f'{api_config[app_env]}/test-purchase', json=body)

    # 4. Assert the response and extract the order ID
    assert response.status_code == 200
    order_id = response.json().get('orderId')
    assert order_id > 0

    # 5. Perform database checks to validate the order details

    # a. Verify the order in the 'orders' table
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order_res = cursor.fetchone()
    assert order_res['id'] == order_id

    # b. Verify the associated order group
    cursor.execute("SELECT * FROM order_group WHERE id = %s", (order_res['order_group_id'],))
    order_group_res = cursor.fetchone()
    assert order_group_res['id'] == order_res['order_group_id']

    # c. Verify the order ticket details
    cursor.execute("SELECT * FROM order_ticket WHERE orders_id = %s", (order_id,))
    order_ticket_res = cursor.fetchone()
    assert order_ticket_res['quantity'] == 1

    # d. Verify the ticket owner records
    cursor.execute("SELECT * FROM ticket_owners WHERE order_ticket_id = %s", (order_ticket_res['id'],))
    ticket_owner_res = cursor.fetchall()
    assert len(ticket_owner_res) == 1 and ticket_owner_res[0]['type'] == 1

    # e. Verify that Game Records have the right amount of tickets allocated

    # e. Verify the payments records

    # 6. Close the cursor
    cursor.close()


# Test Objective: Ensure that a multi ticket order is processed correctly.
# 1. Check all order and ticket related tables are populated
# 2. Check that subscription is created correctly
# 3. Check that fortune keys are allocated correctly
def test_submit_order_multi_ticket(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that 1 single and 1 multi ticket combo in same cart are processed correctly.
# 1. Check all order and ticket related tables are populated
# 2. Check that subscription is created correctly for multi
# 3. Check that fortune keys are allocated correctly
def test_submit_order_single_and_multi_tickets(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that multiple single ticket in combos in same cart are processed correctly.
# 1. Check all order and ticket related tables are populated
# 2. Check that fortune keys are allocated correctly if applicable
def test_submit_order_multiple_single_tickets(user_id, app_env, db_connection):
    pass


# Test Objective: Ensure that multiple single ticket in combos in same cart are processed correctly.
# 1. Check all order and ticket related tables are populated
# 2. Check that subscription is created correctly for multi
# 3. Check that fortune keys are allocated correctly
def test_submit_order_multiple_multi_tickets(user_id, app_env, db_connection):
    pass


