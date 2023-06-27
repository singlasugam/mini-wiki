from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.title, name="title"),
    path('search', views.search, name="search"), 
    path('newentry', views.newentry, name="newentry"),
    path('check', views.check, name='check'),
    path('random',views.random_view,name='random'),
    path('edit/<str:title>', views.edit, name='edit'),
    path('update/<str:heading>', views.update, name='update')
]
