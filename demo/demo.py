import json
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
# JSON数据
# data = {
#   "@context": "http://schema.org",
#   "@type": "EventGraph",
#   "events": [
#     {
#       "@type": "Event",
#       "@id": "event_1",
#       "name": "中山大学百年校庆年首场春茗",
#       "description": "中山大学在香港举办的百年校庆年首场春茗，颁发多项校级荣衔。",
#       "startDate": "2023-04-20",
#       "location": {
#         "@type": "Place",
#         "@id": "place_1",
#         "name": "香港",
#         "description": "春茗活动举办地"
#       },
#       "relationships": {
#         "HasParticipant": ["entity_2", "entity_3", "entity_4"],
#         "LocatedAt": "place_1"
#       }
#     }
#   ],
#   "entities": [
#     {
#       "@type": "Person",
#       "@id": "entity_1",
#       "name": "陈亮",
#       "description": "羊城晚报全媒体记者"
#     },
#     {
#       "@type": "Person",
#       "@id": "entity_2",
#       "name": "陈春声",
#       "description": "中山大学党委书记、中山大学教育发展基金会理事长"
#     },
#     {
#       "@type": "Organization",
#       "@id": "entity_3",
#       "name": "中山大学",
#       "description": "中国著名高等学府，迎来百年华诞"
#     },
#     {
#       "@type": "Organization",
#       "@id": "entity_4",
#       "name": "霍英东基金会",
#       "description": "参与捐赠的基金会"
#     },
#     {
#       "@type": "Place",
#       "@id": "place_1",
#       "name": "香港",
#       "description": "春茗活动举办地"
#     }
#   ],
#   "relationships": [
#     {
#       "@id": "rel_1",
#       "relationshipType": "ReportedBy",
#       "source": "entity_1",
#       "target": "event_1"
#     },
#     {
#       "@id": "rel_2",
#       "relationshipType": "OrganizedBy",
#       "source": "entity_3",
#       "target": "event_1"
#     },
#     {
#       "@id": "rel_3",
#       "relationshipType": "RecipientOfAward",
#       "source": "entity_2",
#       "target": "event_1"
#     },
#     {
#       "@id": "rel_4",
#       "relationshipType": "DonatedTo",
#       "source": "entity_4",
#       "target": "entity_3"
#     }
#   ]
# }
data = {
  "@context": "http://schema.org",
  "@type": "EventGraph",
  "events": [
    {
      "@type": "Event",
      "@id": "event1",
      "name": "中山大学百年校庆年首场春茗",
      "description": "中山大学在香港举办百年校庆年首场春茗活动",
      "startDate": "2023-04-20",
      "location": {
        "@type": "Place",
        "@id": "place1",
        "name": "香港",
        "description": "中山大学在香港举办此次活动"
      },
      "relationships": {
        "HasParticipant": [
          "entity1",
          "entity2",
          "entity3",
          "entity4",
          "entity5"
        ],
        "LocatedAt": "place1"
      }
    },
    {
      "@type": "Event",
      "@id": "event2",
      "name": "中山大学在香港设立高等研究院",
      "description": "中山大学在香港设立高等研究院,加强与香港的合作",
      "startDate": "2023-04-20",
      "location": {
        "@type": "Place",
        "@id": "place1",
        "name": "香港",
        "description": "中山大学在香港设立高等研究院"
      },
      "relationships": {
        "HasParticipant": [
          "entity1",
          "entity6"
        ],
        "LocatedAt": "place1"
      }
    },
    {
      "@type": "Event",
      "@id": "event3",
      "name": "中山大学在青岛举办春茗和荣衔授予仪式",
      "description": "中山大学近期将在青岛举办春茗和荣衔授予仪式",
      "startDate": "2023-04-20",
      "location": {
        "@type": "Place",
        "@id": "place2",
        "name": "青岛",
        "description": "中山大学在青岛举办此次活动"
      },
      "relationships": {
        "HasParticipant": [
          "entity1"
        ],
        "LocatedAt": "place2"
      }
    }
  ],
  "entities": [
    {
      "@type": "Person",
      "@id": "entity1",
      "name": "陈春声",
      "description": "中山大学党委书记、中山大学教育发展基金会理事长"
    },
    {
      "@type": "Person",
      "@id": "entity2",
      "name": "霍英东",
      "description": "爱港爱国人士,多次资助中山大学"
    },
    {
      "@type": "Person",
      "@id": "entity3",
      "name": "伍沾德",
      "description": "爱港爱国人士,多次资助中山大学"
    },
    {
      "@type": "Person",
      "@id": "entity4",
      "name": "曾宪梓",
      "description": "爱港爱国人士,多次资助中山大学"
    },
    {
      "@type": "Person",
      "@id": "entity5",
      "name": "林浩然",
      "description": "中国工程院院士、中山大学生命科学学院教授"
    },
    {
      "@type": "Organization",
      "@id": "entity6",
      "name": "中山大学香港高等研究院",
      "description": "中山大学在香港设立的高等研究院"
    },
    {
      "@type": "Organization",
      "@id": "entity7",
      "name": "中山大学教育发展基金会",
      "description": "中山大学的教育发展基金会"
    },
    {
      "@type": "Organization",
      "@id": "entity8",
      "name": "中山大学深圳校友会",
      "description": "中山大学深圳校友会"
    },
    {
      "@type": "Person",
      "@id": "entity9",
      "name": "陈运河",
      "description": "中山大学校友"
    },
    {
      "@type": "Person",
      "@id": "entity10",
      "name": "刘修婉",
      "description": "中山大学校友"
    },
    {
      "@type": "Person",
      "@id": "entity11",
      "name": "谢锦鹏",
      "description": "捐赠人"
    }
  ],
  "relationships": [
    {
      "@id": "rel1",
      "relationshipType": "HasPosition",
      "source": "entity1",
      "target": "entity7"
    },
    {
      "@id": "rel2",
      "relationshipType": "Donated",
      "source": "entity2",
      "target": "entity1"
    },
    {
      "@id": "rel3",
      "relationshipType": "Donated",
      "source": "entity3",
      "target": "entity1"
    },
    {
      "@id": "rel4",
      "relationshipType": "Donated",
      "source": "entity4",
      "target": "entity1"
    },
    {
      "@id": "rel5",
      "relationshipType": "HasPosition",
      "source": "entity5",
      "target": "entity6"
    },
    {
      "@id": "rel6",
      "relationshipType": "Donated",
      "source": "entity8",
      "target": "entity6"
    },
    {
      "@id": "rel7",
      "relationshipType": "Donated",
      "source": "entity9",
      "target": "entity6"
    },
    {
      "@id": "rel8",
      "relationshipType": "Donated",
      "source": "entity10",
      "target": "entity6"
    },
    {
      "@id": "rel9",
      "relationshipType": "Donated",
      "source": "entity11",
      "target": "entity6"
    }
  ]
}
data = {
  "@context": "http://schema.org",
  "@type": "EventGraph",
  "events": [
    {
      "@type": "Event",
      "@id": "event1",
      "name": "中山大学百年校庆年首场春茗",
      "description": "中山大学在香港举办百年校庆年首场春茗，颁发校级荣衔并举行捐赠仪式。",
      "startDate": "2024-04-20",
      "location": {
        "@type": "Place",
        "@id": "location1",
        "name": "香港",
        "description": "中山大学百年校庆年首场春茗举办地"
      },
      "relationships": {
        "HasParticipant": [
          "entity1",
          "entity2",
          "entity3",
          "entity4",
          "entity5",
          "entity6",
          "entity7",
          "entity8",
          "entity9",
          "entity10",
          "entity11",
          "entity12",
          "entity13",
          "entity14",
          "entity15",
          "entity16",
          "entity17",
          "entity18",
          "entity19",
          "entity20",
          "entity21",
          "entity22",
          "entity23",
          "entity24",
          "entity25",
          "entity26",
          "entity27",
          "entity28",
          "entity29",
          "entity30",
          "entity31",
          "entity32",
          "entity33",
          "entity34",
          "entity35",
          "entity36",
          "entity37",
          "entity38",
          "entity39",
          "entity40"
        ],
        "LocatedAt": "location1"
      }
    },
    {
      "@type": "Event",
      "@id": "event2",
      "name": "中山大学在香港设立高等研究院",
      "description": "中山大学在香港设立高等研究院，加快建设工作并吸引全球顶尖学者。",
      "location": {
        "@type": "Place",
        "@id": "location1",
        "name": "香港",
        "description": "中山大学百年校庆年首场春茗举办地"
      }
    },
    {
      "@type": "Event",
      "@id": "event3",
      "name": "中山大学校级荣衔授予仪式",
      "description": "中山大学在香港举行校级荣衔授予仪式，感谢各界对学校发展的支持。",
      "location": {
        "@type": "Place",
        "@id": "location1",
        "name": "香港",
        "description": "中山大学百年校庆年首场春茗举办地"
      }
    },
    {
      "@type": "Event",
      "@id": "event4",
      "name": "霍英东基金会捐赠仪式",
      "description": "霍英东基金会捐赠支持霍英东体育中心修缮工程启动。",
      "location": {
        "@type": "Place",
        "@id": "location2",
        "name": "未提及",
        "description": "未提及"
      }
    },
    {
      "@type": "Event",
      "@id": "event5",
      "name": "中山大学深圳校友会捐赠仪式",
      "description": "中山大学深圳校友会捐赠设立首笔中山大学香港高等研究院建设基金。",
      "location": {
        "@type": "Place",
        "@id": "location2",
        "name": "未提及",
        "description": "未提及"
      }
    },
    {
      "@type": "Event",
      "@id": "event6",
      "name": "陈运河、刘修婉校友伉俪捐赠仪式",
      "description": "陈运河、刘修婉校友伉俪捐赠饶宗颐先生墨宝。",
      "location": {
        "@type": "Place",
        "@id": "location2",
        "name": "未提及",
        "description": "未提及"
      }
    },
    {
      "@type": "Event",
      "@id": "event7",
      "name": "谢锦鹏先生捐赠仪式",
      "description": "谢锦鹏先生捐赠设立中山大学博物馆贵宾厅装修基金。",
      "location": {
        "@type": "Place",
        "@id": "location2",
        "name": "未提及",
        "description": "未提及"
      }
    }
  ],
  "entities": [
    {
      "@type": "Person",
      "@id": "entity1",
      "name": "陈亮",
      "description": "羊城晚报全媒体记者"
    },
    {
      "@type": "Person",
      "@id": "entity2",
      "name": "李建平",
      "description": "通讯员"
    },
    {
      "@type": "Person",
      "@id": "entity3",
      "name": "林娜",
      "description": "通讯员"
    },
    {
      "@type": "Person",
      "@id": "entity4",
      "name": "陈春声",
      "description": "中山大学党委书记、中山大学教育发展基金会理事长"
    },
    {
      "@type": "Person",
      "@id": "entity5",
      "name": "霍英东",
      "description": "爱港爱国人士"
    },
    {
      "@type": "Person",
      "@id": "entity6",
      "name": "伍沾德",
      "description": "爱港爱国人士"
    },
    {
      "@type": "Person",
      "@id": "entity7",
      "name": "曾宪梓",
      "description": "爱港爱国人士"
    },
    {
      "@type": "Person",
      "@id": "entity8",
      "name": "林浩然",
      "description": "中国工程院院士、中山大学生命科学学院教授"
    },
    {
      "@type": "Person",
      "@id": "entity9",
      "name": "陈运河",
      "description": "校友"
    },
    {
      "@type": "Person",
      "@id": "entity10",
      "name": "刘修婉",
      "description": "校友"
    },
    {
      "@type": "Person",
      "@id": "entity11",
      "name": "谢锦鹏",
      "description": "先生"
    },
    {
      "@type": "Organization",
      "@id": "entity12",
      "name": "中山大学"
    },
    {
      "@type": "Organization",
      "@id": "entity13",
      "name": "中山大学教育发展基金会"
    },
    {
      "@type": "Organization",
      "@id": "entity14",
      "name": "香港高等研究院"
    },
    {
      "@type": "Organization",
      "@id": "entity15",
      "name": "霍英东基金会"
    },
    {
      "@type": "Organization",
      "@id": "entity16",
      "name": "中山大学深圳校友会"
    },
    {
      "@type": "Organization",
      "@id": "entity17",
      "name": "羊城晚报"
    }
  ],
  "relationships": [
    {
      "@id": "relation1",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity1"
    },
    {
      "@id": "relation2",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity2"
    },
    {
      "@id": "relation3",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity3"
    },
    {
      "@id": "relation4",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity4"
    },
    {
      "@id": "relation5",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity5"
    },
    {
      "@id": "relation6",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity6"
    },
    {
      "@id": "relation7",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity7"
    },
    {
      "@id": "relation8",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity8"
    },
    {
      "@id": "relation9",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity9"
    },
    {
      "@id": "relation10",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity10"
    },
    {
      "@id": "relation11",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity11"
    },
    {
      "@id": "relation12",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity12"
    },
    {
      "@id": "relation13",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity13"
    },
    {
      "@id": "relation14",
      "relationshipType": "HasParticipant",
      "source": "event1",
      "target": "entity14"
    },
    {
      "@id": "relation15",
      "relationshipType": "HasParticipant",
      "source": "event4",
      "target": "entity15"
    },
    {
      "@id": "relation16",
      "relationshipType": "HasParticipant",
      "source": "event5",
      "target": "entity16"
    },
    {
      "@id": "relation17",
      "relationshipType": "HasParticipant",
      "source": "event6",
      "target": "entity9"
    },
    {
      "@id": "relation18",
      "relationshipType": "HasParticipant",
      "source": "event6",
      "target": "entity10"
    },
    {
      "@id": "relation19",
      "relationshipType": "HasParticipant",
      "source": "event7",
      "target": "entity11"
    }
  ]
}

# 创建一个空的有向图
G = nx.DiGraph()

# 添加实体和事件作为节点
for entity in data['entities']:
    G.add_node(entity['@id'], label=entity['name'])

for event in data['events']:
    G.add_node(event['@id'], label=event['name'])

# 添加关系作为边
for relationship in data['relationships']:
    G.add_edge(relationship['source'], relationship['target'], label=relationship['relationshipType'])

# 画出图
pos = nx.spring_layout(G)
node_labels = nx.get_node_attributes(G, 'label')
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx(G, pos, labels=node_labels, with_labels=True, node_color='skyblue', edge_color='r', node_size=1500, alpha=.7, arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
