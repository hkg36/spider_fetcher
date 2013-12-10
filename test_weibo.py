import weibo_tools
import os
import json
import random

weibo_tools.UseRandomLocalAddress()
os.remove('data/weibo_oauths.db')
client=weibo_tools.DefaultWeiboClient()
fun=getattr(client,u'statuses__public_timeline')
res=fun()
print res
res=client.post.statuses__update(status="hello all"+str(random.randint(0,1000)))
print res
res=json.loads(res)
res=client.post.statuses__destroy(id=res['id'])
print res