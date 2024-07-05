from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("admin", "0527")
with GraphDatabase.driver(URI, auth=AUTH) as client:
    session = client.session(database="eventgraph1")
    ret = session.run("match (n:事件) return n")
    for item in ret.data():
        print(item)