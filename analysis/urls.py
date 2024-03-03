from django.urls import path
from .views import WikiSearch, WikiHistory

urlpatterns = [
    path('word_frequency/', WikiSearch.as_view(), name='word_frequency'),
    path('search_history/', WikiHistory.as_view(), name='search_history'),
]
