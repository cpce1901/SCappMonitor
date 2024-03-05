from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter, SimpleListFilter
from django.utils.translation import gettext_lazy as _
from .models import Measures
from import_export.resources import ModelResource
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin

class InputFilter(SimpleListFilter):
    template = 'filters/more_than.html'

    def lookups(self, request, model_admin):
        return ((),)
    
    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class MoreThan(InputFilter):
    parameter_name = 'pa'
    title = _('Mayor que')

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None and value.strip():  # Verifica si el valor no está vacío
            try:
                pa = float(value)
                return queryset.filter(pa__gte=pa)
            except ValueError:
                pass  # Handle the case where the value is not a valid float

        return queryset


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
        MoreThan
    )

    list_per_page = 20 

    def located(self, obj):
        return obj.sensor.located_sensor

    located.short_description = "ubicación"


admin.site.register(Measures, MeasureAdmin)
