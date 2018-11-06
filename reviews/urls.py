from django.urls import path
from . import views

urlpatterns = [
        path('register/', views.register, name='register'),
        path('login/', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('index/', views.index, name='index'),
        path('welcome/', views.welcome, name='welcome'),
        path('list_reviews/', views.list_reviews, name='list_reviews'),
        path('create_review/', views.create_review, name='create_review'),
]
