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

    # 검색: GET /crops/?q=...
    def list(self, request):
        query = request.query_params.get("q", "")

        body = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"crop_type": query}},
                        {"match": {"growing_period": query}},
                        {"match": {"budget": query}},
                        {"match": {"notes": {"query": query, "fuzziness": "AUTO"}}}
                    ]
                }
            }
        }

        result = es.search(index=self.index_name, body=body)
        hits = [hit["_source"] for hit in result["hits"]["hits"]]
        return Response(hits, status=status.HTTP_200_OK)
