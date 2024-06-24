import pandas as pd
import json
def csv_to_json(csv_file, json_file):
    # 使用pandas读取CSV文件
    df = pd.read_csv(csv_file)
    # for i in range(len(df)):
    #     # 提取每一行中的代码
    #     code = extract_python_code(df.iloc[i]['origin_answer'])
    #     if code:
    #         # 将提取的代码替换到CSV文件中
    #         df.at[i, 'code'] = code[0].strip()
    # 将DataFrame转换为JSON格式，并写入文件
    df.to_json(json_file, orient='records', force_ascii=False, indent=4) 

def excel_to_json(excel_file, json_file):
    # 使用pandas读取Excel文件
    df = pd.read_excel(excel_file)
    # 将DataFrame转换为JSON格式，并写入文件
    df.to_json(json_file, orient='records', force_ascii=False, indent=4)

def json_to_csv(json_file,df_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_csv(df_file,index=False)

def json_to_excel(json_file,excel_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel(excel_file,index=False)

excel_to_json("data\中山大学腾讯网.xlsx","data\中山大学腾讯网.json")