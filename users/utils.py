import datetime
import logging
from typing import Any

from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse

logging.basicConfig(filename=settings.LOG_FILE,
                    encoding='utf-8', level=logging.warning)

logger = logging.getLogger(__name__)


def return_response(status: Any = 200, data=None, msg: Any = None):
    message_switcher = {
        "200": "Data fetch successful",
        "201": "Create or Update successful",
        "204": "Delete successful",
        "404": "User doesn't exist",
        "_": msg
    }
    return JsonResponse({'status': status, 'message': message_switcher.get(str(status)), 'data': data}, status=status)


def fetch_user(pk):
    try:
        obj = User.objects.get(id=pk)
    except User.DoesNotExist as e:
        raise e
    except Exception as e:
        logger.warning('User() was accessed at ' +
                       str(datetime.datetime.now()) + ' hours!')
        raise e


def return_data(obj: object):
    return {
        "id": obj.id,
        "username": obj.username,
        "first_name": obj.first_name,
        "last_name": obj.last_name,
        "email": obj.email,
    }
