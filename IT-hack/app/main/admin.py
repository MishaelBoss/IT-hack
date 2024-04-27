from django.contrib import admin
from .models import *

admin.site.register(Place)
admin.site.register(PlaceMember)
admin.site.register(Place_room)
admin.site.register(Place_roomMember)
admin.site.register(FAQMessage)