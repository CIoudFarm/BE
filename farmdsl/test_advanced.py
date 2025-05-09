import uuid
import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from container.models import Container
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


class CropSearchViewSetTest(APITestCase):
    def setUp(self):
        self.index_url = reverse('crops-list')
        self.search_url = reverse('crops-search')
        self.base_upload_url = reverse('crops-base-upload')

    def _print_api_result(self, api_name, method, url, request_data, response):
        print(f"\n🔹 [{api_name}]")
        print(f"[{method}] {url}")
        print("Request:", json.dumps(request_data, ensure_ascii=False))
        print("Response:", response.status_code, response.json())
        print("---------------- ")

    def test_create_crop_index(self):
        data = {
            "crop_type": "옥수수",
            "notes": "태풍에 강하고 생산량이 높음",
            "growing_period": 90,
            "budget": 50000
        }
        response = self.client.post(self.index_url, data, format='json')
        self._print_api_result("test_create_crop_index", "POST", self.index_url, data, response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_search_crop_with_notes(self):
        # 색인 먼저
        index_data = {
            "crop_type": "상추",
            "notes": "여름에 적합한 작물",
            "growing_period": 40,
            "budget": 30000
        }
        self.client.post(self.index_url, index_data, format='json')
        es.indices.refresh(index='crops')

        search_data = {
            "crop_type": "상추",
            "notes": "여름"
        }
        response = self.client.post(self.search_url, search_data, format='json')
        self._print_api_result("test_search_crop_with_notes", "POST", self.search_url, search_data, response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_base_upload(self):
        file_content = json.dumps({"config": "value"})
        tags = json.dumps(["전력 효율", "습도 자동 조절"])
        data = {
            "file": self._create_file(file_content),
            "notes": "이 컨테이너는 자동 기능이 있습니다.",
            "tags": tags,
        }

        response = self.client.post(self.base_upload_url, data, format="multipart")
        self._print_api_result("test_base_upload", "POST", self.base_upload_url, {"notes": data["notes"], "tags": tags}, response)

        self.assertEqual(response.status_code, 200)
        self.assertIn("container_id", response.data)

    def test_upload_to_existing_container(self):
        container = Container.objects.create(
            name="테스트 컨테이너", creater="test", scale="중간", hit_range="10m", electricity="220V", humid="60%"
        )
        upload_url = reverse('crops-upload', args=[str(container.pk)])

        file_content = json.dumps({"config": "new"})
        data = {
            "file": self._create_file(file_content)
        }

        response = self.client.post(upload_url, data, format="multipart")
        self._print_api_result("test_upload_to_existing_container", "POST", upload_url, {}, response)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["setting_file"]["config"], "new")

    def _create_file(self, content: str):
        from django.core.files.uploadedfile import SimpleUploadedFile
        return SimpleUploadedFile("test.json", content.encode("utf-8"), content_type="application/json")
