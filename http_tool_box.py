import socket
import re
import random
from cStringIO import StringIO
import pycurl
import urlparse
import httplib
import gzip
from weibo_tools.weibo_autoreg import parseHeaders

InterfaceIP=None

def UseRandomLocalAddress():
    global InterfaceIP
    names,aliases,ips = socket.gethostbyname_ex(socket.gethostname())
    print ips
    to_use_ip=set()
    for ip in ips :
        if not re.match('^(192.)|(10.)|(127.)',ip):
            to_use_ip.add(ip)
            print 'use ip:',ip
    InterfaceIP=list(to_use_ip)

def getHttpBody(url,ref=None,content_type=None,body=None,cookie=None):
    source_addr=None
    if InterfaceIP is not None:
        if isinstance(InterfaceIP,list) and len(InterfaceIP)>0:
            source_addr=InterfaceIP[random.randint(0,len(InterfaceIP)-1)]
        elif (isinstance(InterfaceIP,str) or isinstance(InterfaceIP,unicode)) and len(InterfaceIP)>0:
            source_addr=InterfaceIP
    urlpart=urlparse.urlparse(url)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
             'Accept-Encoding':'gzip',
             'Host':urlpart.netloc}
    if content_type:
        headers["Content-Type"]=content_type
    if cookie:
        headers["Cookie"]=cookie
    if ref is not None:
        headers["Referer"]=ref

    """crl = pycurl.Curl()
    crl.setopt(pycurl.FOLLOWLOCATION, 0)
    crl.setopt(pycurl.MAXREDIRS, 5)
    crl.setopt(pycurl.USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')
    crl.setopt(pycurl.ENCODING,"gzip,deflate")
    if ref is not None:
        crl.setopt(pycurl.REFERER,ref)
    headers=[]
    if content_type:
        headers.append("Content-Type: %s;"%content_type)
    if cookie:
        headers.append("Cookie: %s;"%cookie)
    for i in xrange(len(headers)):
        if isinstance(headers[i],unicode):
            headers[i]=headers[i].encode('utf-8')
    crl.setopt(pycurl.HTTPHEADER, headers)
    if body:
        crl.setopt(crl.POSTFIELDS,body)
    
    if source_addr is not None:
        crl.setopt(pycurl.INTERFACE,source_addr)
    crl.setopt(pycurl.CONNECTTIMEOUT, 6)
    crl.setopt(pycurl.TIMEOUT, 15)
    crl.fp = StringIO()
    crl.hp=StringIO()
    crl.setopt(pycurl.URL, url)
    crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
    crl.setopt(crl.HEADERFUNCTION,crl.hp.write)
    crl.perform()

    res=crl.getinfo(pycurl.HTTP_CODE),crl.fp.getvalue(),parseHeaders(crl.hp)
    crl.close()"""
    if urlpart.scheme=="https":
        conn = httplib.HTTPSConnection(urlpart.netloc,source_address=(source_addr,0) if source_addr is not None else None ,timeout=20)
    else:
        conn = httplib.HTTPConnection(urlpart.netloc,source_address=(source_addr,0) if source_addr is not None else None ,timeout=20)
    conn.request('POST' if body else 'GET', urlpart.path, headers =headers
                ,body=body)
    res = conn.getresponse()
    res_body=res.read()
    if res.getheader('Content-Encoding')=='gzip':
        res_body=gzip.GzipFile(mode='rb',fileobj=StringIO(res_body)).read()
    result=(res.status,res_body,res.msg.dict)
    return result

if __name__ == '__main__':
    print getHttpBody('https://www.google.com.hk/search?q=%E6%B2%99%E5%A1%94%E6%96%AF+%E9%94%BB%E7%82%89&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:zh-CN:official&client=firefox-a',
                      cookie='PREF=ID=ab9b8ecbd188f031:U=11a2711234e6a912:FF=0:LR=lang_zh-CN|lang_en:LD=en:NW=1:TM=1359995945:LM=1378102101:GM=1:SG=1:S=f3MPctNZidoPA5o-; NID=67=aapjHT4qLZqX71lYWJ8831notRrUxciIaNKNkUldb93FPglrYBY-lIp3zhRTpMUUYTofuihWIuXb211g7qfE95iI_34BGU77DPqzLc3_d3SG0Xye60V8XcoqwBotyLwpuVLRL5AdYXw6kjqDTdjibx14Kl4tx5bgRDixRg4kcuWMhiwSOIHCffK2wrl7OOoAdglkdwbOYVRgy5FOG9-mW2zx9rDsUEaziB4o-k5y1pkJuR5H9Q; SID=DQAAAHIBAACXlBI8CHaZgYBJraoKkX6_69oRqcQJkOZPF1ao2WYJFJOnhJdaEwHe8pTFTXtyRlrvGmy6Nld-z1G8BTIlZi1sXys4FDKTUk88Ix4Tz8MnPAQyKiFSs-0rk_mJMZfj83s-iM5n6DbqidIrBsUQ0PQulvIIj_X91ezvQDy-YbbZYubpD9JKbVvPOYKjdB78wYqmqQMxlUpWzRiAk0DBdVfvmQDb4jphiXFyTaFkjumk3h3F3c1gIDNYSK3TNvgrRWkYAYU9wNWQ0YYMHk7g_YV7mhPZrNPbv61QE6zOpfNnXiAV2-sIdww5b9XeB3I5hUWW4PsHzxlPxJk_BEo4rZfg1QrSOo-9aHDckS1jm-KHqe83INaF0z3P3JoxvBd0jM2DtCO0P-6SIlwvfHdjIZnO4sv0hbU41FLL06iQKABP6nBOZT7Wp4_Eg9-6qMDv179If0SIvMQ_BynEpU8INc6RrCR5pvx5eRy5G70-wPJ7Kk0z1-5aJTTA-EzTTlTV1iE; HSID=AsuaDeIcYavcT0170; SSID=A5NsYHCb0nQBHyutF; APISID=qEGwFS6SQ_VNwOzH/AixechYlfBHXSXFyL; SAPISID=2sxxYezVR6Z1QGWa/ALk1_bu0BQgIfngLh')[2]
    print getHttpBody('https://reg.163.com/logins.jsp','http://www.163.com/','application/x-www-form-urlencoded',
                      'username=496642325%40163.com&password=180144206&type=1&product=163&savelogin=1&url=http%3A%2F%2Fwww.163.com%2Fspecial%2F0077450P%2Flogin_frame.html&url2=http%3A%2F%2Fwww.163.com%2Fspecial%2F0077450P%2Flogin_frame.html&noRedirect=1')
    print getHttpBody('http://www.163.com')