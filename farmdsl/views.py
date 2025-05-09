from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from elasticsearch import Elasticsearch
from .serializers import CropSearchSerializer


es = Elasticsearch("http://localhost:9200")


class CropSearchViewSet(viewsets.ViewSet):
    index_name = "crops"

    # 색인: POST /crops/
    def create(self, request):
        serializer = CropSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        es.index(index=self.index_name, body=serializer.validated_data)
        return Response({"message": "Indexed successfully"}, status=status.HTTP_201_CREATED)

    # 검색: POST /crops/search/
    @action(detail=False, methods=["post"], url_path="search")
    def search(self, request):

        crop_type = request.data.get("crop_type")
        growing_period = request.data.get("growing_period")
        budget = request.data.get("budget")
        notes = request.data.get("notes")

        must_queries = []
        filter_queries = []

        if crop_type:
            must_queries.append({"match": {"crop_type": crop_type}})

        if notes:
            must_queries.append({
                "match": {
                    "notes": {
                        "query": notes,
                        "fuzziness": "AUTO"
                    }
                }
            })

        if growing_period:
            try:
                period_value = int(growing_period)
                filter_queries.append({
                    "range": {
                        "growing_period": {
                            "lte": period_value
                        }
                    }
                })
            except ValueError:
                pass

        if budget:
            try:
                budget_value = int(budget)
                filter_queries.append({
                    "range": {
                        "budget": {
                            "lte": budget_value
                        }
                    }
                })
            except ValueError:
                pass

        if not must_queries and not filter_queries:
            return Response({"detail": "검색 조건을 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        body = {
            "query": {
                "bool": {
                    "must": must_queries,
                    "filter": filter_queries
                }
            }
        }

        result = es.search(index=self.index_name, body=body)
        hits = [hit["_source"] for hit in result["hits"]["hits"]]

        return Response({
            "count": len(hits),
            "results": hits
        }, status=status.HTTP_200_OK)
        # fields = ["crop_type", "growing_period", "budget", "notes"]
        # should_queries = []

        # for field in fields:
        #     value = request.data.get(field)
        #     if value:
        #         if field == "notes":
        #             should_queries.append({
        #                 "match": {
        #                     "notes": {
        #                         "query": value,
        #                         "fuzziness": "AUTO"
        #                     }
        #                 }
        #             })
        #         else:
        #             should_queries.append({
        #                 "match": {field: value}
        #             })

        # if not should_queries:
        #     return Response({"detail": "검색어를 하나 이상 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # body = {
        #     "query": {
        #         "bool": {
        #             "should": should_queries
        #         }
        #     }
        # }

        # result = es.search(index=self.index_name, body=body)
        # hits = [hit["_source"] for hit in result["hits"]["hits"]]

        # response_data = {
        #     'count': len(hits),
        #     'results': hits,
        # }

        # return Response(response_data, status=status.HTTP_200_OK)
