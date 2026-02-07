from django.contrib import admin

# Register your models here.

from .models import Application,Job

admin.site.register(Application)
admin.site.register(Job)