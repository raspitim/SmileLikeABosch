from django.contrib import admin
from main.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        import_id_fields = ['order_no']


class OrderAdmin(ImportExportModelAdmin):
    resource_classes = [OrderResource]


class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "value")

admin.site.register(Property, PropertyAdmin)
admin.site.register(Component)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
