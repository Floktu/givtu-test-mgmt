import mysql.connector
import redis
from flask import Flask, jsonify
from config.config import db_config

app = Flask(__name__)

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

def fetch_user_queue_counts():
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT id, email FROM user")
    users = cursor.fetchall()

    user_queue_counts = []
    for user in users:
        queue_key = f"user_queue:{user['id']}"
        queue_length = redis_conn.llen(queue_key)

        if queue_length > 0:
            user_queue_counts.append({
                'user_id': user['id'],
                'email': user['email'],
                'queue_count': queue_length
            })

    return user_queue_counts

@app.route('/active_draws', methods=['GET'])
def active_draws():
    draws = fetch_active_draws()
    draw_data = []

    for draw in draws:
        ticket_count = redis_conn.get(f"draw_id_{draw['id']}_ticket_count")
        ticket_count = ticket_count.decode() if ticket_count else "0"

        draw_data.append({
            'draw_id': draw['id'],
            'ticket_count': ticket_count,
            'launched_date': draw['launched_date'].strftime('%Y-%m-%d %H:%M:%S'),
            'end_date': draw['end_date'].strftime('%Y-%m-%d %H:%M:%S'),
            'clone_end_date': draw['clone_end_date'].strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify(draw_data)

@app.route('/user_queue_counts', methods=['GET'])
def user_queue_counts():
    user_queue_counts = fetch_user_queue_counts()
    return jsonify(user_queue_counts)

if __name__ == '__main__':
    app.run(debug=True)
