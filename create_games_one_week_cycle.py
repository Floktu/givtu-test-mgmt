from datetime import datetime, timedelta
import mysql.connector
from config.config import db_config
from tests.utils import reset_db


def get_next_draw_date(draw_day, draw_time_hour):
    # Calculate the next occurrence of the given day and time
    now = datetime.now()
    draw_days = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }
    today = now.weekday()
    day_num = draw_days[draw_day]
    days_ahead = (day_num - today + 7) % 7
    next_date = now + timedelta(days=days_ahead)
    next_date = next_date.replace(hour=draw_time_hour, minute=0, second=0, microsecond=0)
    return next_date


fortune_draws_total = 53

fortune_draws = [
    {"draw_amount": 10000, "draw_date": "Tuesday", "draw_amount_reset": 5000, "fortune_group": 0, "draw_time_hour": 18},
    {"draw_amount": 20000, "draw_date": "Wednesday", "draw_amount_reset": 10000, "fortune_group": 0,
     "draw_time_hour": 18},
    {"draw_amount": 40000, "draw_date": "Thursday", "draw_amount_reset": 20000, "fortune_group": 0,
     "draw_time_hour": 18},
    {"draw_amount": 80000, "draw_date": "Friday", "draw_amount_reset": 40000, "fortune_group": 0, "draw_time_hour": 18},
]

draw_winner_conf = [
    {"quantity": 1, "label_desc": "GRAND PRIZE", "ticket_type": 1, "draw_order": 1, "value": 2500},
    {"quantity": 3, "label_desc": "$25", "ticket_type": 0, "draw_order": 1, "value": 25},
    {"quantity": 5, "label_desc": "FREE TICKET", "ticket_type": 2, "draw_order": 2, "value": None},
]

# Configuration for different draws
draws = [
    {"day": "Tuesday", "name": "Tuesday 1", "start_offset": -4, "start_time": "12:00", "clone_end_time": "11:00",
     "end_time": "12:00"},
    {"day": "Tuesday", "name": "Tuesday 2", "start_offset": 0, "start_time": "10:00", "clone_end_time": "13:00",
     "end_time": "14:00"},
    {"day": "Wednesday", "name": "Wednesday 1", "start_offset": -1, "start_time": "12:00", "clone_end_time": "11:00",
     "end_time": "12:00"},
    {"day": "Wednesday", "name": "Wednesday 2", "start_offset": 0, "start_time": "10:00", "clone_end_time": "13:00",
     "end_time": "14:00"},
    {"day": "Thursday", "name": "Thursday 1", "start_offset": -1, "start_time": "12:00", "clone_end_time": "11:00",
     "end_time": "12:00"},
    {"day": "Thursday", "name": "Thursday 2", "start_offset": 0, "start_time": "10:00", "clone_end_time": "13:00",
     "end_time": "14:00"},
    {"day": "Friday", "name": "Friday 1", "start_offset": -1, "start_time": "12:00", "clone_end_time": "11:00",
     "end_time": "12:00"},
    {"day": "Friday", "name": "Friday 2", "start_offset": 0, "start_time": "10:00", "clone_end_time": "13:00",
     "end_time": "14:00"},
]


def main():
    # Calculate the appropriate dates based on today's date
    today = datetime.now()
    day_of_week = today.weekday()  # Monday is 0, Sunday is 6

    draw_schedule_entries = []

    for draw in draws:
        target_day = (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(draw["day"])
                      - day_of_week) % 7
        draw_date = today + timedelta(days=target_day)

        start_datetime = draw_date + timedelta(days=draw["start_offset"])
        end_datetime = draw_date
        clone_end_datetime = draw_date

        # Adjust start_datetime to match the draw's start time and round down to the nearest hour
        start_datetime = start_datetime.replace(
            hour=int(draw["start_time"].split(':')[0]),
            minute=0, second=0, microsecond=0
        )

        # Adjust end_datetime to match the draw's end time and round down to the nearest hour
        end_datetime = end_datetime.replace(
            hour=int(draw["end_time"].split(':')[0]),
            minute=0, second=0, microsecond=0
        )

        # Adjust clone_end_datetime to match the draw's clone end time and round down to the nearest hour
        clone_end_datetime = clone_end_datetime.replace(
            hour=int(draw["clone_end_time"].split(':')[0]),
            minute=0, second=0, microsecond=0
        )

        current_datetime = datetime.now()
        created = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        draw_schedule_entries.append({
            "name": draw["name"],
            "subdomain": "",
            "start_date": start_datetime,
            "end_date": end_datetime,
            "ticket_limit": 70,
            "repeat_number": 7,
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
    connection = mysql.connector.connect(**db_config['staging'])
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

    # Initialize the records list

    # Update the fortune_draws list with the next occurrence datetime
    for draw in fortune_draws:
        draw_date = get_next_draw_date(draw["draw_date"], draw["draw_time_hour"])
        draw["draw_date"] = draw_date.strftime('%Y-%m-%d %H:%M:%S')
        del draw["draw_time_hour"]

    for i in range(len(fortune_draws), fortune_draws_total):
        draw_date = fortune_draws[i - 4]["draw_date"]
        draw_date = datetime.strptime(draw_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        draw_amount = fortune_draws[-1]['draw_amount'] * 2
        draw_amount_reset = draw_amount // 2
        record = {"draw_amount": draw_amount, "draw_date": draw_date.strftime('%Y-%m-%d %H:%M:%S'),
                  "draw_amount_reset": draw_amount_reset, "fortune_group": 0}
        fortune_draws.append(record)

    cursor = connection.cursor(dictionary=True)
    for idx, draw in enumerate(fortune_draws):
        fortune_draw_query = f'''INSERT INTO fortune_draws
            (draw_amount, draw_date, draw_num, draw_amount_reset, fortune_group )
             VALUES ({draw['draw_amount']}, '{draw['draw_date']}', {idx + 1}, 
             {draw['draw_amount_reset']}, {draw['fortune_group']});'''
        print(fortune_draw_query)
        cursor.execute(fortune_draw_query)
    connection.commit()


if __name__ == "__main__":
    main()
