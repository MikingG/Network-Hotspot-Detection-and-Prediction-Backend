from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models
import pandas as pd
import time


# 请替换以下为您的腾讯云API密钥ID和密钥，用的时候记得填
# SECRET_ID = ""
# SECRET_KEY = ""

# 实例化一个认证对象
cred = credential.Credential(SECRET_ID, SECRET_KEY)

# 实例化要请求产品的client对象, TMT的region固定为ap-guangzhou
client = tmt_client.TmtClient(cred, "ap-guangzhou")

# 读取csv文件
df = pd.read_csv('data/tiktok/tiktok_中山大学_description.csv')  # 请替换为你的输入文件名

def translate_text(text, index, column_name='title'):
    try:
        # 添加ProjectId到请求对象中，确保其为int64类型
        req = models.TextTranslateRequest()
        req.ProjectId = int(0)
        req.SourceText = text
        req.Source = "zh"
        req.Target = "en"
        
        # 发起请求
        resp = client.TextTranslate(req)
        translated_text = resp.TargetText
        print(f"翻译第{index}条记录的'{column_name}'成功")
        return translated_text
    except Exception as e:
        print(f"翻译第{index}条记录的'{column_name}'错误: {e}")
        return text  # 如果翻译失败，保留原文
    
    finally:
        # 为了遵守每秒5次请求的限制，简单地在每次请求后暂停0.2秒
        time.sleep(0.2)  # 这个延时可以根据实际情况调整


# 使用apply函数时传递索引，以便在翻译后打印信息
df['title_en'] = df.apply(lambda row: translate_text(row['title'], row.name), axis=1)

# 保存到新的csv文件
df.to_csv('data/tiktok/tiktok_中山大学_description_translated.csv', index=False)  # 请替换为你希望的输出文件名