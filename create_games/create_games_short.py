from datetime import datetime, timedelta
import mysql.connector
from config.config import db_config
from tests.utils import reset_db

draw_winner_conf = [
    {"quantity": 1, "label_desc": "GRAND PRIZE", "ticket_type": 1, "draw_order": 1, "value": 2500},
    {"quantity": 50, "label_desc": "$25", "ticket_type": 0, "draw_order": 1, "value": 25},
    {"quantity": 5000, "label_desc": "FREE TICKET", "ticket_type": 2, "draw_order": 2, "value": None},
    {"quantity": 5000, "label_desc": "FORTUNE KEYS", "ticket_type": 3, "draw_order": 1, "value": None},
]


def get_datetime_now():
    return datetime.now()


def main():
    connection = mysql.connector.connect(**db_config['dev'])
    reset_db(connection)
    current_date = get_datetime_now()
    if current_date.minute != 0 or current_date.second != 0:
        current_date = current_date.replace(minute=0, second=0, microsecond=0)

    set_date = current_date
    fortune_draw_date = current_date

    draw_schedules = []
    draws = []
    fortune_draws = []

    for i in range(16):
        start_date = set_date
        end_date = start_date + timedelta(minutes=60)
        clone_end_date = start_date + timedelta(minutes=50)

        draw_schedule = {
            'name': f'Short Game {i + 1}',
            'subdomain': '',
            'start_date': start_date,
            'end_date': end_date,
            'ticket_limit': 10,
            'repeat_number': 320,
            'active': True,
            'updated': get_datetime_now(),
            'prize_setting': 0,
            'nfp_setting': 0,
            'clone_end_date': clone_end_date,
            'is_continuous': 1,
            'repeat_type': 'Minute/s',
            'child_set': 0,
            'is_split': 1,
            'auto_draw_enabled': 1,
        }

        set_query = f'''INSERT INTO draw_schedule
                (name, subdomain, start_date, end_date, ticket_limit, repeat_number, active, prize_setting,
                nfp_setting, clone_end_date, is_continuous, repeat_type, child_set, is_split, auto_draw_enabled, updated)
                VALUES ('{draw_schedule['name']}', '{draw_schedule['subdomain']}', '{draw_schedule['start_date']}', '{draw_schedule['end_date']}', 
                {draw_schedule['ticket_limit']}, {draw_schedule['repeat_number']}, {draw_schedule['active']}, {draw_schedule['prize_setting']},
                {draw_schedule['nfp_setting']}, '{draw_schedule['clone_end_date']}', {draw_schedule['is_continuous']}, '{draw_schedule['repeat_type']}',
                {draw_schedule['child_set']}, {draw_schedule['is_split']}, {draw_schedule['auto_draw_enabled']}, '{draw_schedule['updated']}');'''
        print(set_query)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(set_query)
        draw_schedule_id = cursor.lastrowid

        draw = {
            'name': f'Short Game {i + 1}',
            'subdomain': '',
            'end_date': end_date,
            'launched_date': start_date,
            'prize_setting': 0,
            'nfp_setting': 0,
            'active': True,
            'ticket_limit': 10,
            'hidden': False,
            'draw_schedule_id': draw_schedule_id,
            'clone_end_date': clone_end_date,
            'auto_draw_enabled': 1,
            'tickets_sold': 0,
            'tickets_revoked': 0,
            'created': get_datetime_now()
        }

        draw_query = f'''INSERT INTO draws
         (name, subdomain, launched_date, end_date, ticket_limit, active, prize_setting,
         nfp_setting, clone_end_date, auto_draw_enabled, created, draw_schedule_id)
         VALUES ('{draw['name']}', '{draw['subdomain']}', '{draw['launched_date']}', '{draw['end_date']}',
         {draw['ticket_limit']},  {draw['active']}, {draw['prize_setting']},
         {draw['nfp_setting']}, '{draw['clone_end_date']}',
         {draw['auto_draw_enabled']}, '{draw['created']}', {draw_schedule_id});'''
        print(draw_query)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(draw_query)

        for dwc in draw_winner_conf:
            if dwc['value']:
                dwc_query = f'''INSERT INTO drawing_winner_conf
                    (quantity, label_desc, ticket_type, draw_order, value, draw_schedule_id)
                    VALUES ({dwc['quantity']}, '{dwc['label_desc']}', {dwc['ticket_type']}, {dwc['draw_order']},
                    {dwc['value']},  {draw_schedule_id});'''
            else:
                dwc_query = f'''INSERT INTO drawing_winner_conf
                    (quantity, label_desc, ticket_type, draw_order, draw_schedule_id)
                    VALUES ({dwc['quantity']}, '{dwc['label_desc']}', {dwc['ticket_type']}, {dwc['draw_order']},
                    {draw_schedule_id});'''
            print(dwc_query)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(dwc_query)

        draws.append(draw)
        set_date += timedelta(minutes=40)

    draw_amount = 10000
    fortune_draw_date += timedelta(hours=2)
    cursor = connection.cursor(dictionary=True)
    for i in range(1000):
        draw_date = fortune_draw_date
        fortune_draw = {
            'draw_amount': min(draw_amount, 1000000),
            'draw_amount_reset': draw_amount // 2,
            'draw_date': draw_date,
            'draw_num': i + 1,
            'lock_draw': False,
            'fortune_group': 0,
        }
        fortune_draw_query = f'''INSERT INTO fortune_draws
            (draw_amount, draw_date, draw_num, draw_amount_reset, fortune_group )
             VALUES ({fortune_draw['draw_amount']}, '{fortune_draw['draw_date']}', {i + 1}, 
             {fortune_draw['draw_amount_reset']}, {fortune_draw['fortune_group']});'''
        print(fortune_draw_query)
        cursor.execute(fortune_draw_query)
        fortune_draws.append(fortune_draw)
        fortune_draw_date += timedelta(minutes=80)
        draw_amount *= 2

        connection.commit()


if __name__ == "__main__":
    main()
