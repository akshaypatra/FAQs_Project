import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from deep_translator import GoogleTranslator
from django_ckeditor_5.fields import CKEditor5Field

# Language choices 
LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali'),
    ('mr', 'Marathi'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
    ('gu', 'Gujarati'),
    ('kn', 'Kannada'),
    ('ml', 'Malayalam'),
    ('pa', 'Punjabi'),
    ('ur', 'Urdu'),
    ('or', 'Odia'),
    ('as', 'Assamese'),
    ('kok', 'Konkani'),
    ('mai', 'Maithili'),
    ('ne', 'Nepali'),
    ('sa', 'Sanskrit'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('ru', 'Russian'),
    ('ar', 'Arabic'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ko', 'Korean'),
    ('tr', 'Turkish'),
    ('nl', 'Dutch'),
]

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = CKEditor5Field("Answer", config_name="default")
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en') 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.translate_question()  

    def translate_question(self):
        """Translate question to other languages and store in FAQTranslation model"""
        for lang_code, _ in LANGUAGE_CHOICES:
            if lang_code == 'en': 
                continue
            
            existing_translation = self.translations.filter(language=lang_code).first()
            if not existing_translation:  
                translated_text = GoogleTranslator(source='auto', target=lang_code).translate(self.question)
                FAQTranslation.objects.create(faq=self, language=lang_code, translated_question=translated_text)

    def get_translated_question(self, lang='en'):
        """Retrieve cached translated question"""
        if lang == 'en':
            return self.question
        
        cache_key = f'faq_{self.id}_{lang}'
        cached_translation = cache.get(cache_key)
        if cached_translation:
            return cached_translation

        translation = self.translations.filter(language=lang).first()
        translated_text = translation.translated_question if translation else self.question

        cache.set(cache_key, translated_text, timeout=86400)  # Cache for 24 hours
        return translated_text

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

class FAQTranslation(models.Model):
    """Model to store translated versions of FAQ questions"""
    faq = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    translated_question = models.TextField()

    def __str__(self):
        return f"{self.faq.question} ({self.language})"

    class Meta:
        unique_together = ('faq', 'language')  
