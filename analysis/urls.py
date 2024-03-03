from django.urls import path
from .views import WikiAnalysis

urlpatterns = [
    path('word_frequency/', WikiAnalysis.as_view(), name='word_frequency'),
]
