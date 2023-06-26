from django.db import connection
import requests

from demodjango.utils.responseGenerator import responseGenerator
from demodjango.utils.constants import *


def getUserInfo():
    return "helllo sandy"


def login(username, password):
    with connection.cursor() as cursor:
        query = "SELECT * FROM admin_users WHERE username = %s;"
        cursor.execute(query, [username])
        result = cursor.fetchone()
        if result is not None and result[2] == password:
            return {
                "msg": "Success",
                "data": result
            }

        if result is not None and result[2] != password:
            return {
                "msg": "wrong password",
            }

        else:
            return {
                "msg": "user not exist, Please register",
            }



def register(regObject):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (fname, lname,email,phone,age,password) VALUES (%s, %s,%s,%s,%s,%s)",
                       [regObject.fname, regObject.lname, regObject.email, regObject.phone, regObject.age,
                        regObject.password])

    return "success"


def send_push_notification(uid, title, body):
    with connection.cursor() as cursor:
        server_key = 'AAAAdeVOsPQ:APA91bGnlZkmT_wsTHYc3Q4zv-h6hnOrzbORDVDKYh-3zby3rbXgfjgSAyrrMTLER5lQftvPu3Ph2REmB5HFPFnMqVvWEn6_kxZenJGfmWyx48rZ21NZq9RP2epRFJ5F4x2WrprjYA7D'
        query = "SELECT fcm_token FROM users WHERE uid = %s;"
        cursor.execute(query, [uid])
        device_token = cursor.fetchone()
        if device_token is not None:
            data = {
                'to': device_token[0],
                'notification': {
                    'title': title,
                    'body': body
                },

            }

            # Send the request to FCM API
            headers = {
                'Authorization': 'key=' + server_key,
                'Content-Type': 'application/json'
            }
            response = requests.post('https://fcm.googleapis.com/fcm/send', json=data, headers=headers)

            # Return the response from FCM API
            return (response.json()), response.status_code


def getUserdata(uid):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT first_name, last_name, phone, email, city
                    FROM users
                    WHERE uid = %s
                """, [uid])
        user_data = cursor.fetchone()
        return responseGenerator.generateResponse(user_data, USER_DATA)


def get_user_notifications(uid):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT title, description, type, created
                    FROM notification
                    WHERE uid = %s ORDER BY created DESC
                """, [uid])
        noti_data = cursor.fetchall()
        return responseGenerator.generateResponse(noti_data, USER_NOTIFICATION)