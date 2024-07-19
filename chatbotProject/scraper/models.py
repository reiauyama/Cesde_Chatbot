from django.db import models

class Menu(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SubMenu(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='submenus')
    title = models.CharField(max_length=250)
    link = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SubSubMenu(models.Model):
    submenu = models.ForeignKey(SubMenu, on_delete=models.CASCADE, related_name='subsubmenus')
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True, null=True)
    content = models.TextField( blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class sub3menu(models.Model):
    subsubmenu = models.ForeignKey(SubSubMenu, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField()
    active = models.BooleanField(default=True)

from rest_framework import serializers
from .models import Menu, SubMenu, SubSubMenu, sub3menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = '__all__'

class SubSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubMenu
        fields = '__all__'

class sub3menuSerializer(serializers.ModelSerializer):
    class Meta:
        model = sub3menu
        fields = '__all__'
