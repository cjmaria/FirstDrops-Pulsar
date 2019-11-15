

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Cluster)
admin.site.register(Property)
admin.site.register(Namespace)
admin.site.register(Bundle)


class TopicAdmin(admin.ModelAdmin):
    list_filter = ('cluster', 'namespace__property__name')


admin.site.register(Topic, TopicAdmin)
