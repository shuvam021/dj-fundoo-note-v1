import json
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from users.utils import return_data, return_response

logging.basicConfig(filename=settings.LOG_FILE,
                    encoding='utf-8', level=logging.warning)

logger = logging.getLogger(__name__)


# Create your views here.
class UserView(View):
    model = User

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logger.warning("user get()")
        pk = kwargs.get('pk')
        qs = self.model.objects.all()
        try:
            if pk:
                qs = get_object_or_404(self.model, pk=pk)
                return return_response(data=return_data(qs))
            return return_response(data=[return_data(obj) for obj in qs])
        except Exception as e:
            print(e)

    def post(self, request, *args, **kwargs):
        logger.warning("user post()")
        try:
            data = json.loads(request.body)
            password = data.pop('password')
            obj = User(**data)
            obj.set_password(password)
            obj.save()
            return return_response(status=201, data=return_data(obj))
        except Exception as e:
            return return_response(status="_", msg=str(e))

    def put(self, request, *args, **kwargs):
        logger.warning("user put()")
        pk = kwargs.get("pk")
        try:
            obj = get_object_or_404(self.model, pk=pk)
            data = json.loads(request.body)
            obj.username = data.get("username")
            obj.first_name = data.get("first_name")
            obj.last_name = data.get("last_name")
            obj.email = data.get("email")
            obj.save()
            return return_response(status=201, data=return_data(obj))
        except Exception as e:
            print(e)

    def delete(self, request, *args, **kwargs):
        logger.warning("user delete()")
        pk = kwargs.get("pk")
        try:
            obj = get_object_or_404(self.model, pk=pk)
            obj.delete()
            return return_response(status=204)
        except Exception as e:
            print(e)
