from django.contrib import admin
from .models import Profile,Projects,Comments,Ratings
# Register your models here.
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Ratings)
admin.site.register(Projects)