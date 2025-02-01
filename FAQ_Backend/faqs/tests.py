from django.test import TestCase
from .models import FAQ

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(question="Hello", answer="This is a test FAQ", language='en')

    def test_translation(self):
        self.assertIsNotNone(self.faq.get_translated_question('hi'))
