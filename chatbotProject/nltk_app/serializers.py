from rest_framework import serializers
from scraper.models import Menu, SubMenu, SubSubMenu, sub3menu

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
