from django.contrib import admin

# Register your models here.
from .models import Country, Region, City, Org, Series, Sport, Medal, Profile, Medal_To_Moderate

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Org)
admin.site.register(Series)
admin.site.register(Sport)
admin.site.register(Medal)
admin.site.register(Profile)
admin.site.register(Medal_To_Moderate)
