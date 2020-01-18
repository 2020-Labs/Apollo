import urllib.request
import http.cookiejar
from urllib.parse import urlencode
from urllib.parse import parse_qs
from urllib.parse import quote

filename = '/work2/baidu.cookie'
cookie = http.cookiejar.LWPCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
for item in cookie:
    print(item.name, ' = ', item.value)


data = urlencode({"name":"中国" , "user":"wang"})
print(data)

obj = parse_qs(data)
print(obj['name'][0])


print(quote('中国'))