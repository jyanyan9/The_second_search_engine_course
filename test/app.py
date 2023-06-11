from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=['POST'])   
def search():
    keyword = request.form['query'].lower()
    body = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["title", "content"]
            }
        }
    }
    res = es.search(index='my_index_test', body=body)
    results = res['hits']['hits']
    results = [(item['_source']['title'])for item in results]
    return render_template("results.html", results=results, query=keyword)

if __name__ == '__main__':
    app.run(debug=True)