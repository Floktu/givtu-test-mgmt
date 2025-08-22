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


def get_current_or_previous_draw_date(draw_day, draw_time_hour):
    # Calculate the most recent occurrence of the given day and time
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

    # If the draw day is before or equal to today, find the previous occurrence
    if day_num <= today:
        days_behind = today - day_num
        target_date = now - timedelta(days=days_behind)
    else:  # Otherwise, calculate it for the upcoming occurrence
        days_ahead = day_num - today
        target_date = now + timedelta(days=days_ahead)

    # Set the hour, minute, second, and microsecond for the target date
    target_date = target_date.replace(hour=draw_time_hour, minute=0, second=0, microsecond=0)
    return target_date


fortune_draws_total = 53

fortune_draws = [
    {"draw_amount": 200000, "draw_date": "Tuesday", "draw_amount_reset": 100000, "fortune_group": 0,
     "draw_time_hour": 18},
    {"draw_amount": 210000, "draw_date": "Wednesday", "draw_amount_reset": 110000, "fortune_group": 0,
     "draw_time_hour": 18},
    {"draw_amount": 220000, "draw_date": "Thursday", "draw_amount_reset": 120000, "fortune_group": 0,
     "draw_time_hour": 18},
    {"draw_amount": 230000, "draw_date": "Friday", "draw_amount_reset": 130000, "fortune_group": 0,
     "draw_time_hour": 18},
]

draw_winner_conf = [
    {"quantity": 1, "label_desc": "GRAND PRIZE", "ticket_type": 1, "draw_order": 1, "value": 2500},
    {"quantity": 4, "label_desc": "$25", "ticket_type": 0, "draw_order": 1, "value": 25},
    {"quantity": 75, "label_desc": "FREE TICKET", "ticket_type": 2, "draw_order": 2, "value": None},
    {"quantity": 250, "label_desc": "FORTUNE KEYS", "ticket_type": 3, "draw_order": 1, "value": None},
]

