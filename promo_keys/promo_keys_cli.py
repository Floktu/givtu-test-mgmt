import csv
import math
import requests
import click
import mysql.connector
from datetime import datetime
from tabulate import tabulate
from config.config import db_config


def get_keys_status(db_connection, date, page_size=10):
    # Convert date string to datetime for comparison
    eval_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Step 1: Get the total number of users
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    total_users = cursor.fetchone()[0]

    # Calculate the total number of pages
    total_pages = (total_users // page_size) + (1 if total_users % page_size > 0 else 0)

    current_page = 0  # Start with the first page

    while True:
        click.clear()
        # Step 2: Fetch a batch of user information
        offset = current_page * page_size
        users_query = """
        SELECT id, email, firstname, lastname 
        FROM user
        LIMIT %s OFFSET %s
        """
        cursor.execute(users_query, (page_size, offset))
        users = cursor.fetchall()

        # Step 3: For each user, get the active and total keys
        results = []
        for user in users:
            user_id, email, first_name, last_name = user
            keys_query = """
            SELECT 
                COALESCE(SUM(CASE WHEN assign_date <= %s THEN 1 ELSE 0 END), 0) AS active_keys, 
                COALESCE(COUNT(*), 0) AS total_keys
            FROM fortune_keys
            WHERE current_user_id = %s
            """
            cursor.execute(keys_query, (eval_date, user_id))
            active_keys, total_keys = cursor.fetchone()

            results.append((user_id, email, first_name, last_name, active_keys, total_keys))

        # Display results in a pretty printed table
        headers = ['User ID', 'Email', 'First Name', 'Last Name', 'Active Keys', 'Total Keys']
        click.echo(tabulate(results, headers=headers, tablefmt='pretty'))

        # Step 4: Prompt user for navigation
        if current_page == 0:
            click.echo("Type 'n' for next page.")
        elif 0 < current_page < total_pages - 1:
            click.echo("Type 'b' to go back, or 'n' for next page.")
        else:
            click.echo("Type 'b' for next page.")

        click.echo(f"Page {current_page + 1} of {total_pages}.")
        user_input = click.prompt("Enter your choice", default="n", show_default=False)

        if user_input.lower() == 'n':
            if current_page < total_pages - 1:
                current_page += 1
            else:
                click.echo("You are already on the last page.")
        elif user_input.lower() == 'b':
            if current_page > 0:
                current_page -= 1
            else:
                click.echo("You are already on the first page.")
        else:
            try:
                page_number = int(user_input)
                if 1 <= page_number <= total_pages:
                    current_page = page_number - 1
                else:
                    click.echo(f"Please enter a valid page number between 1 and {total_pages}.")
            except ValueError:
                click.echo("Invalid input. Please enter 'b', 'n', or a valid page number.")

    cursor.close()


def allocate(db_connection, method, value, eval_date, active_date, only_active_keys=False):
    # Convert eval_date string to datetime for comparison, if provided
    cursor = db_connection.cursor()

    users_query = """
          SELECT id, email, firstname, lastname 
          FROM user
          """
    cursor.execute(users_query)
    users = cursor.fetchall()

    total_users = len(users)
    # Step 3: For each user, get the active and total keys
    with click.progressbar(length=total_users, label=click.style('Allocating keys', fg='cyan'), show_eta=False) as bar:
        for user in users:
            user_id, email, first_name, last_name = user
            keys_query = """
                  SELECT 
                      COALESCE(SUM(CASE WHEN assign_date <= %s THEN 1 ELSE 0 END), 0) AS active_keys, 
                      COALESCE(COUNT(*), 0) AS total_keys
                  FROM fortune_keys
                  WHERE current_user_id = %s
                  """
            cursor.execute(keys_query, (eval_date, user_id))
            active_keys, total_keys = cursor.fetchone()

            amount = math.ceil(value)

            if method == 'percentage_increase':
                base = active_keys if only_active_keys else total_keys
                amount = math.ceil((value / 100) * base)

            # click.echo(f" Allocating {amount} keys to {first_name} {last_name}, active after {active_date}")
            # Step 4: Make the POST request to the Symfony endpoint
            post_data = {
                'amount': amount,
                'userId': user_id,
                'dateActive': active_date,
                'promotional': 'promo_code_example'  # Adjust this value as needed
            }

            response = requests.post('http://localhost:8741/apiv3/cron/allocate-promo-keys', json=post_data)

            if response.status_code == 200:
                click.echo(click.style(
                    f" Successfully allocated {amount} keys for {first_name} {last_name}, active after {active_date}.",
                    fg='green'))
            else:
                click.echo(
                    click.style(f" Failed to allocate keys for {first_name} {last_name}: {response.text}", fg='red'))
            bar.update(1)


@click.command()
@click.option('--date', required=True, help="Evaluation date and time in YYYY-MM-DD HH:MM:SS format.")
@click.option('--env', default="staging", help="Database environment to use (e.g., staging, production).")
@click.option('--page-size', default=10, help="Number of results per page.")
def show_keys(date, env, page_size):
    # Establish connection
    try:
        connection = mysql.connector.connect(**db_config[env])
    except mysql.connector.Error as err:
        click.echo(f"Error: {err}")
        return

    # Pass the date as a string to get_keys_status
    get_keys_status(connection, date, page_size)
    # Close the connection
    connection.close()


@click.command()
@click.option('--method', type=click.Choice(['fixed_qty', 'percentage_increase']), required=True)
@click.option('--value', type=float, required=True, help="Amount of keys to allocate.")
@click.option('--eval_date', required=True, help="Evaluation date in YYYY-MM-DD format for active key checks.")
@click.option('--active_date', required=True, help="Active date in YYYY-MM-DD format for promo keys.")
@click.option('--only_active_keys', is_flag=True, default=False, help="Use only active keys for calculation.")
@click.option('--env', default="dev", help="Database environment to use (e.g., dev, staging, production).")
@click.option('--filename', required=True, help="Base filename for before and after export files.")
def allocate_keys(method, value, eval_date, active_date, only_active_keys, env, filename):
    # Establish connection
    try:
        connection = mysql.connector.connect(**db_config[env])
    except mysql.connector.Error as err:
        click.echo(f"Error: {err}")
        return

    before_file = f"{filename}_before-allocation.csv"
    after_file = f"{filename}_after-allocation.csv"

    _export_key_table(eval_date, env, before_file)

    if method == 'percentage_increase' and not (0 < value < 100):
        raise Exception(f"Invalid value for percentage_increase {value}")

    allocate(connection, method, value, eval_date, active_date, only_active_keys)

    _export_key_table(eval_date, env, after_file)

    connection.close()


@click.command()
@click.option('--date', required=True, help="Evaluation date and time in YYYY-MM-DD HH:MM:SS format.")
@click.option('--env', default="staging", help="Database environment to use (e.g., staging, production).")
@click.option('--output', default="key_allocation.csv", help="Output CSV file name.")
def export_key_table(date, env, output):
    """Exports key allocation data to a CSV file."""
    # Establish connection
    _export_key_table(date, env, output)


def _export_key_table(date, env, output):
    try:
        connection = mysql.connector.connect(**db_config[env])
    except mysql.connector.Error as err:
        click.echo(f"Error: {err}")
        return

    # Get the data
    eval_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Fetch all user data and calculate active/total keys
    cursor = connection.cursor()
    users_query = """
       SELECT id, email, firstname, lastname 
       FROM user
       """
    cursor.execute(users_query)
    users = cursor.fetchall()

    results = []
    for user in users:
        user_id, email, first_name, last_name = user
        keys_query = """
           SELECT 
               COALESCE(SUM(CASE WHEN assign_date <= %s THEN 1 ELSE 0 END), 0) AS active_keys, 
               COALESCE(COUNT(*), 0) AS total_keys
           FROM fortune_keys
           WHERE current_user_id = %s
           """
        cursor.execute(keys_query, (eval_date, user_id))
        active_keys, total_keys = cursor.fetchone()
        results.append((user_id, email, first_name, last_name, active_keys, total_keys))

    cursor.close()
    headers = ['User ID', 'Email', 'First Name', 'Last Name', 'Active Keys', 'Total Keys']

    # Write results to a CSV file
    with open(output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(results)

    click.echo(f"Data successfully saved to {output}")

    # Close the database connection
    connection.close()


@click.group()
def cli():
    """Main entry point for the Click command line interface."""
    pass


# Register the commands with the CLI group
cli.add_command(show_keys)
cli.add_command(allocate_keys)
cli.add_command(export_key_table)

if __name__ == "__main__":
    cli()
