from rest_framework import serializers
from .models import FAQ, FAQTranslation

class FAQTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQTranslation
        fields = ['language', 'translated_question']

class FAQSerializer(serializers.ModelSerializer):
    translated_question = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'language', 'translated_question']

    def get_translated_question(self, obj):
        request = self.context.get('request')
        lang = request.GET.get('lang', 'en') if request else 'en'
        return obj.get_translated_question(lang)
