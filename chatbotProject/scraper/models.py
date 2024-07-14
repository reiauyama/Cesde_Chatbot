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
    escuela = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('subsubmenu', 'escuela')
