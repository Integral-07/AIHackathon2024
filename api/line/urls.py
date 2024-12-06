from django.urls import path
from . import views

urlpatterns = [

    path("", views.Line.as_view()),
    path("callback/", views.Line.handle_message)
]