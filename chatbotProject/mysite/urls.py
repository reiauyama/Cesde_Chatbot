"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from nltk_app.views import chatbot_query

from nltk_app.views import MenuViewSet, SubMenuViewSet, SubSubMenuViewSet, sub3menuViewSet

router = DefaultRouter()
router.register(r'menus', MenuViewSet)
router.register(r'submenus', SubMenuViewSet)
router.register(r'subsubmenus', SubSubMenuViewSet)
router.register(r'sub3menus', sub3menuViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/chatbot/', chatbot_query, name='chatbot-query')
]
