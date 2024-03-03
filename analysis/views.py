from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import QuerySet

from analysis.utils import WikiAnalysisUtil
from .models import SearchResult
from .const import SEARCH_HISTORY_DATETIME_FORMAT
from wikipedia_analysis.loggers import logging


logger = logging.getLogger("wiki_analysis")


class WikiSearch(View):
    def get(self, request, *args, **kwargs):
        """
            Method to return the analysis of top words based on the WIKI topic to be searched
        :param request: HTTPRequest object
        :return: JSON Response
            On success:
                {
                    "topic": "database sharding",
                    "word_frequency": [
                        {
                            "word": frequency
                        }
                    ]
                }

            On Failure:
            {
                "error": "error"
            }
        """
        topic = request.GET.get('topic', '')
        if not topic:
            logger.error(f"No topic provided. Topic:: {topic}")
            return JsonResponse({'error': 'Topic is required'}, status=400)
        top_word_count = int(request.GET.get('n', 10))
        try:
            util_obj = WikiAnalysisUtil(topic=topic, top_word_count=top_word_count, skip_common_words=True,
                                        skip_numbers=True)
            word_freq_data = util_obj.process()
        except Exception as ex:
            return JsonResponse({"error": f"{ex}"}, status=400)
        return JsonResponse(word_freq_data, status=200)


class WikiHistory(View):
    def get(self, request, *args, **kwargs):
        """
            Method to return the analysis of top words based on the WIKI topic to be searched
        :param request: HTTPRequest object
        :return: JSON Response, list of search results
            On success:
            {
                data: [
                    {
                        "topic": "database sharding",
                        "word_frequency": [
                            {
                                "word": frequency
                            }
                        ]
                    }
                ],
                pagination: {
                    'current_page': ,
                    'total_pages': ,
                    'total_results': ,
                    'next_page': ,
                    'previous_page:
                }
            }
        """

        # Default values for pagination parameters
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        if isinstance(page_size, str) and not page_size.isnumeric():
            return JsonResponse({'error': "Invalid page size"}, status=400)
        # Fetch all search results ordered by creation time
        search_results = SearchResult.objects.all().order_by('-created_at')

        # Create a Paginator object
        paginator = Paginator(search_results, page_size)

        # Get the search results for the requested page
        try:
            search_results_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            search_results_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver the last page of results.
            search_results_page = paginator.page(paginator.num_pages)

        # Prepare the search history data
        search_history = [
            {
                'topic': result.topic,
                'word_frequency': result.word_frequency,
                'created_at': result.created_at.strftime(SEARCH_HISTORY_DATETIME_FORMAT)
            }
            for result in search_results_page
        ]

        # Include pagination information in the response
        pagination_info = {
            'current_page': search_results_page.number,
            'total_pages': paginator.num_pages,
            'total_results': paginator.count,
            'next_page': search_results_page.has_next() and search_results_page.next_page_number() or None,
            'previous_page': search_results_page.has_previous() and search_results_page.previous_page_number() or None,
        }

        return JsonResponse({'data': search_history, 'pagination': pagination_info})
