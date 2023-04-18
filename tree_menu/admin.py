from django.contrib import admin
from tree_menu.models import MenuItem, Menu


class MenuItemInline(admin.TabularInline):
    model = MenuItem


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem)
