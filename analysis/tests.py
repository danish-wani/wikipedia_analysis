from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

from analysis.utils import WikiAnalysisUtil
from analysis.models import SearchResult


class TestWikiAnalysisUtil(TestCase):

    @patch('requests.get')
    def test_fetch_wikipedia_article_success(self, mock_get):
        # Mock a successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'query': {
                'pages': {
                    '123': {
                        'extract': 'This is a test extract.'
                    }
                }
            }
        }
        mock_get.return_value = mock_response

        util = WikiAnalysisUtil('test topic')
        pages = util.fetch_wikipedia_article()
        self.assertEqual(pages, mock_response.json()['query']['pages'])

    def test_word_frequency_analysis_empty_text(self):
        util = WikiAnalysisUtil('test topic')
        word_freq = util.word_frequency_analysis('')
        self.assertEqual(word_freq, [])

    def test_word_frequency_analysis_with_common_words(self):
        util = WikiAnalysisUtil('test topic', skip_common_words=True)
        text = "This is a test. This is only a test."
        word_freq = util.word_frequency_analysis(text)
        self.assertEqual(word_freq, [('test', 2), ('only', 1)])

    def test_word_frequency_analysis_with_numbers(self):
        util = WikiAnalysisUtil('test topic', skip_numbers=True)
        text = "This is a test. This is only a test. 123"
        word_freq = util.word_frequency_analysis(text)
        self.assertEqual(word_freq, [('this', 2), ('is', 2), ('a', 2), ('test', 2), ('only', 1)])

    def test_clean_input_topic_empty_input(self):
        with self.assertRaises(ValueError):
            WikiAnalysisUtil('')

    def test_clean_input_topic_non_string_input(self):
        with self.assertRaises(ValueError):
            WikiAnalysisUtil(123)

    def test_remove_html_tags_empty_text(self):
        util = WikiAnalysisUtil('test topic')
        clean_text = util.remove_html_tags('')
        self.assertEqual(clean_text, '')

    def test_remove_html_tags_with_html(self):
        util = WikiAnalysisUtil('test topic')
        html_text = "<p>This is a paragraph with <b>bold</b> text.</p>"
        clean_text = util.remove_html_tags(html_text)
        self.assertEqual(clean_text, "This is a paragraph with bold text.")


class WikiHistoryViewTest(TestCase):
    def setUp(self):
        # Create some search results
        for _ in range(20):
            SearchResult.objects.create(topic="database sharding",
                                        word_frequency=[{"word": "database", "frequency": 5}])

    def test_successful_request_with_default_pagination(self):
        response = self.client.get(reverse('search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(len(response.json()['data']), 10) # Default page size is 10
        self.assertEqual(response.json()['pagination']['current_page'], 1)
        self.assertEqual(response.json()['pagination']['total_pages'], 2)
        self.assertEqual(response.json()['pagination']['total_results'], 20)
        self.assertEqual(response.json()['pagination']['next_page'], 2)
        self.assertIsNone(response.json()['pagination']['previous_page'])

    def test_successful_request_with_custom_pagination(self):
        response = self.client.get(reverse('search_history'), {'page': 2, 'page_size': 5})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(len(response.json()['data']), 5)  # Custom page size is 5
        self.assertEqual(response.json()['pagination']['current_page'], 2)
        self.assertEqual(response.json()['pagination']['total_pages'], 4)
        self.assertEqual(response.json()['pagination']['total_results'], 20)
        self.assertEqual(response.json()['pagination']['next_page'], 3)
        self.assertEqual(response.json()['pagination']['previous_page'], 1)

    def test_request_with_invalid_pagination_parameters(self):
        response = self.client.get(reverse('search_history'), {'page': 'invalid', 'page_size': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_request_when_no_search_results(self):
        SearchResult.objects.all().delete()
        response = self.client.get(reverse('search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(len(response.json()['data']), 0)
        self.assertEqual(response.json()['pagination']['current_page'], 1)
        self.assertEqual(response.json()['pagination']['total_pages'], 1)
        self.assertEqual(response.json()['pagination']['total_results'], 0)
        self.assertIsNone(response.json()['pagination']['next_page'])
        self.assertIsNone(response.json()['pagination']['previous_page'])


if __name__ == '__main__':
    unittest.main()
