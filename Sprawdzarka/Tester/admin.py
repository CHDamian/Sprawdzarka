from django.contrib import admin
from .models import Uzytkownicy, Zadania, Wysylki

# Register your models here.
admin.site.register(Uzytkownicy)
admin.site.register(Zadania)
admin.site.register(Wysylki)