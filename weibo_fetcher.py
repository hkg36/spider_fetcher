#-*-coding:utf-8-*-

import weibo_tools
import gzip
from cStringIO import StringIO
import time
import QueueWorker2
import config
import os
import weibo_tools

weibo_tools.USE_PYCURL=False
class WeiboQueueWork(QueueWorker2.QueueWorker):
    def RequestWork(self,params,body):
        APP_KEY=params.get('app_key','2824743419')
        APP_SECRET = params.get('app_secret','9c152c876ec980df305d54196539773f')
        ACCESS_TOKEN=params.get('access_token')
        function_name=params.get('function')
        function_params=params.get('params')
        if not function_name:
            return {'error':5},'need function'
        if not isinstance(function_params,dict):
            function_params={}
        if ACCESS_TOKEN:
            client = weibo_tools.APIClient(app_key=APP_KEY, app_secret=APP_SECRET)
            client.set_access_token(ACCESS_TOKEN,time.time()+10000)
        else:
            client=weibo_tools.DefaultWeiboClient()
        func=getattr(client,function_name)
        for i in xrange(3):
            try:
                resault=func(**function_params)
                buf = StringIO()
                zf = gzip.GzipFile(fileobj=buf,mode='w')
                zf.write(resault)
                zf.close()
                params['zip']=True
                print 'done'
                return params,buf.getvalue()
            except weibo_tools.WeiboRequestFail,e:
                if e.httpcode in {503,502}:
                    print 'error 1 retry'
                    continue
                if e.httpcode in {403} and e.error_data.get('error_code')==10022:
                    time.sleep(30)
                    continue
                return {'error':1,'httpcode':e.httpcode,'weiboerror':e.error_data.get('error_code',0)},str(e)
            except weibo_tools.APIError,e:
                if e.error_code==10022:
                    print 'error 2'
                    return {'error':2,'api_error':e.error_code},str(e)
                if e.isOauthFail():
                    if ACCESS_TOKEN:
                        return {'error':4},'oauth fail'
                    else:
                        try:
                            os.remove('data/weibo_oauths.db')
                        except Exception,e:
                            print e
                print 'error 2 retry'
                continue
            except Exception,e:
                print 'error 3'
                return {'error':3},str(e)
        return {'error':4},'retry out'
if __name__ == '__main__':
    weibo_tools.UseRandomLocalAddress()
    worker=WeiboQueueWork(config.Queue_Server,config.Queue_Port,config.Queue_Path,config.Queue_User,config.Queue_PassWord,'weibo_request',600)
    worker.run()