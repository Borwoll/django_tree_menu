from django.test import TestCase
from tree_menu.models import Menu, MenuItem
from tree_menu.templatetags.draw_menu import get_menu_items


class TreeMenuTagsTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name='Test Menu')
        self.item1 = MenuItem.objects.create(
            title='Test Item 1',
            menu=self.menu,
            parent=None,
            url='/test1',
            named_url='',
        )
        self.item2 = MenuItem.objects.create(
            title='Test Item 2',
            menu=self.menu,
            parent=None,
            url='/test2',
            named_url='',
        )

    def test_get_menu_items(self):
        items = get_menu_items('Test Menu')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['title'], 'Test Item 1')
        self.assertEqual(items[0]['parent'], None)
        self.assertEqual(items[0]['url'], '/test1')
        self.assertEqual(items[1]['title'], 'Test Item 2')
        self.assertEqual(items[1]['parent'], None)
        self.assertEqual(items[1]['url'], '/test2')
