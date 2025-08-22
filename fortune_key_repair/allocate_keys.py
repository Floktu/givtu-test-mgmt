from datetime import datetime, timedelta
import mysql.connector
from config.config import db_config

connection = mysql.connector.connect(**db_config['prod'])
cursor = connection.cursor()


def key_to_number(key):
    # Ensure key is uppercase for consistency
    key = key.upper()

    # Define the base-26 to letter mapping
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize the result number
    number = 0

    # Iterate through each character in the key
    for char in key:
        # Find the index of the character in letters
        index = letters.index(char)
        # Multiply the current number by 26 and add the index
        number = number * 26 + (index)  # +1 to adjust for 1-based indexing

    return number + 1


def fetch_audit_records(user_id):
    """
    Fetch records from the 'fortune_key_audit' table for a given user_id.
    """
    query = "SELECT * FROM fortune_key_audit WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


def fetch_fortune_keys(ids):
    """
    Fetch records from the 'fortune_keys' table for a given list of IDs.
    """
    if not ids:
        return []

    placeholders = ','.join(['%s'] * len(ids))
    query = f"SELECT * FROM fortune_keys WHERE id IN ({placeholders}) and status is null"
    cursor.execute(query, ids)
    return cursor.fetchall()


def update_fortune_keys(records):
    """
    Update the 'fortune_keys' table with values derived from audit records.
    """
    update_query = """
       UPDATE fortune_keys
       SET 
           status = %s,
           category = %s, 
           allocated_date = %s,
           active_date = %s,
           user_id = %s,
           order_id = %s,
           fortune_draw_id = %s
       WHERE id = %s and status is null
       """
    for record in records:
        status = 1
        category = record[3]
        allocated_date = record[6]
        active_date = record[7]
        user_id = record[1]
        order_id = record[2]
        fortune_draw_id = record[4]
        id = key_to_number(record[5])

        query_str = update_query % (
            repr(status),
            repr(category),
            repr(allocated_date),
            repr(active_date),
            repr(user_id),
            repr(order_id),
            repr(fortune_draw_id),
            repr(id)
        )

        print(query_str)
        # Execute update query
        cursor.execute(update_query, (status, category, allocated_date, active_date, user_id, order_id, fortune_draw_id, id))

    # Commit changes to the database
    connection.commit()


if __name__ == "__main__":
    user_id = 53  # Replace with the desired user_id
    audit_records = fetch_audit_records(user_id)
    ids = [key_to_number(record[5]) for record in audit_records]
    keys = fetch_fortune_keys(ids)
    fkeys = sorted([record[2] for record in keys])
    audit_fkeys = sorted([record[5] for record in audit_records])

    if fkeys == audit_fkeys:
        print("The records are exactly the same.")
        if audit_records:
            print(f"Fetched {len(audit_records)} records for user_id {user_id}.")
            update_fortune_keys(audit_records)
            print(f"Updated 'fortune_keys' table successfully.")
        else:
            print(f"No records found for user_id {user_id}.")
    else:
        print("The records are NOT the same.")

    # Close the database connection
    cursor.close()
    connection.close()
