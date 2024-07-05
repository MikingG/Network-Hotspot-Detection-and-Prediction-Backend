from TuGraphClient import TuGraphClient
import json
import ollama
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import logging
from GPT import askgpt
import re
from transformers import AutoTokenizer, AutoModel
from sklearn.cluster import DBSCAN
import torch


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

def entity_cluster_test(client):
    cypher = "MATCH (n:实体)-[]->(:抽象实体) RETURN n.entityID"
    except_entity_list = client.call_cypher(cypher)
    except_entity_list = except_entity_list['result']
    cypher = f"MATCH (n:实体) WHERE NOT n.entityID IN [{str.join(',',[f"'{e[0]}'" for e in except_entity_list])}] RETURN n.entityID,n.name,n.description,n.entityType"
    entity_list = client.call_cypher(cypher)
    entity_list = entity_list['result']
    print(f'正在处理实体数量: {len(entity_list)}')
    embeddings = []
    for event in entity_list:
        embeddings.append(getEmbedding(str(event)))
    for i in range(10,12):
        print("------------------------------------")
        print(f'正在处理聚类eps={i}')
        labels = cluster_news1(embeddings,eps=i)
        print(f'聚类结果数量: {len(labels)}')
        cluster_entities = {}
        for entity, label in zip(entity_list, labels):
            if label not in cluster_entities:
                cluster_entities[label] = []
            cluster_entities[label].append(entity)
        for index,item in cluster_entities.items():
            print(index,f"实体数量{len(item)} ",[e[1] for e in item])
        print("------------------------------------")

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
            model="qwen2:7b",
            prompt=text,
            format="json",
            options={
                "temperature": 0.0,
                "top_p": 1.0,
            }
        )
    return res['response']

def merge_event(client):
    '''
    这个函数用来将同一个事件指向同一个抽象事件节点
    '''
    cypher = "MATCH (n:事件)-[]->(:抽象事件) RETURN n.eventID"
    except_event_list = client.call_cypher(cypher)
    except_event_list = except_event_list['result']
    cypher = f"MATCH (n:事件) WHERE NOT n.eventID IN [{str.join(',',[f"'{e[0]}'" for e in except_event_list])}] RETURN n.eventID,n.description,n.name,n.startDate"
    event_list = client.call_cypher(cypher)
    event_list = event_list['result']
    
    labels = cluster_news(event_list)
    cluster_events = {}
    for event, label in zip(event_list, labels):
        if label not in cluster_events:
            cluster_events[label] = []
        cluster_events[label].append(event)
    with open("prompt1.txt", 'r', encoding='utf-8') as f:
        origin_prompt = f.read()
    for label, events in cluster_events.items():
        print(f'事件簇{label}包含的事件数量: {len(events)}')
        prompt = origin_prompt.replace("<事件列表>", str([{"事件描述": event[1], "事件名": event[2], "开始日期": event[3]} for event in events]))
        answer = getExtraJson(prompt,'ollama')
        # 创建抽象事件节点
        try:
            if answer['eventDate'] != "null" and answer['eventDate'] is not None:
                cypher = f"CREATE (:抽象事件 {{name:'{answer['eventName']}',description:'{answer['eventSummary'].replace("'","\'").replace('"','\"')}',docNum:{len(events)},date:'{answer['eventDate']}'}})"
            else:
                cypher = f"CREATE (:抽象事件 {{name:'{answer['eventName']}',description:'{answer['eventSummary'].replace("'","\'").replace('"','\"')}',docNum:{len(events)}}})"
            client.call_cypher(cypher)
        except Exception as e:
            print(f'抽象事件节点创建失败: {answer}')
            print(e)
            continue
        # 将同一事件蔟的事件指向同一个抽象事件节点
        for event in events:
            source_id = event[0]
            cypher = (
                "MATCH (source:事件 {eventID: '"
                + source_id
                + "'}), (target:抽象事件 {name: '"
                + answer['eventName']
                + "'}) CREATE (source)-[:属于]->(target)"
            )
            client.call_cypher(cypher)

