import json
import uuid
import random
from pathlib import Path
from datetime import timedelta
from django.utils import timezone
from mypage.models import Instance
from container.models import Container


CONFIG_DIR = Path("farms/files")

FILES = [
    ("온실 표준형", "base_config_greenhouse_std.json", "기본 온도/습도 센서와 LED, 팬으로 구성된 표준 온실 환경입니다."),
    ("고온건조 실험환경", "base_config_hot_dry.json", "고온(35℃ 이상) 및 저습 환경에서의 작물 내성 실험을 위한 구성입니다."),
    ("저온고습 발아실", "base_config_cold_humid.json", "저온 다습 조건에서 발아를 유도하고 관찰할 수 있는 실험실 환경입니다."),
    ("수직농장 3층", "base_config_vertical_3layer.json", "3개 층의 베드 구조를 갖춘 수직 농장 환경으로, 공간 효율성을 높였습니다."),
    ("양액 재배 최적화", "base_config_hydroponics.json", "양액 센서와 급수 펌프 중심의 설정으로 수경재배에 최적화된 환경입니다."),
    ("로봇 순찰 포함형", "base_config_with_robot.json", "베드 사이를 자율적으로 순찰하는 로봇이 포함된 스마트 자동화 환경입니다."),
    ("외부 날씨 연동형", "base_config_weather_api.json", "외부 기상 API 데이터를 기반으로 내부 환경을 제어하는 시뮬레이션입니다."),
    ("조도 센서 실험", "base_config_light_sensor.json", "조도 센서를 기반으로 LED를 자동 제어하는 광량 조절 실험 환경입니다."),
    ("무작위 배치 테스트", "base_config_randomized.json", "센서 및 액추에이터가 무작위 위치에 배치된 비정형 테스트용 환경입니다."),
    ("대형 스마트팜 시뮬레이션", "base_config_large_scale.json", "10개 이상의 베드, 복수 층, 다양한 센서/액추에이터 및 로봇이 포함된 복합 대형 구성입니다."),
]

CREATER_NAMES = [
    "그린팜코리아", "에코스마트농장", "농업테크", "팜솔루션즈", "어반팜랩",
    "넥스트팜", "스마트애그리", "그로우팜", "하이브팜", "에버그린팜",
    "에이아이팜", "프레시플랜트", "에코그로스", "인텔리팜", "씨앗랩스",
    "에그리파이", "바이오팜넷", "텃밭컴퍼니", "뉴팜시스템즈", "딥팜AI"
]


def create_sample_data():
    print("📦 farms/files 기반 Instance & Container 10개 생성 시작")

    for i, (name, filename, description) in enumerate(FILES):
        config_path = CONFIG_DIR / filename
        if not config_path.exists():
            print(f"⚠️ 설정 파일 없음: {filename}")
            continue

        with open(config_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        base_config_bin = json.dumps(content, ensure_ascii=False).encode("utf-8")

        Instance.objects.create(
            name=name,
            type="표준형",
            start_date=timezone.now().date() - timedelta(days=random.randint(0, 30)),
            status="시작",
            region="서울특별시",
            base_config=base_config_bin,
            base_config_name=filename,
        )

        Container.objects.create(
            name=f"{name} 컨테이너",
            creater=random.choice(CREATER_NAMES),
            scale="10평",
            hit_range="중간",
            electricity="양호",
            humid="60%",
            functions=["LED 제어", "환기", "센서 수집"],
            setting_file=content,
            notes=description,
            stars=round(random.uniform(3.5, 5.0), 1),
            download_count=random.randint(5, 100),
            added_at=timezone.now() - timedelta(days=random.randint(0, 10)),
        )

    print("✅ farms/files 기반 데이터 10개 생성 완료")
