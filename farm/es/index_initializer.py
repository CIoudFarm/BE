import requests

from farmdsl.es.indice import create_crop_index


def create_index():
    url = "http://localhost:9200/_all"
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print("🗑️ 모든 인덱스 삭제 완료")
    except Exception as e:
        print("❌ 모든 인덱스 삭제 실패:", e)
        print("응답 내용:", response.text)
        raise

    # 생성
    create_crop_index()

