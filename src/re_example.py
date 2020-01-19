import re



resp = '24234234234 ' \
       '<a class="ExploreSpecialCard-title" href="/special/19593548" target="_blank" rel="noreferrer noopener" data-za-detail-view-id="5792">有哪些特别好看的壁纸？</a>' \
       'sfsafsafasf'




re_express = 'ExploreSpecialCard-title.*?>(.*?)</a>'

pattern = re.compile("ExploreSpecialCard-title.*?>(.*?)</a>", re.S)
titles = re.findall(pattern, resp)
print(titles)

result = re.match(re_express, resp)
print(result)


resp ='AMT-Network-Wanglei-100-(OPPO)(9)'
re_express = '\(\d+\)'

resp ='AMT-Network-Wanglei-100-(OPPO)->9#8#2< #333#'
#ExploreSpecialCard-title.*?>(.*?)</a>"

#9
re_express = '\((\d+)\)'

#(9)
re_express = '\(\d+\)'

#['9', '8', '2', '333']
re_express ='[(#](\d+)'

#['(OPPO)', '(9#8#2)']
re_express ='\(.*?\)'

#(OPPO)(9#8#2)
re_express ='\(.*\)'
resp_sub = '(OPPO)-(9#8#2)'
#9,8,2
re_express_sub='(\d+)'


re_express ='\(.*?\)'

#['9#8#2']
re_express = '.*>(.*)<'


#result = re.match(re_express,resp)
#print(result)

pattern = re.compile(re_express, re.S)
titles = re.findall(pattern, resp)
print(titles)
