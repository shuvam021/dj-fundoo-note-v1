import json

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from users.utils import fetch_user, logger, return_data, return_response


# Create your views here.
def list_users(request):
    obj_list = User.objects.all()
    if obj_list.count() == 0:
        return return_response(status=404)
    return return_response(status=200, data=[return_data(obj) for obj in obj_list])


@csrf_exempt
def save_user(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            password = data.pop('password')
            obj = User(**data)
            obj.set_password(password)
            obj.save()
            return return_response(status=201, data=return_data(obj))
        return return_response(status="_", msg="Something went wrong")
    except Exception as e:
        logger.warning("user create()")
        print(e)


def get_user(request, pk):
    try:
        obj = fetch_user(pk)
        return return_response(status=200, data=return_data(obj))
    except Exception as e:
        print(e)


@csrf_exempt
def update_user(request, pk):
    try:
        obj = fetch_user(pk)
        if request.method == "PUT":
            data = json.loads(request.body)
            obj.username = data.get("username")
            obj.first_name = data.get("first_name")
            obj.last_name = data.get("last_name")
            obj.email = data.get("email")
            obj.save()
        return return_response(status=201, data=return_data(obj))
    except Exception as e:
        logger.warning("user Update()")
        print(e)


@csrf_exempt
def delete_user(request, pk):
    try:
        obj = fetch_user(pk)
        if request.method == "DELETE":
            obj.delete()
            return return_response(status=204)
    except Exception as e:
        logger.warning("user Update()")
        print(e)
