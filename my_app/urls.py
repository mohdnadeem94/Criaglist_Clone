from django.urls import include, path
from my_app import views
#from django.conf.urls import url

app_name = 'my_app'

urlpatterns = [
    path('newsearch/',views.New_Search,name = 'new_search'),
    path('analytics/',views.Analytics_Page,name = 'analytics'),
]
