
# RTC KPI
***

## 配置文件和输出报告格式模板
> config file template:

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

> result template:
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

## 功能模块的责任
- config: 解析配置文件
- HtmlLoader： 加载html文件（从本地或网络获取)
- Parser: 解析html并提取数据进行统计
- Printer: 输出统计结果，格式：文本/Markdown
- RtcMain: 程序入口



