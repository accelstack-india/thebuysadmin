from django.db import connection

from demodjango.utils.constants import *
from demodjango.utils.responseGenerator import responseGenerator


def all_users_with_broker_Subscription_status():
    with connection.cursor() as cursor:
        cursor.execute("""
                   SELECT users.first_name, users.last_name, users.phone, users.email,
                          users.city, users.uid,
                          CASE WHEN user_broker_details.uid IS NOT NULL THEN true ELSE false END as broker_status,
                          CASE WHEN subscriptions.user_id IS NOT NULL AND subscriptions.end_date >= %s THEN true ELSE 
                          false END as active_subscription_status FROM users
                           LEFT JOIN user_broker_details ON users.uid = user_broker_details.uid
                           LEFT JOIN subscriptions ON users.uid = subscriptions.user_id
                           """, [today.date()])
        usersObject = cursor.fetchall()
        return responseGenerator.generateResponse(usersObject, DASHBOARD_CONTROLLER)


def dashbord_stats():
    with connection.cursor() as cursor:
        cursor.execute(""" select count(*) from users""")
        total_users_count = cursor.fetchone()

        cursor.execute(""" SELECT count(*) FROM user_broker_details WHERE uid IN (SELECT uid FROM user_broker_details 
        GROUP BY uid HAVING COUNT(uid) = 1)""")
        total_user_broker_linked = cursor.fetchone()

        cursor.execute(""" SELECT count(*) FROM subscriptions WHERE end_date >= %s AND user_id IN (SELECT user_id FROM subscriptions 
                GROUP BY user_id HAVING COUNT(user_id) = 1)""", [today.date()])
        total_user_subscription_active = cursor.fetchone()

        cursor.execute("""SELECT COUNT(DISTINCT users.uid) AS present_count,
               (SELECT COUNT(uid) FROM users WHERE uid NOT IN (SELECT user_id FROM trading_history WHERE DATE(start_time) = %s)) AS not_present_count
        FROM users
        INNER JOIN trading_history ON users.uid = trading_history.user_id
        WHERE DATE(trading_history.start_time) = %s""", [today.date(), today.date()])
        result = cursor.fetchone()
        today_traded_users_count, today_tradedMissed_users_count = result

        query = """
            SELECT order_name, 
                (CASE
                    WHEN order_name LIKE 'BANK%%' THEN (sell_price - buy_price) * 25

                    ELSE (sell_price - buy_price) * 50
                END) AS expression_result
            FROM trading_history
            WHERE DATE(start_time) = %s AND sell_price IS NOT NULL AND sell_price != ''
            GROUP BY order_id
        """
        cursor.execute(query, [today.date()])
        trades_with_profit_per_lot = cursor.fetchall()

        cursor.execute(""" SELECT count(*) FROM users where DATE(created_on) = %s""", [today.date()])
        new_users_today = cursor.fetchone()

        cursor.execute(""" SELECT count(*) FROM user_broker_details where DATE(created_on) = %s""", [today.date()])
        new_broker_linked_today = cursor.fetchone()

        cursor.execute(""" SELECT count(*) FROM subscriptions where DATE(start_date) = %s""", [today.date()])
        new_subscriptions_today = cursor.fetchone()
        dashboardObject = total_users_count[0], total_user_broker_linked[0], total_user_subscription_active[0], \
            today_traded_users_count, today_tradedMissed_users_count, trades_with_profit_per_lot, new_users_today[0],\
            new_broker_linked_today[0], new_subscriptions_today[0]

        return responseGenerator.generateResponse(dashboardObject, DASHBOARD_STATS)


def get_user_trades(uid):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT order_name, buy_price, sell_price, start_time, quantity
                FROM trading_history
                WHERE user_id = %s AND sell_price IS NOT NULL AND sell_price != '' 
                ORDER BY start_time DESC
            """, [uid])
        trades = cursor.fetchall()
        return responseGenerator.generateResponse(trades, TRADE_LIST)
