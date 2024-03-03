from django.db import models


class SearchResult(models.Model):
    topic = models.CharField(max_length=255, db_index=True)
    word_frequency = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_results'

    def __str__(self):
        return self.topic
