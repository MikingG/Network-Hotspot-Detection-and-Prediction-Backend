from flask import Flask, jsonify
import asyncio
from concurrent.futures import ThreadPoolExecutor
from TuGraphClient import TuGraphClient
from neo4j import GraphDatabase
from flask_cors import CORS
app = Flask(__name__)
# client = TuGraphClient("127.0.0.1:7070", "admin", "0527", graph="eventgraph1")
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("admin", "0527")) #认证连接数据库
# async def get_event_list_async():
#     cypher_query = "MATCH (n:抽象事件) RETURN n.name"
#     result = await client.call_cypher(cypher_query)
#     event_list = [{'name': event_name} for event_name in result['result']]
#     return event_list

# executor = ThreadPoolExecutor(1)
CORS(app)
@app.route('/geteventlist')
def get_event_list():
    URI = "bolt://localhost:7687"
    AUTH = ("admin", "0527")
    with GraphDatabase.driver(URI, auth=AUTH) as client:
        session = client.session(database="eventgraph1")
        ret = session.run("match (n:抽象事件) return n")
        event_list = []
        for item in ret.data():
            event_list.append(item['n']['name'])
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': event_list
        })
    # cypher_query = "MATCH (n:抽象事件) RETURN n.name"
    # result = client.call_cypher(cypher_query)
    # event_list = [{'name': event_name} for event_name in result['result']]
    # # Return JSON response
    # return jsonify({
    #     'code': 200,
    #     'message': 'success',
    #     'data': event_list
    # })

if __name__ == '__main__':
    app.run(debug=True)
