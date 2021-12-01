from django.contrib import admin
from .models import Author, Typ, Bike, BikeInstance, Sex

admin.site.register(Typ)
admin.site.register(Sex)


class BikesInline(admin.TabularInline):
    model = Bike


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name',
                    'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BikesInline]


class BikesInstanceInline(admin.TabularInline):
    model = BikeInstance


class BikeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_typ', 'photo')
    inlines = [BikesInstanceInline]


admin.site.register(Bike, BikeAdmin)


@admin.register(BikeInstance)
class BikeInstanceAdmin(admin.ModelAdmin):
    list_display = ('bike', 'status', 'borrower', 'due_back', 'id',)
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('bike', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
