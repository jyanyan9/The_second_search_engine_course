import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# 读取文档数据
data_path = input("请输入文档路径：")
docs = []  # 存储从文档中读取的文本数据
for filename in os.listdir(data_path):  # 遍历指定目录下的所有文件
    filepath = os.path.join(data_path, filename)  # 构建文件路径
    with open(filepath, encoding='utf-8') as f:
        doc = f.read()  # 读取文件内容
        docs.append(doc)

# 文本向量化
vectorizer = TfidfVectorizer(analyzer='char',token_pattern=u"(?u)\b\w+\b")
X = vectorizer.fit_transform(docs)

# 聚类
n_clusters = int(input("请输入聚类数目："))  # 指定聚类的类别数
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', max_iter=1000, n_init=10)
kmeans.fit(X)

# 显示三个最大的类及每个类中代表性的文档
doc_labels = kmeans.labels_
doc_centers = kmeans.cluster_centers_
cluster_sizes = [sum(doc_labels == i) for i in range(n_clusters)]
max_clusters = sorted(range(n_clusters), key=lambda i: cluster_sizes[i], reverse=True)[:3]

for i, cluster_id in enumerate(max_clusters):  # 遍历前三大聚类
    print('Cluster {} 总共包含 {} 个文档,距离类中心最近的 5 个文档为:'.format(i + 1, cluster_sizes[cluster_id]))
    center = doc_centers[cluster_id]
    dists = [(j, cosine_similarity(center.reshape(1, -1), X[j])[0][0]) for j in
             range(X.shape[0])]
    closest_docs = sorted(dists, key=lambda x: x[1], reverse=True)[:5]
    for j, similarity in closest_docs:
        print('\t{} (similarity={:.2f})'.format(os.listdir(data_path)[j], similarity))
    print()
