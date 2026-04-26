from django.urls import path
from .views import PayloadView

urlpatterns = [
    path('payload/', PayloadView.as_view()),
]