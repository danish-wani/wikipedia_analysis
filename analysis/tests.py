from django.test import TestCase

from unittest.mock import patch, MagicMock
from analysis.utils import WikiAnalysisUtil


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


if __name__ == '__main__':
    unittest.main()
