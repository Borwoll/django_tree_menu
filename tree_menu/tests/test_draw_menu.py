from django.test import RequestFactory, TestCase
from django.urls import reverse
from tree_menu.models import Menu, MenuItem
from tree_menu.templatetags.draw_menu import draw_menu


class TreeMenuTagsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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

    def test_draw_menu(self):
        request = self.factory.get('/')
        html = draw_menu({'request': request}, 'Test Menu')
        self.assertIn('<a href="/test1">Test Item 1</a>', html)
        self.assertIn('<a href="/test2">Test Item 2</a>', html)
