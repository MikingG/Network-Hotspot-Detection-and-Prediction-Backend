from TuGraphClient import TuGraphClient
import json
def create_nodes_and_relationships(client, data):
    cyphers = []

    # 创建事件节点的Cypher语句
    for event in data["events"]:
        eventID = event["@id"]
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
        eventID = entity["@id"]
        entityType = entity["@type"].split("/")[-1]
        name = entity["name"]
        description = entity.get("description", "")
        cypher = f"CREATE (:实体 {{entityID: '{eventID}', entityType: '{entityType}', name: '{name}', description: '{description}'}})"
        cyphers.append(cypher)
        # res = client.call_cypher(cypher)
        # print(res)
    # 创建关系的Cypher语句
    for relationship in data["relationships"]:
        rel_id = relationship["@id"]
        rel_type = relationship["relationshipType"]
        source_id = relationship["source"]
        target_id = relationship["target"]
        # 创建事件-实体关系
        if 'event' in  source_id and 'entity' in target_id:
            cypher = 'MATCH (source:事件 {eventID: \'' + source_id + '\'}), (target:实体 {entityID: \'' + target_id + '\'}) CREATE (source)-[:事件_实体{relationshipType:\''+rel_type+'\'}]->(target)'
        # 创建实体-实体关系
        elif 'entity' in source_id and 'entity' in target_id:
            cypher = 'MATCH (source:实体 {entityID: \'' + source_id + '\'}), (target:实体 {entityID: \'' + target_id + '\'}) CREATE (source)-[:实体_实体{relationshipType:\''+rel_type+'\'}]->(target)'
        # 创建事件-事件关系
        elif 'event' in source_id and 'event' in target_id:
            cypher = 'MATCH (source:事件 {eventID: \'' + source_id + '\'}), (target:事件 {eventID: \'' + target_id + '\'}) CREATE (source)-[:事件_事件{relationshipType:\''+rel_type+'\'}]->(target)'
        else:
            print('Unknown relationship type:', rel_type)
            continue
        cyphers.append(cypher)
        # cyphers.append(cypher)
        # print(cypher)
        # res = client.call_cypher(cypher)
        # print(res)
    #执行所有Cypher语句
    for cypher in cyphers:
        try:
            res = client.call_cypher(cypher)
             # 打印结果
            print(res)
        except Exception as e:
            print(f"Error executing Cypher: {cypher}")
            print(e)
            continue

   


# 使用TuGraphClient连接数据库
client = TuGraphClient("127.0.0.1:7070", "admin", "0527", graph="eventgraph")  # 请替换为实际的图名称
with open("demodata.json", "r", encoding="utf-8") as f:
    json_data = f.read()
# 解析JSON数据并调用函数创建节点和关系
data = json.loads(json_data)  # 确保此处的json_data变量已正确赋值
create_nodes_and_relationships(client, data)
print("Nodes and relationships created successfully.")