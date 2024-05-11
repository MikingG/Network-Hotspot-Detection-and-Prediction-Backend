from neo4j import GraphDatabase
import json

# 请替换为您的Neo4j数据库的URL和认证信息
uri = "bolt://localhost:7687"
user = "admin"
password = "0527"

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_event_node(tx, event_data):
    eventId = event_data["@id"]
    name = event_data["name"]
    description = event_data.get("description", "")
    startDate = event_data["startDate"]
    query = (
        "CREATE (:Event {eventId: $eventId, name: $name, description: $description, startDate: datetime($startDate)})"
    )
    tx.run(query, eventId=eventId, name=name, description=description, startDate=startDate)

def create_entity_node(tx, entity_data):
    entityId = entity_data["@id"]
    entityType = entity_data["@type"].split("/")[-1]
    name = entity_data["name"]
    description = entity_data.get("description", "")
    query = (
        "CREATE (:Entity {entityId: $entityId, entityType: $entityType, name: $name, description: $description})"
    )
    tx.run(query, entityId=entityId, entityType=entityType, name=name, description=description)

def create_relationship(tx, relationship_data):
    rel_id = relationship_data["@id"]
    rel_type = relationship_data["relationshipType"]
    source_id = relationship_data["source"]
    target_id = relationship_data["target"]

    # 根据关系类型选择合适的Cypher查询
    if rel_type == "HasParticipant":
        query = (
            "MATCH (source:Event), (target:Entity) WHERE source.eventId = $source_id AND target.entityId = $target_id "
            "CREATE (source)-[:PARTICIPATES]->(target)"
        )
    elif rel_type == "HasFunding":
        query = (
            "MATCH (source:Event), (target:Entity) WHERE source.eventId = $source_id AND target.entityId = $target_id "
            "CREATE (source)-[:FUNDED_BY]->(target)"
        )
    else:
        print(f"Unknown relationship type: {rel_type}")
        return

    tx.run(query, source_id=source_id, target_id=target_id)

with driver.session() as session:
    data = json.loads(json_data)  # 使用您提供的JSON数据替换这里的json_data变量

    for event in data["events"]:
        session.write_transaction(create_event_node, event)

    for entity in data["entities"]:
        session.write_transaction(create_entity_node, entity)

    for relationship in data["relationships"]:
        session.write_transaction(create_relationship, relationship)

print("Nodes and relationships created successfully.")
driver.close()