
# RTC KPI


## 配置文件和输出报告格式模板

> 配置文件：
```
{
    "version":2,
    "members":['A','B','C'],
    'report_file':'',
    'rtc':[
        {
            'url':'file:///',
            'report_title':'710Q-',
            'element_id_1':'table1',
            'element_id_3':'table2'
        },
        {
            'url':'file:///',
            'report_title':'710Q-',
            'element_id_1':'table1',
            'element_id_3':'table2'
        }
    ]
}
```

> 输出结果数据结构：
```
{
    'A':{
        'fixed':90,
        'out':1
    },
    'B':{
        'fixed':90,
        'out':1
    },
}
```

> 输出报告格式：
```
--------------------------------------------------------------------
URL: 710q.html 
数据采集时间：
报告生成时间：
--------------------------------------------------------------------
明细：
姓名        修复      分析转出          小计
A           87          3               90

......


```

## 功能模块的责任
- config: 解析配置文件
- HtmlLoader： 加载html文件（从本地或网络获取)
- Parser: 解析html并提取数据进行统计
- Printer: 输出统计结果，格式：文本/Markdown ， 注：文本格式输出同时会输出在日志文件
- RtcMain: 程序入口 ， 



