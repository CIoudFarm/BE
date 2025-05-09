import requests

def create_crop_index():
    index_name = "crops"
    url = f"http://localhost:9200/{index_name}"

    # 이미 존재하면 생략
    if requests.head(url).status_code == 200:
        return

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
                "crop_type": {"type": "text"},
                "growing_period": {"type": "text"},
                "budget": {"type": "text"},
                "notes": {"type": "text", "analyzer": "korean_nori"}
            }
        }
    }

    response = requests.put(url, json=mapping)
    response.raise_for_status()
