from django.contrib import admin
from apps.users.models import User, Role

admin.site.register(User)
admin.site.register(Role)

# Register your models here.
