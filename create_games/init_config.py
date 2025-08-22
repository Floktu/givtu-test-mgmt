from datetime import datetime, timedelta
import mysql.connector
from config.config import db_config
from tests.utils import reset_db


fortune_draws = [
    {"draw_amount": 100000, "draw_date": "02/03/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 1},
    {"draw_amount": 200000, "draw_date": "09/03/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 2},
    {"draw_amount": 300000, "draw_date": "16/03/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 3},
    {"draw_amount": 400000, "draw_date": "23/03/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 3},
    {"draw_amount": 500000, "draw_date": "30/03/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 5},
    {"draw_amount": 600000, "draw_date": "06/04/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 6},
    {"draw_amount": 700000, "draw_date": "11/05/2025 18:00:00", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_num": 7},
]


draw_winner_conf = [
    {"quantity": 1, "label_desc": "GRAND PRIZE", "ticket_type": 1, "draw_order": 1, "value": 2500},
    {"quantity": 80, "label_desc": "$25", "ticket_type": 0, "draw_order": 1, "value": 25},
    {"quantity": 1500, "label_desc": "Free Entries", "ticket_type": 2, "draw_order": 2, "value": None},
    {"quantity": 7500, "label_desc": "Fortune Keys", "ticket_type": 3, "draw_order": 1, "value": None},
]

draws = [
    {"name": "Wednesday 1", "start": "11/04/2025 09:00:00", "end": "07/05/2025 18:00:00",
     "clone_end": "06/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 1", "start": "06/05/2025 17:00:00", "end": "09/05/2025 18:00:00",
     "clone_end": "08/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 2", "start": "08/05/2025 17:00:00", "end": "14/05/2025 18:00:00",
     "clone_end": "13/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 2", "start": "13/05/2025 17:00:00", "end": "16/05/2025 18:00:00",
     "clone_end": "15/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 3", "start": "15/05/2025 17:00:00", "end": "21/05/2025 18:00:00",
     "clone_end": "20/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 3", "start": "20/05/2025 17:00:00", "end": "23/05/2025 18:00:00",
     "clone_end": "22/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 4", "start": "22/05/2025 17:00:00", "end": "28/05/2025 18:00:00",
     "clone_end": "27/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 4", "start": "27/05/2025 17:00:00", "end": "30/05/2025 18:00:00",
     "clone_end": "29/05/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 5", "start": "29/05/2025 17:00:00", "end": "04/06/2025 18:00:00",
     "clone_end": "03/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 5", "start": "03/06/2025 17:00:00", "end": "06/06/2025 18:00:00",
     "clone_end": "05/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 6", "start": "05/06/2025 17:00:00", "end": "11/06/2025 18:00:00",
     "clone_end": "10/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 6", "start": "10/06/2025 17:00:00", "end": "13/06/2025 18:00:00",
     "clone_end": "12/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 7", "start": "12/06/2025 17:00:00", "end": "18/06/2025 18:00:00",
     "clone_end": "17/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 7", "start": "17/06/2025 17:00:00", "end": "20/06/2025 18:00:00",
     "clone_end": "19/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Wednesday 8", "start": "19/06/2025 17:00:00", "end": "25/06/2025 18:00:00",
     "clone_end": "24/06/2025 18:00:00", "end_time": "12:00"},
    {"name": "Friday 8", "start": "24/06/2025 17:00:00", "end": "27/06/2025 18:00:00",
     "clone_end": "26/06/2025 18:00:00", "end_time": "12:00"},
]


def main():
    draw_schedule_entries = []
    repeat = 14
    ticket_qty = 20000
    for draw in draws:
        current_datetime = datetime.now()
        created = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # Convert start_date, end_date, and clone_end_date to datetime objects
        start_datetime = datetime.strptime(draw['start'], '%d/%m/%Y %H:%M:%S')
        end_datetime = datetime.strptime(draw['end'], '%d/%m/%Y %H:%M:%S')
        clone_end_datetime = datetime.strptime(draw['clone_end'], '%d/%m/%Y %H:%M:%S')

        # Convert datetime objects to timestamps
        start_timestamp = start_datetime.timestamp()
        end_timestamp = end_datetime.timestamp()
        clone_end_timestamp = clone_end_datetime.timestamp()

        draw_schedule_entries.append({
            "name": draw["name"],
            "subdomain": "",
            "start_date": start_datetime,
            "end_date": end_datetime,
            "ticket_limit": ticket_qty,
            "repeat_number": repeat,
            "active": 1,
            "prize_setting": 0,
            "nfp_setting": 0,
            "clone_end_date": clone_end_datetime,
            "is_continuous": 1,
            "repeat_type": "Day/s",
            "child_set": 0,
            "is_split": 1,
            "auto_draw_enabled": 1,
            "updated": created
        })

    connection = mysql.connector.connect(**db_config['prod'])
    reset_db(connection)
    # Output SQL Insert Statements
    for entry in draw_schedule_entries:
        set_query = f'''INSERT INTO draw_schedule
        (name, subdomain, start_date, end_date, ticket_limit, repeat_number, active, prize_setting,
        nfp_setting, clone_end_date, is_continuous, repeat_type, child_set, is_split, auto_draw_enabled, updated)
        VALUES ('{entry['name']}', '{entry['subdomain']}', '{entry['start_date']}', '{entry['end_date']}',
        {entry['ticket_limit']}, {entry['repeat_number']}, {entry['active']}, {entry['prize_setting']},
        {entry['nfp_setting']}, '{entry['clone_end_date']}', {entry['is_continuous']}, '{entry['repeat_type']}',
        {entry['child_set']}, {entry['is_split']}, {entry['auto_draw_enabled']}, '{entry['updated']}');'''
        print(set_query)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(set_query)
        draw_schedule_id = cursor.lastrowid

        draw_query = f'''INSERT INTO draws
        (name, subdomain, launched_date, end_date, ticket_limit, active, prize_setting,
        nfp_setting, clone_end_date, auto_draw_enabled, created, draw_schedule_id)
        VALUES ('{entry['name']}', '{entry['subdomain']}', '{entry['start_date']}', '{entry['end_date']}',
        {entry['ticket_limit']},  {entry['active']}, {entry['prize_setting']},
        {entry['nfp_setting']}, '{entry['clone_end_date']}',
        {entry['auto_draw_enabled']}, '{entry['updated']}', {draw_schedule_id});'''

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

    cursor = connection.cursor(dictionary=True)
    for draw in fortune_draws:
        draw_date = datetime.strptime(draw['draw_date'], '%d/%m/%Y %H:%M:%S')
        fortune_draw_query = f'''INSERT INTO fortune_draws
            (draw_amount, draw_date, draw_num, draw_amount_reset, fortune_group )
             VALUES ({draw['draw_amount']}, '{draw_date}', {draw['draw_num']}, 
             {draw['draw_amount_reset']}, {draw['fortune_group']});'''
        print(fortune_draw_query)
        cursor.execute(fortune_draw_query)

        connection.commit()

if __name__ == "__main__":
    main()
