from django.contrib import admin
from .models import Client,Server,Category
# Register your models here.

admin.site.register(Client)
admin.site.register(Server)
admin.site.register(Category)
