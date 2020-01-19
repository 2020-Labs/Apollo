import requests
from bs4 import BeautifulSoup
import re


resp = requests.get('http://httpbin.org/get')
print(resp.status_code)
print(resp.text)

resp = requests.post("http://httpbin.org/post")
print(resp.status_code)
print(resp.text)


#zhihu
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

resp = requests.get("http://www.zhihu.com/explore", headers=headers)

pattern = re.compile("ExploreSpecialCard-title.*?>(.*?)</a>", re.S)
titles = re.findall(pattern, resp.text)
print('话题：', titles)
print(resp.cookies)

for item in resp.cookies:
    print(item.name, ' = ', item.value)


csdn_profile_url= 'https://i.csdn.net/#/uc/profile'
csdn_url = 'http://www.csdn.net'
csdn_req_cookie = 'uuid_tt_dd=10_36837000730-1569162404412-486862; dc_session_id=10_1569162404412.113313; UN=RockEx; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_36837000730-1569162404412-486862!5744*1*RockEx; __gads=Test; UserName=RockEx; UserInfo=d9aab6a0c19f436383e989de9d0ff310; UserToken=d9aab6a0c19f436383e989de9d0ff310; UserNick=RockEx; AU=ABF; BT=1578534431281; p_uid=U000000; searchHistoryArray=%255B%2522python%2520webdriver%2522%252C%2522python%2520%25E5%25AD%2597%25E7%25AC%25A6%25E4%25B8%25B2%25E7%25A9%25BA%25E6%25A0%25BC%25E5%25A1%25AB%25E5%2585%2585%2522%252C%2522python%2520%25E5%25AD%2597%25E7%25AC%25A6%25E4%25B8%25B2%25E6%25A0%25BC%25E5%25BC%258F%25E5%258C%2596%2522%252C%2522python%2520key-value%2522%252C%2522python%25E7%2588%25AC%25E8%2599%25AB%2520%25E5%25A4%25A7%25E5%25AD%25A6%25E6%258E%2592%25E8%25A1%258C%2522%255D; aliyun_webUmidToken=TDD40823F4548B395946824F21213C24251CBEC8C93FF9FE999EC1693DD; firstDie=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1577001965,1579329546,1579331482,1579331575; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1579343514; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F103603408%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; dc_tos=q4at96'
headers = {
    "Cookie": csdn_req_cookie,
    "Host":'i.csdn.net',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
resp = requests.get(csdn_profile_url, headers=headers)
resp.encoding = 'utf-8'
#print(resp.text)
if resp.status_code == requests.codes.ok:
    with open('csdn.html', mode='w', encoding='utf-8') as file:
        file.write(resp.text)


