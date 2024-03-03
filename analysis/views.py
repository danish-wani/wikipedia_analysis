from django.views import View
from django.http import JsonResponse

from analysis.utils import WikiAnalysisUtil


class WikiAnalysis(View):
    def get(self, request, *args, **kwargs):
        """
            Method to return the analysis of top words based on the WIKI topic to be searched
        :param request: HTTPRequest object
        :return: JSON Response
            On success:
                {
                    "topic": "database sharding",
                    "top_words": [
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
            return JsonResponse({'error': 'Topic is required'}, status=400)
        top_word_count = int(request.GET.get('n', 10))
        try:
            util_obj = WikiAnalysisUtil(topic=topic, top_word_count=top_word_count)
            word_freq_data = util_obj.run_analysis()
        except Exception as ex:
            return JsonResponse({"error": f"{ex}"}, status=400)
        return JsonResponse(word_freq_data, status=200)

    def post(self, request, *args, **kwargs):
        pass
