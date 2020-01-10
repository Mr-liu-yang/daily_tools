# encoding=utf8
from elasticsearch import Elasticsearch
import json

es = Elasticsearch([{'host':'106.5.3.10','port':9129}], http_auth=('', ''))

body = {
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "office": "仿冒"
          }
        }
      ]
    }
  }
}

rs=[]
filedata=es.search(index="apk_meta", doc_type="data",scroll='20m',timeout='60s',size=500, body=body)
scroll_id=filedata["_scroll_id"]
total=filedata["hits"]["total"]

print("start write data into file")
with open("fangmao.json",'w+') as f:
    for onedict in filedata["hits"]["hits"]:
        f.write(json.dumps(onedict["_source"]))
        f.write("\n")

    for i in range(total/500):
        print(i)
        res=es.scroll(scroll_id=scroll_id,scroll='20m')
        for onedict in res["hits"]["hits"]:
            f.write(json.dumps(onedict["_source"]))
            f.write("\n")
