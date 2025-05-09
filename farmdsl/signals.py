# farmdsl/signals.py

from farm.es.index_initializer import create_crop_index

def create_elasticsearch_index(sender, **kwargs):
    create_crop_index()


import random
import uuid
from datetime import timedelta, date
from django.utils import timezone
from container.models import Container
from mypage.models import Instance


def create_sample_data():
    print("📦 샘플 데이터 생성 중...")

    type_choices = ["기본형", "표준형", "고급형"]
    status_choices = ["시작", "중지됨"]
    regions = ["전라북도", "경기도", "강원도", "충청남도", "경상남도"]
    notes_templates = [
        "전력 효율 좋음. 난방 효율 높음. 자동 제어 가능.",
        "습도 유지 기능 탁월. 원격 제어 가능.",
        "에너지 절약형 설계. 효율적인 내부 순환.",
        "농작물 생장 최적화됨. 실시간 모니터링 가능.",
    ]
    function_templates = [
        ["난방", "습도조절"],
        ["환기", "조명제어"],
        ["자동급수", "센서모니터링"],
        ["AI 제어", "전력분석"],
    ]

    # Instance 20개 생성
    for i in range(20):
        Instance.objects.create(
            name=f"스마트팜{i+1}",
            type=random.choice(type_choices),
            start_date=date.today() - timedelta(days=random.randint(0, 100)),
            status=random.choice(status_choices),
            region=random.choice(regions),
            base_config=b"config-bytes",
            base_config_name=f"config_{i+1}.bin"
        )

    print("✅ Instance 20개 생성 완료")

    # Container 20개 생성
    for i in range(20):
        Container.objects.create(
            name=f"컨테이너-{i+1}",
            creater=f"사용자{i+1}",
            scale=f"{random.randint(5, 20)}평",
            hit_range=random.choice(["낮음", "중간", "높음"]),
            electricity=random.choice(["양호", "보통", "불안정"]),
            humid=f"{random.randint(40, 70)}%",
            functions=random.choice(function_templates),
            setting_file={"temp": random.randint(18, 30), "humid": random.randint(40, 70)},
            notes=random.choice(notes_templates),
            stars=round(random.uniform(2.5, 5.0), 1),
            download_count=random.randint(0, 100),
            added_at=timezone.now() - timedelta(days=random.randint(0, 30))
        )

    print("✅ Container 20개 생성 완료")


