#-*-coding:utf-8-*-
import config
import pika
import gzip
from cStringIO import StringIO
import time
import bson
class A(object):
    attrs=(('sss',bool),)
    def __init__(self,**kwargs):
        pass
if __name__ == '__main__':
    p=A(sss=False)
    res=bson.BSON.encode({u'tt':True,u'pp':[12,u'ok']})
    ok=bson.BSON(res)
    res=ok.decode()
    cred = pika.PlainCredentials(config.Queue_User,config.Queue_PassWord)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.Queue_Server,
                                                                       port=config.Queue_Port,
                                                                       virtual_host=config.Queue_Path,
                                                                       credentials=cred,
                                                                       heartbeat_interval=20))
    channel = connection.channel()


    result = channel.queue_declare(exclusive=True)
    callback_queue = result.method.queue


    queue_name='net_request'
    channel.queue_declare(queue=queue_name,durable=True)
    properties=pika.BasicProperties(delivery_mode = 2,headers={'type':'http','url':'http://www.baidu.com'},reply_to = callback_queue)
    channel.basic_publish(exchange='',routing_key=queue_name,body='',properties=properties)

    properties=pika.BasicProperties(delivery_mode = 2,headers={'type':'http',
                                                               'url':'http://reg.taobao.com/member/newRegister.jhtml?tg=&&rdn=&timearg=0&tt=0',
                                                               'ref':'http://reg.taobao.com/member/new_register.jhtml?spm=1.1000386.5982201.2.kd3xp1&from=tbtop&ex_info=&ex_sign=',
                                                               'content_type':'application/x-www-form-urlencoded'},reply_to = callback_queue)
    channel.basic_publish(exchange='',routing_key=queue_name,body='ua=205u5ObXObBitH2MRY%2BxNzEXDS85HzknNTzKfM%3D%7CuKBnf0c%2FZ18HTydfx7%2Bnv2U%3D%7CuZFW7MuiORVOJd5SdbKVvZWydVIos1gT6JSoj1WP%7CvoZB%2B2Mb3NQTCzMrA8S8xPw7I0tDS4wUHBTTy6Oro2TshIxWjA%3D%3D%7Cvzfw1%2FAq%7CvCTjxOM5%7CvaW9esDnbCBsYMg%2FyOS%2FxCNvdI%2Bkv0SjmGO4T5TPFD9kSL9UD3OJpf6FHiJuNRn%2BVd6SSYJ6RkqRSVG2rqaupp4WfpnBWdH50dnBJg7pUhkhraG53rWZYrlhLQZKsb3agQ33bIfsF8%2Bo83%2BFuSJZsmpNiq0maiYqgnWC%2FoL%2BGVVOtZ6FfpmiWYJ1UohS%7CsqqCRWJFnw%3D%3D%7Cs6sz9E5GgamxqW52PvneqW52sZkOuTJa7dGJDnlehF4%3D%7CsKiQV%2B3KsCvAi3AMMDdPaK%2BI8muChZ2FQsoNhY2FQtqStW%2B1%7CsamhZkH705uTGyPkLgkRKVEZMRkhSTF5YSkh7eUCOhIaAoqSiuKKAnoiGoLKsnhfmIBafac%3D%7Ctu4pk7Qd5w6VrhUy9U93D5dQeGB4omVtqo2qbQVtNQ3XDQ%3D%3D%7Ct88IspU8xi%2B0jzQT1MwLYwtTC9EL%7CtNwboYYv1TynnCcAx68n4OgvVx9XH8Uf%7Ctd0aoIcu1D2mnSYBxk5WkZleJk4mXoRe%7CqsIFv5gxyyK5gjke2VEp7uYhWTFJUYtR%7Cq8MEvpkwyiO4gzgf2LAo7%2BcgqLDI0ArQ%7CqMAHvZozySC7gDsc21Mr7OQjq5MbY7lj%7CqcEGvJsyyCG6gTod2lJKjYVCyvJqMugy%7CrsYBu5w1zya9hj0a3bUt6uIlrfW91Q%2FV%7Cr8cAup00zie8hzwb3FRMi4NEzLScpH6k%7CrMQDuZ43zSS%2FhD8Y37cv6OAnrye%2Fl02X%7CrcUCuJ82zCW%2BhT4Z3lZOiYFG3taetmy2%7Covo9h6AJ8%2FmFzukulKzEjEtjGyP5Pjbx1vE2rpb%2BZrxm%7Co9scpoEo0jugmyAHwMgPl6%2FX7zXv%7CoNgfpYIr0dun7MsMFNNLcwtTiVM%3D%7CoekulLOUU2sja6yUjNQTCyO783uhew%3D%3D%7Cpv45g6QN992GjPC7nFvh2ZGZXmZOxhzb0xQzFNPL88vzyxHL%7Cp98YooUs1tyg68wLA8Tc5NzkvGa8%7CpNwboYYv1f%2BkrtKZvnlhpr6GvobuNO4%3D%7Cpf06gKcO9P6Cye4pk6vj%2BzwUfESeWVGWsZZRSRFJAYlTiQ%3D%3D%7CmuIln7gR68GakOyngEdPiJDIkNhAmkA%3D%7Cm%2BMknrkQ6uCc1%2FA3L%2BjwqPCosGqw%7CmNAXrYoj2fOoot6VsnVNBT36wvqydV1FfWX9J%2F0%3D%7CmcEGvJsyyPEKQRo9%2BkBo8KhvV9%2FHHdrSFTIV0vrC2kJqsGo%3D%7CnuYhm7wV7%2BWZ0vUyOv3V7fVt5T%2Fl%7Cn%2Bcgmr0U7tcsZzwb3MQDKxM7M3uhew%3D%3D%7CnMQDuZ43zce78NcQqpLKklV9FZ1HgIhPaE%2BIoOhgOADaAA%3D%3D%7CneUimL8W7NUuZT4Z3tYROXH5ofkj%2BQ%3D%3D%7Cktodp4CnYFhQyA83fyfgyEAYUEiSSA%3D%3D%7Ck8sMtpE4wuizucWOqW7U7MTcGyMbM%2BkuJuHG4SYOlq6GvmS%2B%7CkNgfpYIr0egTWAMk49vD6ywUnATDi8PLw7thuw%3D%3D%7CkckOtJM6wPkCSRI18khwaECHvzdfhUJKjaqNSgJKYuryKPI%3D%7Clv45g6QN9841fiUCxU0l4uotdX01HWW%2FZQ%3D%3D%7Cl%2F84gqUM9s80fyQDxEwk4%2BssdHwUPGS%2BZA%3D%3D%7ClPw7gaYP9cw3fCcAx08n4Ogvd3%2F335dNlw%3D%3D%7Clf06gKcO9M02fSYBxk4m4ekudm5mLrZstg%3D%3D%7CitIVr4ivaNLq4rp9NS1lv3hwt5C3cChgaPB4ong%3D%7Ci9MUrokg2uMYUwgv6FJqcmqtlR2VT4iAR2BHgNiw6JCocqg%3D%7CiOAnnboT6dArYDsc26P7PDTzqzNbA2uxaw%3D%3D%7CieEmnLsS6NEqYTod2oKqbWWi%2BmLq0vog%2Bg%3D%3D%7CjuYhm7wV79YtZj0a3bXdGhLVvaXdxU2XTQ%3D%3D%7Cj%2Bcgmr0U7tcsZzwb3ISMS0OE7PR85JxGnA%3D%3D%7CjMQDuZ43zee8tsqBy1Bce7zUnPQzCzO7fBQsVGxkvmQ%3D%7CjcUCuJ82zOWpQmtwTNfsdZ71DmecsGtMi7Obg0QMZCzrk4sTG2O5Yw%3D%3D%7Cgtodp4Ap0%2Fq2XXRvU8jzaoHqEXiDr3RTlC4WPnax%2BaHZA8TMCywLzLSctJyUTpQ%3D%7Cg9scpoEo0usQWwAn4FpiagLF%2FXV9p2Bor4ivaOC4sPjAGsA%3D%7CgOgvlbIb4dgjaDMU07sj5Owroyszq%2FMp8w%3D%3D%7CgekulLMa4NkiaTIV0oqiZW2qMjpSSjLoMg%3D%3D%7Chu4pk7Qd594lbjUS1a2FQkqNFQ0VjcUfxQ%3D%3D%7Ch%2B8okrUc5t8kbzQT1Lw08%2Fs8pLwkHIRehA%3D%3D%7ChMwLsZaxdj6m7ikReXG2LgZOZv4k%2Fg%3D%3D%7Chd0aoIcu1P2xWnNoVM%2F0bYbtFn%2BEqHNUkykRWdEWXhaeRIOLTGtMixNbY1sj%2BSM%3D%7C%2BrK6snV9upJVPfqSml0lTYqSitIVDTVNirLq0hUNZW2qMjr95a1qUirtxf06Ejr91c0KIirt9W2qsjr95Z1aQirt9a1qcjr91RI6YqWNxQLVzcUC1f06EgrN5e0q%2FaVievI1LVWSRV0l4jWtanI6%2FeXdGs3V%2FToiOv0qAjr9KjJqrXpSCs0aAnq9ahLVAopNmgLFEgoCxRI6EtUCKhLVAhoi5TIqYqVyajL1IjpSlUJ6AsUSKqJlsoqCRZKqsnWiipJVgqqCRZK6gkWSuvI14qryNeLaong%3D&_tb_token_=8k31pXaVOQm&CtrlVersion=1%2C0%2C0%2C7&tid=&userFrom=http%3A%2F%2Freg.taobao.com%2Fmember%2Fnew_register.jhtml&agreement=1&action=new_register_action&event_submit_do_register_user=anything&_fm.n._0.a=&refuser=&appendinfo=&regcheck=regcheck&jversion=&jversiondo=&hr=Z0M1Q3RzNzZ0cnVl&tips=&disable=&tt=&calculate=&oslanguage=zh-CN&sr=1600*900&osVer=windows%7C6.1&naviVer=firefox%7C22&_fm.n._0.y=&_fm.n._0.d=&TPL_redirect_url=&redirect_url_name=&_fm.n._0.n=dqwewqeqeq&_fm.n._0.p=123456ok&_fm.n._0.c=123456ok&lqrLHMBVCuNE71AAlYZLpTU%2Fi0jyuN10XH%2BLXCX2h9kopQKVGksjUK9SPTuRuvCrUlLIMTHuViqDh7DFHg%3D%3D=e4hd&CtrlVersion=2%2C1%2C2%2C1&tid=&_fm.n._0.q=&_fm.n._0.qu=&_fm.n._0.qui=&_fm.n._0.quic=&_fm.n._0.quick=&_fm.n._0.pa=2&randomName=&focusCount=&keyupCount=',properties=properties)

    """
    queue_name='weibo_request'
    channel.queue_declare(queue=queue_name,durable=True)
    properties=pika.BasicProperties(delivery_mode = 2,headers={'app_key':'2824743419', #app_key app_secret 可以省略
                                                               'app_secret':'9c152c876ec980df305d54196539773f',
                                                               'access_token':'2.00Iya8SCjn1KFDd12d85ec9cgps2qB', #这个必须和app_key配套
                                                               #app_key  app_secret access_token 可以全部省略，默认用现场+抓取
                                                               'function':'statuses__user_timeline','params':{'uid':"1931386177"}},reply_to = callback_queue)
    channel.basic_publish(exchange='',routing_key=queue_name,body='',properties=properties)
    """
    def on_response(ch, method, props, body):
        if props.headers.get('zip'):
            buf = StringIO(body)
            f = gzip.GzipFile(fileobj=buf)
            body = f.read()
        print body
    channel.basic_consume(on_response,no_ack=True,queue=callback_queue)
    while True:
            connection.process_data_events()
    #connection.process_data_events()
    #channel.start_consuming()
    connection.close()