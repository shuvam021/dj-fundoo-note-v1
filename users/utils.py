from typing import Any

from django.http import JsonResponse


def return_response(status: Any = 200, data=None, msg: Any = None):
    message_switcher = {
        "200": "Data fetch successful",
        "201": "Create or Update successful",
        "204": "Delete successful",
        "404": "User doesn't exist",
        "_": msg
    }
    return JsonResponse({'status': status, 'message': message_switcher.get(str(status)), 'data': data}, status=status)


def return_data(obj: object):
    return {
        "id": obj.id,
        "username": obj.username,
        "first_name": obj.first_name,
        "last_name": obj.last_name,
        "email": obj.email,
    }
