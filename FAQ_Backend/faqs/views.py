from rest_framework import viewsets
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request, *args, **kwargs):
        lang = request.GET.get('lang', 'en')
        faqs = self.get_queryset()
        serializer = self.get_serializer(faqs, many=True, context={'request': request})
        return Response(serializer.data)
