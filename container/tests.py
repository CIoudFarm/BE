from rest_framework.test import APITestCase
from django.urls import reverse
import time
from django.test import override_settings
from rest_framework.test import APITestCase


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class ContainerAPITestCase(APITestCase):
    def test_container_crud(self):
        index_url = reverse("crops-list")
        search_url = reverse("crops-search")

        # ✅ Create: 영어 notes 입력
        payload1 = {
            "crop_type": "Tomato",
            "growing_period": 3,
            "budget": 500000,
            "notes": (
                "High-precision temperature monitoring system with real-time alerts and "
                "historical data tracking. Ideal for greenhouse environments and sensitive crops."
            ),
            "container": "79295b05-b273-402c-9742-0d5587df3649"
        }
        response1 = self.client.post(index_url, data=payload1, format="json")

        base_url = reverse("container-list")  # /containers/

        # ✅ Create
        payload = {
            "scale": "중형",
            "hit_range": "5-10m",
            "electricity": "220V",
            "humid": "60%",
            "setting_file": {"env": "greenhouse", "temp": 24.5},
            "download_count": 3,
            "stars": 4.7,
            # "functions": ["자동 환기", "물 자동 공급"]
        }
        res = self.client.post(base_url, data=payload, format="json")
        print("\n✅ [CREATE] POST", base_url)
        print("요청 본문:", payload)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 201)
        container_id = res.data.get("id")

        # ✅ Partial Update (PATCH)
        patch_data = {"humid": "70%"}
        patch_url = reverse("container-detail", args=[container_id])
        res = self.client.patch(patch_url, data=patch_data, format="json")
        print("\n✅ [PATCH] PATCH", patch_url)
        print("요청 본문:", patch_data)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ List
        res = self.client.get(base_url)
        print("\n✅ [LIST] GET", base_url)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ Retrieve
        retrieve_url = reverse("container-detail", args=[container_id])
        res = self.client.get(retrieve_url)
        print("\n✅ [RETRIEVE] GET", retrieve_url)
        print("응답:", res.data)
        self.assertEqual(res.status_code, 200)

        # ✅ Delete
        res = self.client.delete(retrieve_url)
        print("\n✅ [DELETE] DELETE", retrieve_url)
        print("응답 상태코드:", res.status_code)
        self.assertEqual(res.status_code, 204)
