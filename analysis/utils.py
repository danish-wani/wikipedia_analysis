import re
import requests
from collections import Counter

WIKI_BASE_URL = "https://en.wikipedia.org/w/api.php"


class AnalysisUtil:
    """
        Utility class for handling the business logic of Wiki Analysis
    """
    WIKI_TOPIC_SEARCH_URL = f"{WIKI_BASE_URL}?action=query&prop=extracts&format=json&exintro="
    COMMON_WORDS = ['the', 'is', 'in', 'at', 'which', 'on']

    def __init__(self, topic: str, top_word_count: int = 10, skip_common_words: bool = False,
                 skip_numbers: bool = False) -> None:
        """
            Constructor to initialize the topic and top_word_count
        :param topic: Topic to be searched
        :param top_word_count: An integer specifying the number of top frequent words to return
        :param skip_common_words: (bool) if defined common words are not to be considered
        :param skip_numbers: (bool) if numbers are to be skipped
        """
        self.topic = self.clean_input_topic(topic)
        self.top_word_count = top_word_count
        self.skip_common_words = skip_common_words
        self.skip_numbers = skip_numbers

    @staticmethod
    def clean_input_topic(topic: str) -> str:
        """
            Static method to return the cleaned topic in lower case
        :param topic: Topic name
        :return: Cleaned topic
        """
        if topic and isinstance(topic, str):
            return topic.strip().lower()
        raise ValueError("Topic is invalid.")

    def _check_to_skip(self, word: str) -> bool:
        """
            Method to check if a word has to be skipped
        :param word: Word to check for sanity
        :return: bool, True if word is to be considered else False
        """
        good_to_go = True
        if self.skip_common_words:
            if word not in self.COMMON_WORDS:
                good_to_go = True

        if self.skip_numbers:
            good_to_go = not word.isnumeric()

        return good_to_go

    def word_frequency_analysis(self, text):
        """
            Method to find the common words in the text and returns the top self.top_word_count words
        :param text: Text to be analysed for words and their frequency
        :return: top self.top_word_count words along with their counts
        """
        # Tokenize the text
        words = re.findall(r'\w+', text.lower())
        words_list = [word for word in words]

        # Filter out common words or numbers
        if self.skip_numbers or self.skip_common_words:
            filtered_words = list(filter(self._check_to_skip, words_list))
        else:
            filtered_words = words_list
        word_freq = Counter(filtered_words)
        return word_freq.most_common(self.top_word_count)

    @staticmethod
    def remove_html_tags(text: str):
        """
            Remove the HTML tags from the text and return the HTML less text.
        :param text: Text containing the HTML tags
        :return: Text without the HTML tags
        """
        # regular expression to match any text that starts with <, followed by any number of characters,
        # and ends with >, which is the pattern for HTML tags. It then replaces these matches with an empty string,
        # effectively removing them.
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def _extract_text(self, pages):
        """
            Method to extract text from WIKI pages
        :param pages: Page object
        :return: Text from the page(s)
        :raises:
            ValueError if no page found
        """
        try:
            text = list(pages.values())[0]['extract']
            # Remove the HTML tags from the text
            text = self.remove_html_tags(text)
        except IndexError:
            raise ValueError("No data found")
        return text

    def fetch_wikipedia_article(self):
        """
            Method to fetch the text of a Wikipedia article
        :return:
        """
        url = f"{self.WIKI_TOPIC_SEARCH_URL}&titles={self.topic}"
        response = requests.get(url)
        # Raise error if the response status is not in 2xx
        response.raise_for_status()
        data = response.json()
        pages = data['query']['pages']
        return pages

    def run_analysis(self) -> dict:
        """
            Processes the topic and returns Json containing the topic and the `top_word_count` word to count data
        :return: Json containing the topic and the `top_word_count` word to count data
        """
        pages = self.fetch_wikipedia_article()
        # Extract the text of the first page
        text = self._extract_text(pages)
        word_freq = self.word_frequency_analysis(text)

        return dict(topic=self.topic, top_words=word_freq)

