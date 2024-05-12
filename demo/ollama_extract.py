import ollama
def getExtraJson(text):
    res = ollama.generate(
        model="qwen:4b",
        prompt=text,
        format="json",
    )
    return res['response']
with open('prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()
title = '中山大学获校友捐赠1亿元'
content = '中山大学今年迎来百岁华诞。17日，中山大学校友伉俪林斌、刘向东向中山大学捐赠1亿元庆祝母校百年华诞。据介绍，林斌、刘向东均为中山大学1986级校友，其中林斌现为小米集团联合创始人、副董事长，刘向东为林斌刘向东基金会理事长。'

prompt = prompt.replace('（在此处插入文章内容）', content)
print(prompt)
print(getExtraJson(prompt))