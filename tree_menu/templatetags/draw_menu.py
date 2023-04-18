from django import template
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from tree_menu.models import MenuItem, Menu

register = template.Library()


def get_menu_items(menu_name):
    """
    Получение пунктов меню по имени меню.
    Возвращает список словарей с информацией о пунктах меню.
    """
    # Проверяем, есть ли результат в кэше
    cache_key = f"menu_items_{menu_name}"
    menu_items = cache.get(cache_key)
    if menu_items is not None:
        return menu_items

    # Получаем меню по имени
    menu = get_object_or_404(Menu, name=menu_name)

    # Получаем пункты меню
    menu_items = MenuItem.objects.filter(menu=menu)

    # Формируем список словарей с информацией о пунктах меню
    menu_items_list = []
    for item in menu_items:
        menu_items_list.append({
            "title": item.title,
            "parent": item.parent,
            "url": item.get_absolute_url(),
            "children": get_children(item)
        })

    # Кэшируем результат на 5 минут
    cache.set(cache_key, menu_items_list, 300)

    return menu_items_list


def get_children(item):
    """
    Рекурсивно получает дочерние пункты меню.
    Возвращает список словарей с информацией о дочерних пунктах меню.
    """
    children = []
    if item.children.exists():
        for child in item.children.all():
            children.append({
                "title": child.title,
                "url": child.get_absolute_url(),
                "children": get_children(child)
            })
    return children


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    # Получаем текущий URL
    current_url = context['request'].path

    # Получаем пункты меню по имени меню
    menu_items = get_menu_items(menu_name)

    # Определяем активный пункт меню и его дочерние пункты
    active_item = None
    active_item_children = []
    for item in menu_items:
        if current_url.startswith(item["url"]):
            active_item = item
            if item["children"]:
                active_item_children = item["children"]
            break

    # Отрисовываем меню
    menu_html = '<ul>'
    for item in menu_items:
        if item.get('parent'):
            # Элементы, имеющие родительские элементы, отображаются только внутри своих родительских элементов
            continue
        menu_html += '<li class="{}">'.format('active' if item == active_item else '')
        menu_html += '<a href="{}">{}</a>'.format(item["url"], item["title"])
        menu_html += draw_children(item["children"], active_item_children)
        menu_html += '</li>'
    menu_html += '</ul>'

    return menu_html


# Функция для рекурсивного отображения дочерних элементов
def draw_children(items, active_children):
    if not items:
        return ""
    children_html = "<ul>"
    for item in items:
        children_html += '<li class="{}">'.format('active' if item in active_children else '')
        children_html += '<a href="{}">{}</a>'.format(item["url"], item["title"])
        children_html += draw_children(item["children"], active_children)
        children_html += '</li>'
    children_html += "</ul>"
    return children_html
