from django.urls import path

from users.views import UserApiView, UserDetailsApiView

app_name = "users"

urlpatterns = [
    path('', UserApiView.as_view(), name='user'),
    path('<int:pk>/', UserDetailsApiView.as_view(), name='user_details'),
]
