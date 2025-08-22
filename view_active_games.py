import mysql.connector
import redis
import time
import curses
from config import config

# MySQL connection setup
mysql_conn = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_mysql_database"
)

# Redis connection setup
redis_conn = redis.StrictRedis.from_url(
    "redis://default:3UGSq4MYHCmWazo3ESzCPxxDrefHdhdw@redis-19560.c291.ap-southeast-2-1.ec2.redns.redis-cloud.com:19560"
)


def fetch_active_draws():
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT id, launched_date, end_date, clone_end_date FROM draws WHERE active = 1")
    return cursor.fetchall()


def get_ticket_count(draw_id):
    return redis_conn.get(f"draw_id_{draw_id}_ticket_count")


def refresh_screen(screen):
    curses.curs_set(0)  # Hide cursor
    screen.clear()
    screen.nodelay(True)  # Non-blocking input

    while True:
        screen.clear()
        active_draws = fetch_active_draws()

        screen.addstr(0, 0, "Active Draws with Ticket Count")
        screen.addstr(1, 0, "-" * 40)

        for index, draw in enumerate(active_draws, start=2):
            ticket_count = get_ticket_count(draw['id'])
            ticket_count_display = ticket_count.decode() if ticket_count else "0"

            draw_info = f"Draw ID: {draw['id']} | Tickets Sold: {ticket_count_display} | Launched: {draw['launched_date']} | End: {draw['end_date']}"
            screen.addstr(index, 0, draw_info)

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
