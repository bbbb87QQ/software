from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.classroom_query_view, name='classroom_query'),
]