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
                        "growing_period": {"type": "integer"},
                        "budget": {"type": "integer"},
                        "notes": {"type": "text", "analyzer": "korean_nori"},
                    }
                }
            }
        )

    def tearDown(self):
        self.es.indices.delete(index=self.ES_INDEX)

    def test_crop_crud_and_search(self):
        index_url = reverse("crops-list")
        search_url = reverse("crops-search")

        # ✅ Create
        payload1 = {
            "crop_type": "토마토",
            "growing_period": 3,
            "budget": 500000,
            "notes": "물 많이 줘야 함"
        }
        response1 = self.client.post(index_url, data=payload1, format="json")
        print("\n✅ [CREATE] POST", index_url)
        print("요청 본문:", payload1)
        print("응답:", response1.data)
        self.assertEqual(response1.status_code, 201)
        id1 = response1.data["id"]

        payload2 = {
            "crop_type": "감자",
            "growing_period": 2,
            "budget": 400000,
            "notes": "비료 줘야 함"
        }
        response2 = self.client.post(index_url, data=payload2, format="json")
        print("\n✅ [CREATE] POST", index_url)
        print("요청 본문:", payload2)
        print("응답:", response2.data)
        self.assertEqual(response2.status_code, 201)
        id2 = response2.data["id"]

        time.sleep(1)

        # ✅ List
        res = self.client.get(index_url)
        print("\n✅ [LIST] GET", index_url)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ Retrieve
        retrieve_url = reverse("crops-detail", args=[id1])
        res = self.client.get(retrieve_url)
        print("\n✅ [RETRIEVE] GET", retrieve_url)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ Update
        update_data = {
            "crop_type": "토마토",
            "growing_period": 5,
            "budget": 600000,
            "notes": "수정됨"
        }
        res = self.client.put(retrieve_url, data=update_data, format="json")
        print("\n✅ [UPDATE] PUT", retrieve_url)
        print("요청 본문:", update_data)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ Delete
        delete_url = reverse("crops-detail", args=[id2])
        res = self.client.delete(delete_url)
        print("\n✅ [DELETE] DELETE", delete_url)
        print("응답 상태코드:", res.status_code)
        self.assertEqual(res.status_code, 204)

        time.sleep(1)

        # ✅ Search
        search_payload = {"notes": "물"}
        res = self.client.post(search_url, data=search_payload, format="json")
        print("\n✅ [SEARCH] POST", search_url)
        print("요청 본문:", search_payload)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        search_payload2 = {"crop_type": "토마토", "notes": "수정됨"}
        res = self.client.post(search_url, data=search_payload2, format="json")
        print("\n✅ [SEARCH] POST", search_url)
        print("요청 본문:", search_payload2)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)
