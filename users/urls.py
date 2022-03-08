from django.urls import path

from users.views import UserView

app_name = "users"

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserView.as_view()),
]
