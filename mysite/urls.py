"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp.views import user_login, user_logout, home, data_awal,diskritisasi, proses_bagi_data, pembagian_data,klasifikasi, uji_data, tampilkan_form_uji_data, register


urlpatterns = [
       path('', home, name='home'),
       path('login/', user_login, name='login'),
       path('register/', register, name='register'),
         path('logout/', user_logout, name='logout'),
         path('data_awal/', data_awal, name='data_awal'),
         path('diskritisasi/', diskritisasi, name='diskritisasi'),
         path('proses_bagi_data/', proses_bagi_data, name='proses_bagi_data'),
         path('pembagian_data/', pembagian_data, name='pembagian_data'),
         path('klasifikasi/', klasifikasi, name='klasifikasi'),
         path('uji_data/', uji_data, name='uji_data'),
         path('tampilkan_form_uji_data/', tampilkan_form_uji_data, name='tampilkan_form_uji_data'),
 
        
]


