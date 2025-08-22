import mysql.connector
import redis
import time
import curses
# Add the parent directory to sys.path
import sys
import os
from datetime import datetime

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
print("Current sys.path:", sys.path)
from config.config import db_config

if __name__ == "__main__":
    # MySQL connection setup
    mysql_conn = mysql.connector.connect(**db_config['staging'])

    # Redis connection setup
    redis_conn = redis.StrictRedis.from_url(
        "redis://default:3UGSq4MYHCmWazo3ESzCPxxDrefHdhdw@redis-19560.c291.ap-southeast-2-1.ec2.redns.redis-cloud.com:19560"
    )

    def fetch_active_draws():
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT id, launched_date, end_date, clone_end_date FROM draws WHERE active = 1 ORDER BY end_date")
        return cursor.fetchall()

    def get_ticket_count(draw_id):
        ticket_count = redis_conn.get(f"draw_id_{draw_id}_ticket_count")
        return ticket_count.decode() if ticket_count else "0"

    def format_date(date_value):
        """Format the date value into a readable format."""
        if isinstance(date_value, datetime):
            # If the date is already a datetime object, format it directly
            return date_value.strftime('%Y-%m-%d %H:%M:%S')
        try:
            # If it's a string, parse it and then format it
            return datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return str(e)

    def fetch_user_queue_counts():
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, email
            FROM user
        """)
        users = cursor.fetchall()

        user_queue_counts = {}
        for user in users:
            user_id = user['id']
            user_queue_key = f"user_queue:{user_id}"
            queue_items = redis_conn.llen(user_queue_key)  # Get length of the list in Redis

            # Only consider users with more than 0 items in their queue
            if queue_items > 0:
                user_queue_counts[user_id] = {
                    'email': user['email'],
                    'queue_count': queue_items
                }

        return user_queue_counts

    def refresh_screen(screen):
        curses.curs_set(0)  # Hide cursor
        screen.clear()
        screen.nodelay(True)  # Non-blocking input

        # Define column headers and column widths for alignment
        headers = ["Draw ID", "Tickets Sold", "Launched Date", "End Date", "Clone End Date", "User ID", "Email", "Queue Count"]
        col_widths = [10, 15, 20, 20, 20, 12, 30, 15]

        # Initialize previous ticket counts
        previous_ticket_counts = {}

        while True:
            screen.clear()
            active_draws = fetch_active_draws()
            user_queue_counts = fetch_user_queue_counts()  # Fetch user queue counts

            # Display headers with appropriate spacing
            header_row = " | ".join(f"{header:<{width}}" for header, width in zip(headers, col_widths))
            screen.addstr(0, 0, header_row)

            # Create a horizontal line for header separation
            screen.addstr(1, 0, "-" * (sum(col_widths) + 9))  # Horizontal line under headers

            # Display each draw's data aligned to the column widths
            row_index = 2  # Start after the header
            for draw in active_draws:
                ticket_count = get_ticket_count(draw['id'])

                # Flash the ticket count if it changes
                if ticket_count != previous_ticket_counts.get(draw['id']):
                    # Ticket count has changed, flash it
                    screen.addstr(row_index, col_widths[0] + col_widths[1], f"{ticket_count:<{col_widths[1]}}", curses.A_REVERSE)
                    previous_ticket_counts[draw['id']] = ticket_count
                else:
                    # If no change, display normally
                    screen.addstr(row_index, col_widths[0] + col_widths[1], f"{ticket_count:<{col_widths[1]}}")

                # Format dates properly
                launched_date = format_date(draw['launched_date'])
                end_date = format_date(draw['end_date'])
                clone_end_date = format_date(draw['clone_end_date'])

                draw_row = (
                    f"{draw['id']:<{col_widths[0]}} | "
                    f"{ticket_count:<{col_widths[1]}} | "
                    f"{launched_date:<{col_widths[2]}} | "
                    f"{end_date:<{col_widths[3]}} | "
                    f"{clone_end_date:<{col_widths[4]}}"
                )

                # Add row to the screen for the draw
                screen.addstr(row_index, 0, draw_row)

                # Now add user queue info below the draw
                for user_id, user_info in user_queue_counts.items():
                    user_row = (
                        f"{user_id:<{col_widths[5]}} | "
                        f"{user_info['email']:<{col_widths[6]}} | "
                        f"{user_info['queue_count']:<{col_widths[7]}}"
                    )
                    row_index += 1
                    screen.addstr(row_index, 0, user_row)

                row_index += 1  # Add a row break between draw rows

            screen.refresh()
            time.sleep(1)  # Refresh interval

            # Check for a key press to exit
            if screen.getch() == ord("q"):
                break

        curses.endwin()

    # Run the curses display
    curses.wrapper(refresh_screen)

    # Close connections when done
    mysql_conn.close()
