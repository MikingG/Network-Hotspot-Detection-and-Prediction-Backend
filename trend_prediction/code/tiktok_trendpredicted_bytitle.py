##### Trend Prediction #####

from textblob import TextBlob
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# 修改函数以仅使用标题进行情感分析和预测
def classifiedTextblob(title):
    # 对标题进行情感分析
    polar_title = TextBlob(title).sentiment.polarity
    # 根据情感极性返回分类结果
    return 1 if polar_title > 0 else -1 if polar_title < 0 else 0

def compute(title):
    df = pd.read_csv("./data/USCAGBDEProcessedTextBlob.csv", encoding="ISO-8859-1")
    # 现在我们只关注标题的情感分类，因此删除或调整相关列
    data = df[['title_sent_class', 'label']]
    data = data.dropna()

    sentiment = data['label']
    data = data.drop(columns=['label'])

    # 对标题进行情感分析
    class_title = classifiedTextblob(title)

    d = {'title_sent_class': class_title}
    input_data = pd.DataFrame(data=d, index=[0], columns=data.columns)

    decision_tree = DecisionTreeClassifier()
    decision_tree = decision_tree.fit(data, sentiment)
    prediction = decision_tree.predict(input_data)
    
    # 获取预测的概率而不是类别
    proba = decision_tree.predict_proba(input_data)
    # 获取成为热门视频的概率
    hot_video_proba = proba[0][1]
    print(hot_video_proba)
    
    threshold = 0.5
    is_trending = 'no'
    
    # 根据概率和阈值判断是否成为热门视频
    if hot_video_proba > threshold:
        print("你的视频有很大的可能成为热门视频（100k views)。")
        is_trending = 'yes'
        print(is_trending)
    else:
        print("你的视频成为热门视频的可能性较低。")
        print(is_trending)

    return is_trending, hot_video_proba

###### 批量处理 ######

input_file = 'data/tiktok/tiktok_中山大学_description_translated.csv'
output_file = 'data/tiktok/tiktok_中山大学_trend_predict_by_title_only.csv'

# 读取输入CSV文件
data = pd.read_csv(input_file)

# Replace NaN values with an empty string
data = data.applymap(lambda x: '' if pd.isnull(x) else x)

# 调整apply以适应新的compute函数，只传入title
data[['trend_predict_by_content', 'trending_probability']] = data.apply(lambda row: compute(row['title_en']), axis=1, result_type='expand')

# Save the results to a new CSV file, adjusting columns accordingly
data[['aweme_id', 'trending_probability', 'trend_predict_by_content', 'title']].to_csv(output_file, index=False)





##### Calculate Accuracy #####

import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'data/tiktok/tiktok_中山大学_trend_predict_by_title_only.csv'  # Replace with the actual file path
df = pd.read_csv(file_path)

# Filter the DataFrame based on the given conditions
accurate_predictions = (df['trend_predict_by_content'] == 'yes')

# Calculate the number of accurate predictions
num_accurate_predictions = accurate_predictions.sum()

# Calculate the total number of rows in the DataFrame
total_rows = len(df)

# Calculate the accuracy percentage
accuracy_percentage = (num_accurate_predictions / total_rows) * 100

# Print the results
print(f"Number of accurate predictions: {num_accurate_predictions}")
print(f"Total number of rows: {total_rows}")
print(f"Accuracy percentage: {accuracy_percentage:.2f}%")