# Configuration for different draws
draws = [
    {"day": "Friday", "name": "Friday 1", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 1", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 2", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 2", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 3", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 3", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 4", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 4", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 1", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 1", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 2", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 2", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 3", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 3", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Friday", "name": "Friday 4", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
    {"day": "Wednesday", "name": "Wednesday 4", "start_offset": 0, "start_time": "13:00", "clone_end_time": "13:30",
     "end_time": "18:00"},
]


def get_most_recent_draw_start():
    """Find the most recent Wednesday or Friday at 13:00"""
    now = datetime.now()
    weekday = now.weekday()  # Monday=0, ..., Sunday=6

    # 2 = Wednesday, 4 = Friday
    days = {
        2: "Wednesday",
        4: "Friday"
    }

    candidates = []
    for day_num, day_name in days.items():
        diff = (weekday - day_num + 7) % 7
        draw_day = now - timedelta(days=diff)
        draw_day = draw_day.replace(hour=13, minute=0, second=0, microsecond=0)
        candidates.append((draw_day, day_name))

    # Return the most recent one
    return max(c for c in candidates if c[0] <= now)


def generate_draw_schedule_entries(count=16):
    entries = []
    current_start, current_day_name = get_most_recent_draw_start()
    created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    wednesday_count = 0
    friday_count = 0

    for i in range(count):
        if current_day_name == "Wednesday":
            wednesday_count %= 4
            wednesday_count += 1
            name = f"Friday {wednesday_count}"
            end_date = current_start + timedelta(days=2)  # Friday
            next_day_name = "Friday"
        else:  # Friday
            friday_count %= 4
            friday_count += 1
            name = f"Wednesday {friday_count}"
            end_date = current_start + timedelta(days=5)  # Next Wednesday
            next_day_name = "Wednesday"

        clone_end_date = end_date.replace(hour=13, minute=30, second=0, microsecond=0)
        end_date = end_date.replace(hour=18, minute=0, second=0, microsecond=0)

        entries.append({
            "name": name,
            "subdomain": "",
            "start_date": current_start,
            "end_date": end_date,
            "ticket_limit": 1000,
            "repeat_number": 14,
            "active": 1,
            "prize_setting": 0,
            "nfp_setting": 0,
            "clone_end_date": clone_end_date,
            "is_continuous": 1,
            "repeat_type": "Day/s",
            "child_set": 0,
            "is_split": 1,
            "auto_draw_enabled": 1,
            "updated": created
        })

        # Move to next draw: 2 days after Wednesday, or 5 days after Friday
        days_to_add = 2 if current_day_name == "Wednesday" else 5
        current_start = current_start + timedelta(days=days_to_add)
        current_day_name = next_day_name

    return entries


def main():
    # Calculate the appropriate dates based on today's date
    today = datetime.now()
    day_of_week = today.weekday()  # Monday is 0, Sunday is 6

    draw_schedule_entries = []
    draw_schedule_entries = generate_draw_schedule_entries(16)

    # for i, draw in enumerate(draws):
    #     target_day = (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(draw["day"])
    #                   - day_of_week) % 7
    #     draw_date = today + timedelta(days=target_day)
    #     if i >= 2:
    #         draw_date += timedelta(days=7)
    #
    #     start_datetime = draw_date + timedelta(days=draw["start_offset"])
    #
    #     # Determine end date based on start date's weekday
    #     if start_datetime.weekday() == 2:  # Wednesday (index 2)
    #         end_datetime = start_datetime + timedelta(days=2)  # Friday
    #     elif start_datetime.weekday() == 4:  # Friday (index 4)
    #         end_datetime = start_datetime + timedelta(days=5)  # Next Wednesday
    #     else:
    #         end_datetime = draw_date  # Default (shouldn't happen)
    #
    #     clone_end_datetime = end_datetime
    #
    #     # Adjust start_datetime to match the draw's start time and round down to the nearest hour
    #     start_datetime = start_datetime.replace(
    #         hour=int(draw["start_time"].split(':')[0]),
    #         minute=0, second=0, microsecond=0
    #     )
    #
    #     # Adjust end_datetime to match the draw's end time and round down to the nearest hour
    #     end_datetime = end_datetime.replace(
    #         hour=int(draw["end_time"].split(':')[0]),
    #         minute=0, second=0, microsecond=0
    #     )
    #
    #     # # Adjust clone_end_datetime to match the draw's clone end time and round down to the nearest hour
    #     # clone_end_datetime = clone_end_datetime.replace(
    #     #     hour=int(draw["clone_end_time"].split(':')[0]),
    #     #     minute=0, second=0, microsecond=0
    #     # )
    #
    #     clone_hour, clone_minute = map(int, draw["clone_end_time"].split(':'))
    #     clone_end_datetime = end_datetime.replace(hour=clone_hour, minute=clone_minute, second=0, microsecond=0)
    #
    #     current_datetime = datetime.now()
    #     created = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    #
    #     draw_schedule_entries.append({
    #         "name": draw["name"],
    #         "subdomain": "",
    #         "start_date": start_datetime,
    #         "end_date": end_datetime,
    #         "ticket_limit": 1000,
    #         "repeat_number": 14,
    #         "active": 1,
    #         "prize_setting": 0,
    #         "nfp_setting": 0,
    #         "clone_end_date": clone_end_datetime,
    #         "is_continuous": 1,
    #         "repeat_type": "Day/s",
    #         "child_set": 0,
    #         "is_split": 1,
    #         "auto_draw_enabled": 1,
    #         "updated": created
    #     })
    connection = mysql.connector.connect(**db_config['dev'])
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
    for draw in fortune_draws:
        draw_date = get_current_or_previous_draw_date(draw["draw_date"], draw["draw_time_hour"])
        draw["draw_date"] = draw_date.strftime('%Y-%m-%d %H:%M:%S')
        del draw["draw_time_hour"]
    # Add additional fortune draws dynamically up to the total count
    for i in range(len(fortune_draws), fortune_draws_total):
        last_draw_date = datetime.strptime(fortune_draws[i - 4]["draw_date"], '%Y-%m-%d %H:%M:%S') + timedelta(days=7)
        # draw_amount = fortune_draws[-1]['draw_amount'] * 2
        # draw_amount_reset = draw_amount // 2
        draw_amount = fortune_draws[-1]['draw_amount'] + 10000
        draw_amount_reset = fortune_draws[-1]['draw_amount_reset'] + 10000
        record = {
            "draw_amount": draw_amount,
            "draw_date": last_draw_date.strftime('%Y-%m-%d %H:%M:%S'),
            "draw_amount_reset": draw_amount_reset,
            "fortune_group": 0
        }
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
