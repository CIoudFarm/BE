# 가능한 인덱스
# crop_index

import requests

def create_crop_index():
    index_name = "crops"
    url = f"http://localhost:9200/{index_name}"

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
                "container": {
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
