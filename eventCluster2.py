from openai import OpenAI
from transformers import AutoTokenizer, AutoModel
from sklearn.cluster import DBSCAN
import torch
import csv
import numpy as np
import pandas as pd
import jieba
import jieba.posseg as pseg
from collections import Counter


def extract_news(csv_file_path):
    df = pd.read_csv(csv_file_path, encoding='GBK')
    column_list = []
    if csv_file_path == '中山大学腾讯网.csv':
        for index, row in df.iterrows():
            combined_value = row.iloc[0] if pd.isna(row.iloc[1]) else f"{row.iloc[0]}。{row.iloc[1]}"
            column_list.append(combined_value)
    return column_list


def tokenize(news_list, bert_name='acge_text_embedding', max_length=256):
    tokenizer = AutoTokenizer.from_pretrained(bert_name)
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
    model = AutoModel.from_pretrained('acge_text_embedding')
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)
        embeddings = outputs[0][:, 0, :].numpy()
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(embeddings)
    for i, label in enumerate(labels):
        if label == -1:
            labels[i] = max(labels) + 1
    return labels


def generate_event_cate(news):
    predefined_categories = [
        "学校历史与排名", "校友捐赠与荣誉", "校庆活动",
        "学术合作", "学术研究与发现", "人物与纪念",
        "学生与教育", "校园生活与文化", "社会服务与培训"
    ]
    client = OpenAI(
        base_url="https://api.xiaoai.plus/v1",
        api_key="sk-NFxr7dzBKJT5f0vM6f717eFb23924aB4Af2d1e1bB3604bCc",
    )
    user_input = (
            "请你为以下新闻组成的事件生成一个事件类别，类别仅限于以下9个主题之一："
            "学校历史与排名、校友捐赠与荣誉、校庆活动、学术合作、学术研究与发现、"
            "人物与纪念、学生与教育、校园生活与文化、社会服务与培训。如果都不是，请划入“其他”类别。"
            + "。" + "。".join(news)
    )
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
    event_cate = response.choices[0].message.content.strip()
    if event_cate not in predefined_categories:
        event_cate = "其他"
    return event_cate


def generate_event_title(news):
    client = OpenAI(
        base_url="https://api.xiaoai.plus/v1",
        api_key="sk-NFxr7dzBKJT5f0vM6f717eFb23924aB4Af2d1e1bB3604bCc",
    )
    user_input = "请你为以下新闻组成的事件生成一个事件标题，只根据给出的信息" + "。" + "。".join(news)
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
    event_title = response.choices[0].message.content
    return event_title


def display_clustered_news(news_list, labels):
    clustered_news = {}
    key_info = []

    for news, label in zip(news_list, labels):
        if label not in clustered_news:
            clustered_news[label] = []
        clustered_news[label].append(news)

    for label, news in clustered_news.items():
        hotspot_info = {}
        hotspot_info["Hotspot"] = label
        news_count = len(news)
        hotspot_info["Number of news items"] = news_count
        event_title = generate_event_title(news)
        hotspot_info["Event Title"] = event_title
        event_cate = generate_event_cate(news)
        hotspot_info["Event Category"] = event_cate

        key_info.append(hotspot_info)

        print(f"Hotspot {label}:")
        print(f"Number of news items: {news_count}")
        print("Event Title:", event_title)
        print("Event Category:", event_cate)
        for item in news:
            print(item)
        print("")
    key_info_sorted = sorted(key_info, key=lambda x: x['Hotspot'])
    return key_info_sorted


def extract_word_frequencies(news_list):
    stop_words = set()
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip())
    meaningful_pos = {'n', 'v', 'vd', 'vn', 'ns', 'nr', 'nt', 'eng'}
    jieba.setLogLevel(jieba.logging.INFO)
    word_counts = Counter()
    for news in news_list:
        words = pseg.lcut(news)
        for word, flag in words:
            if word not in stop_words and flag in meaningful_pos:
                word_counts.update([word])
    return word_counts


def save_to_csv(data, file_path, fieldnames=None):
    """
    将数据保存到 CSV 文件中

    Args:
        data (list or dict): 要保存的数据，可以是列表或字典形式
        file_path (str): 文件路径
        fieldnames (list): 字段名称列表，仅当 data 是字典列表时需要提供
    """
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        if isinstance(data, list):
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        elif isinstance(data, dict):
            writer = csv.writer(f)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        else:
            raise ValueError("Unsupported data type. Please provide data as a list or dict.")


csv_file_path = '中山大学腾讯网.csv'
news_list = extract_news(csv_file_path)

word_frequencies = extract_word_frequencies(news_list)
print("Word Frequencies:", word_frequencies)

input_ids, attention_masks = tokenize(news_list)
labels = cluster_news(input_ids, attention_masks)

key_info = display_clustered_news(news_list, labels)

save_to_csv(dict(word_frequencies), 'word_frequencies.csv', fieldnames=['Word', 'Frequency'])
save_to_csv(key_info, 'key_info.csv', fieldnames=['Hotspot', 'Number of news items', 'Event Title', 'Event Category'])



# # 测试函数
# news = ["林斌是小米的联合创始人", "小米是一家知名的科技公司"]
# event_title = generate_event_title(news)
# print("Generated Event Title:", event_title)
