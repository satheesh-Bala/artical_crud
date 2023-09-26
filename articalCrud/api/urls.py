from django.urls import path
import api.views as views

urlpatterns=[
    path('artical/',views.ArticalCrud.as_view()),
    path('registeruser/',views.RegisterUser.as_view()),
    path('loginuser/',views.CreateToken.as_view()),
]