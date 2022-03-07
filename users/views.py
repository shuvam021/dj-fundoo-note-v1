import datetime
import logging
from typing import Any

from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logging.basicConfig(filename=settings.LOG_FILE, encoding='utf-8', level=logging.DEBUG)

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
        obj = User.objects.filter(id=pk)
    except Exception as e:
        logger.warning('User() was accessed at ' + str(datetime.datetime.now()) + ' hours!')
        return return_response(status="_", msg=e)
    if obj.exists():
        return obj.first()
    return None


def return_data(obj: object):
    return {
        "id": obj.id,
        "username": obj.username,
        "first_name": obj.first_name,
        "last_name": obj.last_name
    }


# Create your views here.
def list_users(request):
    obj_list = User.objects.all()
    print(obj_list.count())
    if obj_list.count() == 0:
        return return_response(status=404)
    return return_response(status=200, data=[return_data(o) for o in obj_list])


@csrf_exempt
def save_user(request):
    if request.method == "POST":
        obj = User(
            username=request.POST.get("username"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
        )
        obj.set_password(request.POST.get("password"))
        obj.save()
        return return_response(status=201, data=return_data(obj))


def get_user(request, pk):
    logger.info("User get_user() accessed")
    obj = fetch_user(pk)
    if not obj:
        return return_response(status=404)
    return return_response(status=200, data=return_data(obj))


@csrf_exempt
def update_user(request, pk):
    logger.info("User Update accessed")
    obj = fetch_user(pk)
    if not obj:
        return return_response(status=404)
    if request.method == "POST":
        obj.username = request.POST.get("username")
        obj.first_name = request.POST.get("first_name")
        obj.last_name = request.POST.get("last_name")
        obj.save()
    return return_response(status=201, data=return_data(obj))


@csrf_exempt
def delete_user(request, pk):
    obj = fetch_user(pk)
    if not obj:
        return return_response(status=404)
    obj.delete()
    return return_response(status=204)
