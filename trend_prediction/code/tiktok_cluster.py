##### Keywords&Count of Cluster #####



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import jieba
import jieba.posseg as pseg
from nltk.corpus import stopwords
import nltk
import re

# 确保nltk的停用词表已下载
nltk.download('stopwords')
stop_words = set(stopwords.words('chinese'))

# 自定义中文停用词列表
custom_stopwords = ['的', '了', '是', '在', '和','有','也','与','中','对']
stop_words.update(custom_stopwords)

# 读取CSV文件
data = pd.read_csv('./data/tiktok/tiktok_中山大学_choose_only_trending.csv', encoding='utf-8')

# 中文分词并筛选名词函数
def preprocess_text_nouns(text):
    # 分词并标注词性
    words = pseg.cut(text)
    # 筛选名词并去停用词
    nouns = [word for word, flag in words if flag == 'n' and word not in stop_words]
    return ' '.join(nouns)

# 数据预处理
data['Processed_Title'] = data['title'].apply(preprocess_text_nouns)

# 特征提取 - TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['Processed_Title'])

# 寻找最佳聚类数
sil_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    sil_scores.append(score)
    print(f'For n_clusters={k}, the Silhouette Score is {score}')

optimal_k = sil_scores.index(max(sil_scores)) + 2
print(f'\nOptimal number of clusters: {optimal_k}')

# 应用KMeans聚类
kmeans = KMeans(n_clusters=optimal_k)
data['Cluster'] = kmeans.fit_predict(X)

# 保存聚类结果到新的CSV文件，同时保留原始数据
data.to_csv('./data/tiktok/tiktok_中山大学_clustered_data.csv', index=False, encoding='utf-8')

# 获取名词关键词的函数
def get_cluster_noun_keywords(cluster_num, n_terms=5):
    terms = vectorizer.get_feature_names_out()
    sorted_centroids = kmeans.cluster_centers_[cluster_num].argsort()[::-1]
    
    # 直接收集名词关键词，正确处理生成器对象
    noun_keywords = []
    for idx in sorted_centroids[:n_terms]:
        word_gen = pseg.cut(terms[idx])
        try:
            word, flag = next(word_gen)
            if flag == 'n':
                noun_keywords.append(word)
        except StopIteration:
            # 处理解析词时可能遇到的空值或单字无法切分的情况
            continue
    
    return noun_keywords

# 收集所有聚类的名词关键词
cluster_keywords = {f'Cluster {i}': ', '.join(get_cluster_noun_keywords(i)) for i in range(optimal_k)}

# 收集所有聚类的关键词及每个聚类的样本数量
cluster_details = []
for i in range(optimal_k):
    cluster_mask = data['Cluster'] == i
    cluster_size = cluster_mask.sum()
    keywords = ', '.join(get_cluster_noun_keywords(i))
    cluster_details.append((f'Cluster {i}', keywords, cluster_size))

# 将聚类关键词信息及样本数量保存到CSV
cluster_summary = pd.DataFrame(cluster_details, columns=['Cluster', 'Keywords', 'Sample Count'])
cluster_summary.to_csv('./data/tiktok/tiktok_中山大学_cluster_keywords_nouns.csv', index=False, encoding='utf-8')

print("Clustered data and cluster noun keyword summaries with sample counts have been saved.")



##### ------------------ #####



##### Count Keywords #####



import pandas as pd

# 读取CSV文件
df = pd.read_csv('./data/tiktok/tiktok_中山大学_cluster_keywords_nouns2.csv')  # 请将'your_file.csv'替换为你的文件名

# 将"Keywords"列的字符串转换为列表以便遍历
df['Keywords'] = df['Keywords'].str.split(', ')

# 初始化一个空的字典来存储关键词计数
keyword_counts = {}

# 遍历数据框的每一行
for index, row in df.iterrows():
    cluster = row['Cluster']
    keywords = row['Keywords']
    sample_count = row['Sample Count']
    
    # 对于该行中的每个关键词
    for keyword in keywords:
        # 构建一个复合键，用于区分不同Cluster下的相同关键词
        composite_key = f"{cluster}_{keyword}"
        
        # 更新或添加关键词计数
        if composite_key in keyword_counts:
            keyword_counts[composite_key] += sample_count
        else:
            keyword_counts[composite_key] = sample_count

# 计算每个不重复关键词的总出现次数
unique_keyword_counts = {}
for key, value in keyword_counts.items():
    cluster, keyword = key.split('_')
    if keyword not in unique_keyword_counts:
        unique_keyword_counts[keyword] = value
    else:
        unique_keyword_counts[keyword] += value

# 打印每个关键词的总出现次数
for keyword, total_count in unique_keyword_counts.items():
    print(f"{keyword}: {total_count}")
    
# 创建一个新的DataFrame来保存关键词及其总出现次数
result_df = pd.DataFrame(list(unique_keyword_counts.items()), columns=['Keyword', 'Total Count'])

# 将结果保存到新的CSV文件
result_df.to_csv('./data/tiktok/tiktok_中山大学_keyword_counts2.csv', index=False)  # 文件名可根据需要修改

print("关键词统计结果已保存至 'keyword_counts.csv'")



##### ------------------ #####