from django import template
from django.shortcuts import get_object_or_404
from tree_menu.models import MenuItem, Menu

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    # получаем текущий URL
    current_url = context['request'].path

    # получаем меню по его названию
    menu = get_object_or_404(Menu, name=menu_name)

    # получаем все пункты меню
    menu_items = MenuItem.objects.filter(menu=menu)

    # определяем активный пункт меню и его дочерние пункты
    active_item = None
    active_item_children = []
    for item in menu_items:
        if current_url.startswith(item.get_absolute_url()):
            active_item = item
            if item.children.exists():
                active_item_children = item.children.all()
            break

    # отрисовываем меню
    menu_html = '<ul>'
    for item in menu_items:
        menu_html += '<li class="{}">'.format('active' if item == active_item else '')
        menu_html += '<a href="{}">{}</a>'.format(item.get_absolute_url(), item.title)
        if item.children.exists():
            menu_html += '<ul>'
            for child in item.children.all():
                menu_html += '<li class="{}">'.format('active' if child in active_item_children else '')
                menu_html += '<a href="{}">{}</a>'.format(child.get_absolute_url(), child.title)
                menu_html += '</li>'
            menu_html += '</ul>'
        menu_html += '</li>'
    menu_html += '</ul>'

    return menu_html
