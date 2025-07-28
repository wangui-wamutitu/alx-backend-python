from django.contrib import admin
from .models import Message, User, Notification


admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(User)