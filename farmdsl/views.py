from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from .serializers import CropSearchSerializer

es = Elasticsearch("http://localhost:9200")


class CropSearchViewSet(viewsets.ViewSet):
    index_name = "crops"

    # 1. Create - 색인
    def create(self, request):
        serializer = CropSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = es.index(index=self.index_name, body=serializer.validated_data)
        return Response({"id": result['_id'], "message": "Indexed successfully"}, status=status.HTTP_201_CREATED)

    # 2. Retrieve - 단일 문서 조회 (GET /crops/{id}/)
    def retrieve(self, request, pk=None):
        try:
            result = es.get(index=self.index_name, id=pk)
            return Response(result["_source"], status=status.HTTP_200_OK)
        except NotFoundError:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

    # 3. Update - 문서 전체 수정 (PUT /crops/{id}/)
    def update(self, request, pk=None):
        serializer = CropSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            es.update(index=self.index_name, id=pk, body={"doc": serializer.validated_data})
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        except NotFoundError:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

    # 4. Delete - 문서 삭제 (DELETE /crops/{id}/)
    def destroy(self, request, pk=None):
        try:
            es.delete(index=self.index_name, id=pk)
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFoundError:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)

    # 5. List - 모든 문서 조회 (GET /crops/)
    def list(self, request):
        result = es.search(index=self.index_name, body={"query": {"match_all": {}}})
        hits = [hit["_source"] | {"id": hit["_id"]} for hit in result["hits"]["hits"]]
        return Response(hits, status=status.HTTP_200_OK)

    # 6. Search - 조건 검색 (POST /crops/search/)
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
                        "growing_period": {"lte": period_value}
                    }
                })
            except ValueError:
                pass

        if budget:
            try:
                budget_value = int(budget)
                filter_queries.append({
                    "range": {
                        "budget": {"lte": budget_value}
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
        hits = [hit["_source"] | {"id": hit["_id"]} for hit in result["hits"]["hits"]]

        return Response({
            "count": len(hits),
            "results": hits
        }, status=status.HTTP_200_OK)
