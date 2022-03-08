from django.urls import path

from users.views import (delete_user, get_user, list_users, save_user,
                         update_user)

app_name = "users"

urlpatterns = [
    path('', list_users, name='list-users'),
    path('save/', save_user, name='save-user'),

    path('<int:pk>/', get_user, name='get-user'),
    path('<int:pk>/update/', update_user, name='update-user'),
    path('<int:pk>/delete/', delete_user, name='delete-user'),
]
