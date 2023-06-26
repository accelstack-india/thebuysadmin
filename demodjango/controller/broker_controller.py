from django.db import connection
import pyotp
from demodjango.utils.kite_trade import KiteApp, get_enctoken


def getRefreshTotp(totp_token):
    totp = pyotp.TOTP(totp_token)
    return totp.now()

def checkBrokerLogin(result):
    try:

        KiteApp(enctoken=get_enctoken(result[3], result[4], getRefreshTotp(result[5])))
        return True
    except Exception as e:
        print("Error:", e)
        return False

def get_statistics(broker_details):
    try:
        kite = KiteApp(enctoken=get_enctoken(broker_details[3], broker_details[4], getRefreshTotp(broker_details[5])))
        data = kite.margins()
        margin_data = data['equity']
        available_cash = margin_data['net']
        utilized_margin = margin_data['utilised']['debits']
        return available_cash, utilized_margin
    except Exception as e:
        print("Error:", e)

def get_broker_balance(uid):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM user_broker_details WHERE uid = %s AND status = %s', (uid, 1))
        brokerObj = cursor.fetchone()
        if brokerObj is None:
            print("no broker account")
            return {
                "isBrokerLinked": 0,
                "Balance": 0
            }
        else:
            if checkBrokerLogin(brokerObj):
                statistics = get_statistics(brokerObj)
                return {
                    "isBrokerLinked": 1,
                    "available_broker_balance": statistics[0]
                }
            else:
                return {
                    "isBrokerLinked": 2,
                    "available_broker_balance": 0
                }