# RTC KPI
---

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
