from openai import OpenAI
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import torch
import numpy as np
import pandas as pd


def extract_news(csv_file_path):
  # 读取CSV文件
  df = pd.read_csv(csv_file_path, encoding='GBK')
  # 创建一个空列表用于存放提取的内容
  column_list = []
  # 遍历数据框的每一行
  if csv_file_path == '中山大学腾讯网.csv':
      for index, row in df.iterrows():
          # 提取第一列和第二列的内容，并组合成一个新的字符串，中间加上句号
          combined_value = row.iloc[0] if pd.isna(row.iloc[1]) else f"{row.iloc[0]}。{row.iloc[1]}"
          # 将组合结果添加到列表中
          column_list.append(combined_value)
  if csv_file_path == '中山大学凤凰网.csv':
      for index, row in df.iterrows():
          if not pd.isna(row.iloc[2]):
              combined_value = f"{row.iloc[0]}。{row.iloc[2]}"
              combined_value = combined_value.replace(" ", "").replace("\n", "")  # 清除空格和空行
              column_list.append(combined_value)
  return column_list


def tokenize(news_list, bert_name='acge_text_embedding', max_length=256):
    # 初始化 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    # 编码文本数组
    inputs = tokenizer.batch_encode_plus(
        news_list,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids = inputs['input_ids']
    attention_masks = inputs['attention_mask']
    return input_ids, attention_masks


def cluster_news(input_ids, attention_masks, eps=12, min_samples=2):
    # 加载预训练的BERT模型
    model = AutoModel.from_pretrained('acge_text_embedding')
    # 使用BERT模型获取词嵌入向量
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
        embeddings = outputs[0][:, 0, :].numpy()  # 取每个句子的CLS向量作为句子的嵌入向量
    # 使用DBSCAN算法进行文本聚类
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(embeddings)
    # 将每个噪声点单独归为一个簇
    for i, label in enumerate(labels):
        if label == -1:
            labels[i] = max(labels) + 1
    # 计算每个簇的簇心
    cluster_centers = []
    for label in set(labels):
        cluster_center = embeddings[labels == label].mean(axis=0)
        cluster_centers.append(cluster_center)
    return labels, cluster_centers

def display_clustered_news(news_list, labels):
    # 创建一个字典，用于存放每个类别的新闻
    clustered_news = {}
    # 遍历每个新闻和其对应的类别标签
    for news, label in zip(news_list, labels):
        # 如果该类别标签不存在于字典中，创建一个新的列表
        if label not in clustered_news:
            clustered_news[label] = []
        # 将该新闻添加到对应类别的列表中
        clustered_news[label].append(news)
    # 打印每个类别下的新闻
    for label, news in clustered_news.items():
        print(f"Cluster {label}:")
        # 生成事件标题
        event_title = generate_event_title(news)
        print("Event Title:", event_title)
        # 打印每个类别下的新闻
        for item in news:
            print(item)
        print("")


def find_nearest_cluster(new_news, cluster_centers, threshold=0.2):
    new_news_embedding = text_to_embedding(new_news).numpy()
    new_news_embedding = np.squeeze(new_news_embedding, axis=0)
    closest_cluster_index = -1  # 默认情况下，将自身视为一个新的簇
    max_similarity = -1
    # 遍历每个簇的中心向量
    for i, cluster_center in enumerate(cluster_centers):
        # 计算新闻与簇中心之间的余弦相似度
        similarity = cosine_similarity([new_news_embedding], [cluster_center])[0][0]
        # 如果相似度大于之前记录的最大相似度值，则更新最大相似度值和最接近的簇索引
        if similarity > max_similarity:
            max_similarity = similarity
            closest_cluster_index = i
    # print(max_similarity)
    # 检查最大相似度值是否大于阈值，如果大于阈值，则将新闻归属到最接近的簇
    if max_similarity > threshold:
        return closest_cluster_index
    else:
        return -1  # 如果最大相似度值不大于阈值，则将新闻视为一个新的簇


def text_to_embedding(text, bert_name='acge_text_embedding', layer=-1):
    # 加载预训练的BERT模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
    model = AutoModel.from_pretrained(bert_name)
    # 文本编码
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    # 获取模型输出
    with torch.no_grad():
        outputs = model(**inputs)
    # 提取所需层的输出作为嵌入向量
    embedding = outputs.last_hidden_state[:, layer, :]  # 取最后一层的输出作为嵌入向量
    return embedding

def generate_event_title(news):
    # 创建 OpenAI 客户端
    client = OpenAI(
        base_url="https://api.xiaoai.plus/v1",
        api_key="sk-NFxr7dzBKJT5f0vM6f717eFb23924aB4Af2d1e1bB3604bCc",
    )
    # 将新闻内容转换为字符串
    user_input = "请你为以下新闻组成的事件生成一个事件标题，只根据给出的信息" + "。" + "。".join(news)
    # 发送请求生成事件标题
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                ],
            }
        ]
    )
    # 提取生成的事件标题
    event_title = response.choices[0].message.content
    return event_title

csv_file_path = '中山大学腾讯网.csv'  #更改这里选文件
news_list = extract_news(csv_file_path)
print(news_list[3])

input_ids, attention_masks = tokenize(news_list)
print(input_ids[3])
print(input_ids.shape)

labels, cluster_centers = cluster_news(input_ids, attention_masks)
print("Cluster Labels:", labels)
print("Cluster Centers:", len(cluster_centers))

new_news = '最新！中山大学林天歆教授、黄健教授联合发文：发现癌症免疫治疗靶向候选者'
cluster_index = find_nearest_cluster(new_news, cluster_centers)
print(cluster_index)

display_clustered_news(news_list, labels)


# # 测试函数
# news = ["林斌是小米的联合创始人", "小米是一家知名的科技公司"]
# event_title = generate_event_title(news)
# print("Generated Event Title:", event_title)

