from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_account/', views.new_account, name='new_account'),
    path('add_account/', views.add_account, name='add_account'),
    path('login/', views.login, name='login'),
    path('my_page/', views.my_page, name='my_page'),
    path('logout/', views.logout, name='logout'),
    path('tasks/', views.tasks, name='tasks'),
    path('send/', views.send, name='send'),
    path('make_tests/', views.make_tests, name='make_tests'),
    path('solutions/', views.solutions, name='solutions'),
    path('read_raport/<int:id>/', views.read_raport, name='read_raport')
]