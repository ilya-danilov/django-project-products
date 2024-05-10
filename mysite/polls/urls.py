from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.main, name='homepage'),
    path('<uuid:id>/', views.detail, name='detail'),
]