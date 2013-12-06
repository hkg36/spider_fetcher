#-*-coding:utf-8-*-
import config
import http_tool_box
import gzip
from cStringIO import StringIO
import time
import QueueWorker2

class HttpQueueWork(QueueWorker2.QueueWorker):
    def RequestWork(self,params,body):
        url=params.get('url')
        if len(url)==0:
            return {'error':'no url'},''
        try:
            code,body,headers=http_tool_box.getHttpBody(url,params.get('ref'),params.get('content_type'),body,params.get('cookie'))
            buf = StringIO()
            zf = gzip.GzipFile(fileobj=buf,mode='w')
            zf.write(body)
            zf.close()
            print 'fetched %s'%url
            params['zip']=True
            params['httpcode']=code
            if 'set-cookie' in headers:
                params['set_cookie']=headers.get('set-cookie')
            return params,buf.getvalue()
        except Exception,e:
            return {'error':str(e)},"fail"

if __name__ == '__main__':
    http_tool_box.UseRandomLocalAddress()
    worker=HttpQueueWork(config.Queue_Server,config.Queue_Port,config.Queue_Path,config.Queue_User,config.Queue_PassWord,'net_request',600)
    worker.run()