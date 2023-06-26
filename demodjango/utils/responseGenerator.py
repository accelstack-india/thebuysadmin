from demodjango.utils.constants import *
from decimal import Decimal


class responseGenerator:
    @classmethod
    def generateResponse(cls, data, controller_type):
        if controller_type == DASHBOARD_CONTROLLER:
            user_list = []
            for users in data:
                user_list.append(
                    {
                        "fname": users[0],
                        "lname": users[1],
                        "phone": users[2],
                        "email": users[3],
                        "city": users[4],
                        "uid": users[5],
                        "broker_linked": users[6],
                        "Subscription_Active": users[7]
                    }
                )
            return user_list

        if controller_type == DASHBOARD_STATS:
            trades_with_profit_per_lot = []
            total_PL = Decimal('0.00')
            for trades in data[5]:
                total_PL = total_PL + trades[1]
                trades_with_profit_per_lot.append(
                    {
                        "trade_name": trades[0],
                        "profit_per_lot": trades[1]
                    }
                )

            return {
                "total_user_count": data[0],
                "total_user_broker_linked": data[1],
                "total_user_subscription_active": data[2],
                "today_traded_users_count": data[3],
                "today_tradedMissed_users_count": data[4],
                "trades_with_profit_per_lot": trades_with_profit_per_lot,
                "total_PL": total_PL,
                "new_users_today": data[6],
                "new_broker_linked_today": data[7],
                "new_subscriptions_today": data[8]
            }

        if controller_type == TRADE_LIST:
            trade_list = []
            total_PL = Decimal('0.00')
            for trades in data:
                PL = (trades[2] - trades[1]) * trades[4]
                total_PL = total_PL + PL
                trade_list.append(
                    {
                        "order_name": trades[0],
                        "buy_price": trades[1],
                        "sell_price": trades[2],
                        "trade_time": trades[3],
                        "PL": PL
                    }
                )
            return {
                "trade_list": trade_list,
                "total_PL": total_PL
            }

        if controller_type == USER_DATA:
            return {
                "first_name": data[0],
                "last_name": data[1],
                "phone": data[2],
                "email": data[3],
                "city": data[4]
            }

        if controller_type == USER_NOTIFICATION:
            notification_list = []
            for notification in data:
                notification_list.append(
                    {
                        "title": notification[0],
                        "description": notification[1],
                        "type": notification[2],
                        "created": notification[3]
                    }
                )
            return notification_list
