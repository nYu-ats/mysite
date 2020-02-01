from django.urls import path
from . import views

urlpatterns=[
path('', views.login_user, name='index1'),
path('register/',views.register_user,name='register'),
path('diary/',views.write_diary,name='diary'),
path('diary/choice/',views.choice_date,name='choice'),
path('diary/logout/',views.logout,name='logout'),
path('diary/choice/logout/',views.logout,name='logout'),
path('change/',views.change_password,name='change')
]
