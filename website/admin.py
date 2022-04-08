from django.contrib import admin

# Register your models here.
from .models import Users, Buddies, Interests
admin.site.register(Users)
admin.site.register(Buddies)
admin.site.register(Interests)
