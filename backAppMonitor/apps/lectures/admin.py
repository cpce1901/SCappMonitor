from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from .models import Measures
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin


class MeasureResource(ModelResource):
    class Meta:
        model = Measures
        use_bulk = True
        batch_size = 500


# Register your models here.
class MeasureAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_class = MeasureResource
    list_display = (
        "created",
        "sensor",
        "located",
        "v1",
        "v2",
        "v3",
        "v13",
        "v23",
        "v12",
        "i1",
        "i2",
        "i3",
        "p1",
        "p2",
        "p3",
        "pa",
        "fp",
        "hz",
    )

    readonly_fields = ("created",)

    ordering = ("-created",)

    list_filter = (
        ("created", DateFieldListFilter),
        "sensor__id",
        "sensor__located_sensor",
    )

    def located(self, obj):
        return obj.sensor.located_sensor

    located.short_description = "ubicación"


admin.site.register(Measures, MeasureAdmin)
