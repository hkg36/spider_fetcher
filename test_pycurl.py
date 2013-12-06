__author__ = 'amen'
import pycurl
from StringIO import StringIO
crl = pycurl.Curl()
crl.fp = StringIO()
crl.setopt(pycurl.URL, "http://www.sina.com.cn")
crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
crl.perform()
res_code=crl.getinfo(pycurl.HTTP_CODE)
res_body=crl.fp.getvalue()
print res_body

crl.fp = StringIO()
crl.setopt(pycurl.URL, "http://www.baidu.com")
crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
crl.perform()
res_code=crl.getinfo(pycurl.HTTP_CODE)
res_body=crl.fp.getvalue()
print res_body

crl.fp = StringIO()
crl.setopt(pycurl.URL, "http://www.163.com")
crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
crl.perform()
res_code=crl.getinfo(pycurl.HTTP_CODE)
res_body=crl.fp.getvalue()
print res_body
