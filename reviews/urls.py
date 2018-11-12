from django.urls import path
from . import views

urlpatterns = [
        path('companies/', views.CompanyListCreate.as_view()),
        path('users/', views.UserListCreate.as_view()),
        path('reviews/', views.ReviewListCreate.as_view()),
        path('login/', views.login, name='login'),
]
