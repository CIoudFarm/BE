from rest_framework.test import APITestCase
from elasticsearch import Elasticsearch
from django.urls import reverse
import time


class CropSearchViewSetTest(APITestCase):
    ES_INDEX = "crops"

    def setUp(self):
        self.es = Elasticsearch("http://localhost:9200")
        if self.es.indices.exists(index=self.ES_INDEX):
            self.es.indices.delete(index=self.ES_INDEX)

        self.es.indices.create(
            index=self.ES_INDEX,
            body={
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "korean_nori": {
                                "type": "custom",
                                "tokenizer": "nori_tokenizer"
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "crop_type": {"type": "text"},
                        "growing_period": {"type": "text"},
                        "budget": {"type": "text"},
                        "notes": {"type": "text", "analyzer": "korean_nori"},
                    }
                }
            }
        )

    def tearDown(self):
        self.es.indices.delete(index=self.ES_INDEX)

    def test_crop_index_and_search_post(self):
        index_url = reverse("crops-list")
        search_url = reverse("crops-search")

        # 색인
        response = self.client.post(index_url, data={
            "crop_type": "토마토",
            "growing_period": 3,
            "budget": 500000,
            "notes": "물 많이 줘야 함"
        }, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.post(index_url, data={
            "crop_type": "토마토",
            "growing_period": 3,
            "budget": 500000,
            "notes": "비료 줘야 함"
        }, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.post(index_url, data={
            "crop_type": "감자",
            "growing_period": 2,
            "budget": 400000,
            "notes": "물 조금 줘야 함",
            "url": "http://localhost:8000",
            "setting_file": {
                "name": "John Doe",
                "age": 30,
                "city": "New York"
            },
        }, format="json")
        print('으아아', response.data)
        self.assertEqual(response.status_code, 201)
        # 색인 반영 대기
        time.sleep(1)

        print('테스트 결과(생성)')
        print(index_url)
        print(response.data)

        # 검색 요청 (POST /crops/search/)
        response = self.client.post(search_url, data={
            "notes": "물"
        }, format="json")

        print('테스트 결과')
        print(search_url)
        print(response.data)


        response = self.client.post(search_url, data={
            "crop_type": "감자",
            "notes": "물",
        }, format="json")

        print('테스트 결과2')
        print(search_url)
        print(response.data)
