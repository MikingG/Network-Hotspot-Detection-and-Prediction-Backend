from TuGraphClient import TuGraphClient
import json
import ollama
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import logging
from GPT import askgpt
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
def create_nodes_and_relationships(client, data, url):
    cyphers = []
    # 创建事件节点的Cypher语句
    for event in data["events"]:
        eventID = url+":"+event["@id"]
        name = event["name"]
        description = event.get("description", "")
        startDate = event["startDate"]
        if startDate is None:
            cypher = f"CREATE (:事件 {{eventID: '{eventID}', name: '{name}', description: '{description}'}})"
        else:
            cypher = f"CREATE (:事件 {{eventID: '{eventID}', name: '{name}', description: '{description}', startDate: date('{startDate}')}})"
        cyphers.append(cypher)
        # res = client.call_cypher(cypher)
        # print(res)

    # 创建实体节点的Cypher语句
    for entity in data["entities"]:
        entityID = url+":"+entity["@id"]
        entityType = entity["@type"].split("/")[-1]
        name = entity["name"]
        description = entity.get("description", "")
        cypher = f"CREATE (:实体 {{entityID: '{entityID}', entityType: '{entityType}', name: '{name}', description: '{description}'}})"
        cyphers.append(cypher)
        # res = client.call_cypher(cypher)
        # print(res)
    # 创建关系的Cypher语句
    for relationship in data["relationships"]:
        rel_id = relationship["@id"]
        rel_type = relationship["relationshipType"]
        source_id = url+":"+relationship["source"]
        target_id = url+":"+relationship["target"]
        # 创建事件-实体关系
        if "event" in source_id and "entity" in target_id:
            cypher = (
                "MATCH (source:事件 {eventID: '"
                + source_id
                + "'}), (target:实体 {entityID: '"
                + target_id
                + "'}) CREATE (source)-[:事件_实体{relationshipType:'"
                + rel_type
                + "'}]->(target)"
            )
        # 创建实体-实体关系
        elif "entity" in source_id and "entity" in target_id:
            cypher = (
                "MATCH (source:实体 {entityID: '"
                + source_id
                + "'}), (target:实体 {entityID: '"
                + target_id
                + "'}) CREATE (source)-[:实体_实体{relationshipType:'"
                + rel_type
                + "'}]->(target)"
            )
        # 创建事件-事件关系
        elif "event" in source_id and "event" in target_id:
            cypher = (
                "MATCH (source:事件 {eventID: '"
                + source_id
                + "'}), (target:事件 {eventID: '"
                + target_id
                + "'}) CREATE (source)-[:事件_事件{relationshipType:'"
                + rel_type
                + "'}]->(target)"
            )
        else:
            print("Unknown relationship type:", rel_type)
            continue
        cyphers.append(cypher)
        # cyphers.append(cypher)
        # print(cypher)
        # res = client.call_cypher(cypher)
        # print(res)
    # 所有事件节点和实体节点指向文档节点
    for event in data["events"]:
        eventID = url+":"+event["@id"]
        cypher = f"MATCH (event:事件 {{eventID: '{eventID}'}}),(doc:文档 {{url: '{url}'}}) CREATE (event)-[:来源]->(doc)"
        cyphers.append(cypher)
    for entity in data["entities"]:
        entityID = url+":"+entity["@id"]
        cypher = f"MATCH (entity:实体 {{entityID: '{entityID}'}}),(doc:文档 {{url: '{url}'}}) CREATE (entity)-[:来源]->(doc)"
    # 执行所有Cypher语句
    for cypher in cyphers:
        try:
            res = client.call_cypher(cypher)
            # 打印结果
            print(res)
        except Exception as e:
            print(f"Error executing Cypher: {cypher}")
            print(e)
            continue
def create_doc_node(client, row):
    logging.info(f'正在创建文档节点: {row["title"]}')
    title = row['title']
    content = row['content']
    url = row['url']
    cypher = f"CREATE (:文档 {{title: '{title}', content: '{content}', url: '{url}'}})"
    try:
        client.call_cypher(cypher)
        logging.info(f'文档节点创建成功: {row["title"]}')
        return True
    except Exception as e:
        logging.error(f'文档节点创建失败: {row["title"]}')
        logging.error(e)
        return False
    
def ask_ollama(text):
    res = ollama.generate(
            model="gemma:latest",
            prompt=text,
            format="json",
        )
    return res['response']

def getEmbedding(text):
    res = ollama.embeddings(
        model="mxbai-embed-large",
        prompt=text,
    )
    return res['embedding']

def getExtraJson(text,model='gpt'):
    while True:
        if model == 'gpt':
            res,model = askgpt(text)
        elif model == 'ollama':
            res = ask_ollama(text)
        try:
            json_data = json.loads(res)
            return json_data
        except Exception as e:
            logging.info(f'JSON解析失败: {res['response']}, 正在重试...')
            continue
def main():
    # 打开csv文件
    logging.info('开始读取xlsx文件')
    # df = pd.read_csv('data\中山大学腾讯网.csv', encoding='unicode-escape')
    df = pd.read_excel('data\中山大学腾讯网.xlsx')
    logging.info('读取xlsx文件成功:\n'+str(df.head()))
    # 输出统计数据
    logging.info('数据统计:\n'+str(df.describe()))
    # 使用TuGraphClient连接数据库
    client = TuGraphClient(
        "127.0.0.1:7070", "admin", "0527", graph="eventgraph"
    )
    with open('prompt.txt', 'r', encoding='utf-8') as f:
        origin_prompt = f.read()  
    # 遍历每一行
    for index, row in df.iterrows():
        # 这里加str是因为默认会把空的title和content识别成float
        title = str(row['title'])
        content = str(row['content'])
        url = str(row['url'])
        logging.info(f'正在处理第{index+1}行数据: {title}')
        # 创建文档节点
        if create_doc_node(client, row) == False:
            logging.info(f'跳过第{index+1}行数据: {title}')
            continue
        prompt = origin_prompt.replace('（在此处插入文章内容）', title+'\n'+content+'\n来自:'+url)
        logging.info(f'正在提取图信息: {title}')
        json_extra = getExtraJson(prompt)
        logging.info(f'图信息提取完成: {title}')
        logging.info(f'正在创建图: {title}')
        create_nodes_and_relationships(client, json_extra,url)
        logging.info(f'图创建完毕: {title}')
    # with open("demodata.json", "r", encoding="utf-8") as f:
    #     json_data = f.read()
    # 解析JSON数据并调用函数创建节点和关系
    # data = json.loads(json_data)  # 确保此处的json_data变量已正确赋值
    # create_nodes_and_relationships(client, data)
    # print("Nodes and relationships created successfully.")


if __name__ == "__main__":
    main()
