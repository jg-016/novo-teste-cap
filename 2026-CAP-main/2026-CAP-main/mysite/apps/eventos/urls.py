from django.urls import path
from .views import criar_evento

app_name = 'eventos'

urlpatterns = [
    path('criar/', criar_evento, name='criar_evento'),
]