def merge_entity(client):
    '''
    这个函数用来将同一个实体指向同一个实体节点
    '''
    cypher = "MATCH (n:实体)-[]->(:抽象实体) RETURN n.entityID"
    except_entity_list = client.call_cypher(cypher)
    except_entity_list = except_entity_list['result']
    cypher = f"MATCH (n:实体) WHERE NOT n.entityID IN [{str.join(',',[f"'{e[0]}'" for e in except_entity_list])}] RETURN n.entityID,n.name,n.description,n.entityType"
    entity_list = client.call_cypher(cypher)
    entity_list = entity_list['result']
    print(f'正在处理实体数量: {len(entity_list)}')
    labels = cluster_news(entity_list,eps=10) # 实体聚类eps=10 的时候效果比较好
    cluster_entities = {}
    for entity, label in zip(entity_list, labels):
        if label not in cluster_entities:
            cluster_entities[label] = []
        cluster_entities[label].append(entity)
    print(f'实体簇数量: {len(cluster_entities)}')
    with open("prompt2.txt", 'r', encoding='utf-8') as f:
        origin_prompt = f.read()
        
    for label, entities in cluster_entities.items():
        print(f'实体簇{label}包含的实体数量: {len(entities)}')
        prompt = origin_prompt.replace("<实体列表>", str([{"实体描述": entity[1], "实体名": entity[2],"实体类型": entity[3]} for entity in entities]))
        answer = getExtraJson(prompt,'ollama')
        try:
            # 创建抽象实体节点
            if answer['entityType'] is not None and answer['entityType']!="null":
                cypher = f"CREATE (:抽象实体 {{name:'{answer['entityName']}',description:'{str(answer['entitySummary']).replace("'","").replace('"','')}',entityType:'{answer['entityType']}',docNum:{len(entities)}}})"
            else:
                cypher = f"CREATE (:抽象实体 {{name:'{answer['entityName']}',description:'{str(answer['entitySummary']).replace("'","").replace('"','')}',docNum:{len(entities)}}})"
            client.call_cypher(cypher)
        except Exception as e:
            print(f'抽象实体节点创建失败: {answer}')
            print(e)
            if "index value already exists." not in str(e):
                continue
        # 将同一实体蔟的实体指向同一个抽象实体节点
        for entity in entities:
            source_id = entity[0]
            cypher = (
                "MATCH (source:实体 {entityID: '"
                + source_id
                + "'}), (target:抽象实体 {name: '"
                + answer['entityName']
                + "'}) CREATE (source)-[:属于]->(target)"
            )
            client.call_cypher(cypher)
def cluster_news(event_list, eps=12, min_samples=2):
    embeddings = []
    for event in event_list:
        embeddings.append(getEmbedding(str(event)))
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(embeddings)
    for i, label in enumerate(labels):
        if label == -1:
            labels[i] = max(labels) + 1
    return labels

def cluster_news1(embeddings, eps=12, min_samples=2):
    
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(embeddings)
    for i, label in enumerate(labels):
        if label == -1:
            labels[i] = max(labels) + 1
    return labels

def getEmbedding(text):
    res = ollama.embeddings(
        model="chevalblanc/acge_text_embedding:latest",
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
def extract_json_from_string(string):
    pattern = r"```json\n(.*?)```"
    match = re.search(pattern, string, re.DOTALL)
    if match:
        code = match.group(1)
        return code
    else:
        return None
def main():
    # # 打开csv文件
    # logging.info('开始读取xlsx文件')
    # # df = pd.read_csv('data\中山大学腾讯网.csv', encoding='unicode-escape')
    # df = pd.read_excel('data\中山大学腾讯网.xlsx')
    df = pd.read_csv("data/event_extract_from_腾讯网.csv")
    # logging.info('读取xlsx文件成功:\n'+str(df.head()))
    # # 输出统计数据
    # logging.info('数据统计:\n'+str(df.describe()))
    # 使用TuGraphClient连接数据库
    client = TuGraphClient(
        "127.0.0.1:7070", "admin", "0527", graph="eventgraph1"
    )
    # merge_event(client)
    merge_entity(client)
    # entity_cluster_test(client)
    # with open('prompt.txt', 'r', encoding='utf-8') as f:
    #     origin_prompt = f.read()
    # 遍历每一行
    # for index, row in df.iterrows():
    #     # 这里加str是因为默认会把空的title和content识别成float
    #     title = str(row['title'])
    #     content = str(row['content'])
    #     url = str(row['url'])
    #     json_extra = str(row['answer'])
    #     logging.info(f'正在处理第{index+1}行数据: {title}')
    #     # 创建文档节点
    #     if create_doc_node(client, row) == False:
    #         logging.info(f'跳过第{index+1}行数据: {title}')
    #         continue
        # prompt = origin_prompt.replace('（在此处插入文章内容）', title+'\n'+content+'\n来自:'+url)
        # logging.info(f'正在提取图信息: {title}')
        # json_extra = getExtraJson(prompt)
        # logging.info(f'图信息提取完成: {title}')
        # try:
        #     json_extra = extract_json_from_string(json_extra)
        #     json_extra = json.loads(json_extra)
        # except Exception as e:
        #     logging.error(f'JSON解析失败: {title}')
        #     logging.error(e)
        #     continue
        # logging.info(f'正在创建图: {title}')
        # create_nodes_and_relationships(client, json_extra,url)
        # logging.info(f'图创建完毕: {title}')
    # with open("demodata.json", "r", encoding="utf-8") as f:
    #     json_data = f.read()
    # 解析JSON数据并调用函数创建节点和关系
    # data = json.loads(json_data)  # 确保此处的json_data变量已正确赋值
    # create_nodes_and_relationships(client, data)
    # print("Nodes and relationships created successfully.")


if __name__ == "__main__":
    main()
