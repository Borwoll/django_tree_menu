from django.test import TestCase
from tree_menu.models import Menu


class MenuModelTest(TestCase):
    def test_menu_model(self):
        menu = Menu.objects.create(name='Test Menu')
        self.assertEqual(menu.name, 'Test Menu')
