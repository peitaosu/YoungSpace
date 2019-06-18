from django.contrib import admin
from .models import User, Event, Keyword, Event_Keyword, User_Keyword, User_Event, About

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Keyword)
admin.site.register(Event_Keyword)
admin.site.register(User_Keyword)
admin.site.register(User_Event)
admin.site.register(About)
