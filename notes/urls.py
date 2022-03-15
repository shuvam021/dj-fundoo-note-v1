from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.NoteListCreateNoteApiView.as_view(), name='note-list'),
    path('<int:pk>/', views.NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-details'),
    path('labels/', views.LabelViewSet.as_view({'get': 'list', 'post': 'create'}), name='label-list'),
    path('labels/<int:pk>/', views.LabelDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='label-detail'),
]
