# tasks.py
from celery import shared_task
import openai
from elasticsearch import Elasticsearch

from django.conf import settings

import ast


openai.api_key = settings.OPENAI_KEY
es = Elasticsearch("http://localhost:9200")

@shared_task(bind=True, ignore_result=True)
def update_functions_from_notes(self, container_id):
    print('코발')
    try:
        # 1. Elasticsearch에서 문서 조회
        query = {
            "query": {
                "term": {
                    "container.keyword": container_id
                }
            }
        }
        result = es.search(index="crops", body=query)
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            print('코발2')
            return  # 해당 문서 없음
        print('코발3')

        doc = hits[0]
        doc_id = doc["_id"]
        source = doc["_source"]
        notes = source.get("notes", "")

        if not notes:
            return  # notes 없음

        # 2. GPT API 호출
        prompt = f"""
            아래 문장을 읽고, '전력 효율 좋음', '난방 효율 좋은'과 같은 형태의 명사형 기능 설명 리스트를 만들어 주세요.
            문장: "{notes}"
            결과는 리스트[str] 형태로 반환해 주세요.
        """.strip()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 명사형 기능을 추출하는 도우미입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message["content"]
        # 간단한 리스트 파싱

        try:
            parsed_list = ast.literal_eval(content)
            assert isinstance(parsed_list, list)
        except Exception:
            print('ㅅ야발')
            return  # GPT 응답이 이상할 경우 업데이트하지 않음

        # 3. Elasticsearch 문서 업데이트
        es.update(index="crops", id=doc_id, body={
            "doc": {
                "functions": parsed_list
            }
        })

    except Exception as e:
        print('컨테이너 기능 생성에 문제 ')
