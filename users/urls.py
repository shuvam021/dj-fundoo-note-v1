from django.urls import path

from users.views import (list_users, get_user, save_user, update_user, delete_user)

app_name = "users"

urlpatterns = [
    path('', list_users, name='list-users'),
    path('save_user/', save_user, name='save-user'),

    path('<int:pk>/get_user/', get_user, name='get-user'),
    path('<int:pk>/update_user/', update_user, name='update-user'),
    path('<int:pk>/delete_user/', delete_user, name='delete-user'),
]
