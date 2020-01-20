import requests
import re
import json

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return  response.text
    return None

def main(offest):
    url = 'https://maoyan.com/board/4?offset=' + str(offest)

    html = get_one_page(url)
    print(html)
    for item in parse_on_page(html):
        print(item)
        write_to_file(item)


def write_to_file(content):
    with open('result.txt',mode='a',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False) + '\n')


def parse_on_page(html):
    re_exp = '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a' \
                          '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>' \
                          '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'
    pattern = re.compile(re_exp, re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5] + item[6]
        }

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
