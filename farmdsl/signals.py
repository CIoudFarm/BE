# farmdsl/signals.py

from farm.es.index_initializer import create_crop_index

def create_elasticsearch_index(sender, **kwargs):
    try:
        create_crop_index()
        print("✅ Elasticsearch 'crops' 인덱스가 준비되었습니다.")
    except Exception as e:
        print("❌ Elasticsearch 인덱스 생성 실패:", e)
