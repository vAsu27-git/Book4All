"""book4All URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('home/', views.login,name="home"),
    path('signup/', views.signup),
    path('logout/',views.logout,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('verify/',views.verify),
    path('verifymail/',views.verifymail),
    path('seelbook/',views.sellbook,name="sellbook"),
    path('mysold/',views.mysoldbook),
    path('bookdetails/<str:id>/',views.bookalldetails),
    path('addcart/<str:id>',views.addCart),
    path('mycart/',views.myCart),
    path('profile/editprofile/',views.editprofile,name="editprofile"),
    path('home/search/',views.search)
]
