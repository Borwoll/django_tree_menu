from django.test import TestCase
from tree_menu.models import Menu, MenuItem


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(name='Test Menu')
        self.item = MenuItem.objects.create(
            title='Test Item',
            menu=self.menu,
            parent=None,
            url='/test',
            named_url='',
        )

    def test_menu_item_model(self):
        self.assertEqual(self.item.title, 'Test Item')
        self.assertEqual(self.item.menu, self.menu)
        self.assertIsNone(self.item.parent)
        self.assertEqual(self.item.url, '/test')
        self.assertEqual(self.item.named_url, '')
