from elasticsearch import Elasticsearch
import os

# 创建Elasticsearch客户端对象
es = Elasticsearch()

# 定义索引名
index_name = 'my_index_test'

# 如果索引已经存在，则删除它
if es.indices.exists(index_name):
    es.indices.delete(index=index_name)

# 创建索引，并设置映射
body = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"
            },
            "content": {
                "type": "text"
            }
        }
    }
}
es.indices.create(index=index_name, body=body)

# 将所有文档添加到Elasticsearch中
docs_path = 'C:\\Users\\56975\\Desktop\\gobug'
for filename in os.listdir(docs_path):
    with open(os.path.join(docs_path, filename), 'r', encoding='utf-8') as f:
        text = f.read()
        es.index(index=index_name, id=filename, body={
            "title": filename,
            "content": text
        })


# 定义搜索函数，接收一个关键词参数，返回匹配结果
def search(keyword):
    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["title", "content"]
            }
        }
    }

    res = es.search(index=index_name, body=body)
    return res['hits']['hits']


# 在命令行交互模式下进行测试
while True:
    keyword = input("请输入关键词：")
    results = search(keyword)
    for result in results:
        # print(result['_source']['title'], result['_source']['content'])
        print(result['_source']['title'])