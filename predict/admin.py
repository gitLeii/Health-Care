from django.contrib import admin

from .models import Disease, Symptom
# Register your models here.

admin.site.register(Symptom)
admin.site.register(Disease)