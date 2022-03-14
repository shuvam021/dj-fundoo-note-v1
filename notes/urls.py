from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.NoteListCreateNoteApiView.as_view(), name='note-list'),
    path('<int:pk>/', views.NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-details'),
]
