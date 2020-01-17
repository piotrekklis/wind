from django.contrib import admin

from .models import Observation, APItoken, ElementsReturned, Localization

admin.site.register(Observation)
admin.site.register(APItoken)
admin.site.register(ElementsReturned)
admin.site.register(Localization)
