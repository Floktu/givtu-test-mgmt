import requests

SERVICE_PERCTENT_FEE = 0.03
SERVICE_FLAT_FEE = 0.44
TICKET_PRICE = 1


def reset_db(cursor, app_url):
    qry = '''
            SET FOREIGN_KEY_CHECKS = 0;
                Truncate Table payment;
                Truncate Table ticket_owners;
                Truncate Table order_ticket;
                Truncate Table orders;
                Truncate Table order_group;
                Truncate Table draft_orders;
                Truncate Table vouchers_transaction;
                Truncate Table subscription;
                Truncate Table subscription_logs;
                Truncate Table subscription_has_custom;
                Truncate Table subscription_qty_adjustment;
                Truncate Table draw_winners;
                Truncate Table dreamlist;
                Truncate Table bank_accounts;
                Truncate Table user_interests;
                Truncate Table user_reset_token;
                Truncate Table user_numbers;
                Truncate Table fortune_key_audit;
                Truncate Table fortune_draws;
                Truncate Table vouchers;
                Truncate Table draw_schedule;
                Truncate Table draws;
                Truncate Table drawing_winner_conf;
                Truncate Table voucher_conf;
            '''
    cursor.execute(qry)
    create_games(app_url)


def create_games(app_url):
    requests.get(f'{app_url}/test-purchase')


def calculate_service_fee(qty):
    return (qty * SERVICE_PERCTENT_FEE) + SERVICE_FLAT_FEE
