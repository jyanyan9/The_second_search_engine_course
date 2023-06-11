import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_same():
    # 输入文件夹名称和阈值比较
    lan = input('请选择文件夹（chinese or english）:')
    folder = 'C:\\Users\\56975\\Desktop\\gobug_' + lan
    file1 = input('请输入文件序号（1-600）：')
    filename = 'News_10' + file1 + '_Result_' + lan + '.txt'
    file_path = os.path.join(folder, filename)
    threshold = float(input("请输入相似度阈值（0-1之间的小数）："))

    # 创建特征向量化的对象
    vectorizer = CountVectorizer(analyzer='char',token_pattern=u"(?u)\b\w+\b")

    # 读入字符串
    with open(file_path, encoding='utf-8') as file:
        text = file.read()

    # 将字符串转化为特征向量
    features = vectorizer.fit_transform([text])

    # 计算余弦相似度
    for compare_file in os.listdir(folder):
        compare_file_path = os.path.join(folder, compare_file)

        # 排除和自己同名文件
        if compare_file_path == file_path:
            continue

        # 读入字符串
        with open(compare_file_path, encoding='utf-8') as file:
            compare_text = file.read()

        # 将字符串转化为特征向量并与当前文件进行比较
        compare_features = vectorizer.transform([compare_text])
        similarity_score = cosine_similarity(features, compare_features)[0][0]

        # 如果相似度达到阈值，则输出命中信息
        if similarity_score >= threshold:
            print(f"{filename} 和 {compare_file} 的相似度为 {similarity_score}")


while True:
    check_same()
    print('\n')
