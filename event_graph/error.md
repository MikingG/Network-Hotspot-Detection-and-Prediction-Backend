2024年6月25日

昨天在Djiango和Flask都没能成功连接Tugraph数据库并查询结果返回给前端。其中的错误和同步/异步的函数调用有关。搞了三个小时都没有头绪。

现在有两种方案：

方案一：把事件图谱全部移到tugraph-web。

方案二：自己试多几个连接tugraph的方法，或者自己写一个简单的tugraph客户端。

刚刚发现可能是我没有用正确的方法来连接数据库......确实有更好的方法，本身可以与Django集成。[Django 在Python中使用Neo4j开发Web应用|极客教程 (geek-docs.com)](https://geek-docs.com/django/django-questions/804_django_developing_a_web_application_in_python_with_neo4j.html)

（一想到我是xx，一切问题就迎刃而解了）
