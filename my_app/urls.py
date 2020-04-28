from django.urls import include, path
from my_app import views
#from django.conf.urls import url

urlpatterns = [
    path('',views.Home,name = 'home_page'),
]
