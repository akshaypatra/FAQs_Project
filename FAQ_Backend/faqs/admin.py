from django.contrib import admin
from .models import FAQ, FAQTranslation

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'language')

class FAQTranslationAdmin(admin.ModelAdmin):
    list_display = ('faq', 'language', 'translated_question')

admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQTranslation, FAQTranslationAdmin)

