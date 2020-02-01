from django.contrib import admin
from .models import Diary,User,WordDict

admin.site.register(User)
admin.site.register(Diary)
admin.site.register(WordDict)
