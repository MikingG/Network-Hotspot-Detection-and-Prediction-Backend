from TuGraphClient import TuGraphClient
client = TuGraphClient("127.0.0.1:7070", "admin", "0527", graph="eventgraph")  # 请替换为实际的图名称
res = client.call_cypher("MATCH (n:事件 {eventID: 'event3'})")
