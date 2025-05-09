# farm/es/index_initializer.py

import requests

def create_crop_index():
    index_name = "crops"
    url = f"http://localhost:9200/{index_name}"

    # 기존 인덱스가 존재하면 삭제
    if requests.head(url).status_code == 200:
        print("⚠️ 기존 인덱스 삭제 중...")
        delete_response = requests.delete(url)
        delete_response.raise_for_status()
        print("🗑️ 기존 인덱스 삭제 완료")

    mapping = {
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
            "crop_type": {
                "type": "text",
                "analyzer": "korean_nori"
            },
            "growing_period": {
                "type": "integer"
            },
            "budget": {
                "type": "integer"
            },
            "notes": {
                "type": "text",
                "analyzer": "korean_nori"
            },
            "url": {
                "type": "keyword"
            },
            "setting_file": {
                "type": "object",
                "properties": {
                "setting": {
                    "type": "text"
                }
                }
            }
            }
        }
        }


    try:
        response = requests.put(url, json=mapping)
        response.raise_for_status()
        print("✅ Elasticsearch 'crops' 인덱스 생성 완료")
    except Exception as e:
        print("❌ Elasticsearch 인덱스 생성 실패:", e)
        print("응답 내용:", response.text)
        raise
