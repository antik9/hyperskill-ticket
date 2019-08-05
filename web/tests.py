from django.test import TestCase
from django.shortcuts import reverse


class TestWeb(TestCase):

    def test__answer(self):
        print(self.client.get(reverse('main')).content)

    def _post_teardown(self):
        ...
