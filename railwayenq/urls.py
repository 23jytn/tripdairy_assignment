from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('api/railway-enquiry/<train_number>/', views.result, name='result'),
    url(r'^$',views.HomePage.as_view(),name='home'),
    # path('admin/', admin.site.urls),
]
