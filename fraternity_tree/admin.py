from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from fraternity_tree.models import PledgeClass, Brother, Chapter

admin.site.register(PledgeClass)
admin.site.register(Brother, MPTTModelAdmin)
admin.site.register(Chapter)
