from graphviz import Digraph

# 假设你已经解析了JSON数据到变量data
def visualize_graph(data):
    dot = Digraph(comment='Event-Entity Graph')
    
    # 遍历并添加节点
    for entity in data['entities']:
        dot.node(entity['@id'], entity['name'])
    
    # 遍历并添加边
    for relationship in data['relationships']:
        source, target = relationship['source'], relationship['target']
        dot.edge(source, target, label=relationship['relationshipType'])
    
    dot.render('event_entity_graph', view=True)

# 调用函数，传入你的JSON数据
visualize_graph(your_parsed_json_data)