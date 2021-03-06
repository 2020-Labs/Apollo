
# RTC Bug单统计 ==概要设计==

## 功能介绍
- 统计各成员的修复Bug数量
- 统计结果输出报告
- 统计数据保存, 可基于初始数据和最后一次的统计数据计算两次统计周期期间新增问题数量


## 功能模块的责任
- config  - 解析配置文件
- htmlloader： 加载html内容，来源：从本地/网络 , `注`: 可扩展请求网络
- spider: 解析html并提取数据
- db-processor: 统计数据的加载和持久化, 对提取的数据进行统计
- report: 输出统计结果，格式：文本/Markdown ， `注`：文本格式输出同时会输出在日志文件
- run.py: 程序入口 ， 选项参数

## 部署
程序目录结构
```text
-- rtc
  |- *.py （执行脚本）
  |- db
  	|- initial.dat
  	|- history.dat
  |- log.txt
  |- reports
  |- * （本地数据来源）
    |- rtc.config
    |- *.html
    |- **report.txt
```

## 启动流程

时序图:
```sequence
#md:sequence, 
#Youdao:sequenceDiagram
run.py->>run.py: 检查选项参数
run.py->>config.py: 读取配置项
run.py->>spider:run
spider-->>spider: 加载本地html文件
spider->>spider: 提取有效数据
spider->>dbprocessor: 统计
dbprocessor->>dbprocessor: 读取基础数据
dbprocessor-->>dbprocessor: 统计数据
dbprocessor-->>spider: 统计结果返回
spider->>dbprocessor: 保存
spider->>report: 输出统计报告
```




> 启动选项参数
```shell
ppython rtckpi.py  -c <xxx.config>| --config=<xxx.config>
```



## 配置文件

> 配置项介绍：

 - MEMBERS: 成员名单列表
 - VERSION: 版本号 （仅用于显示）
 - REPORT_TITLE:输出报告标题
 - REPORT_FMT: 输出报告格式，注TEXT/MD 
 - REPORT_FILE: 输出报告文件名 

 - RTCs:
     - URL:
     - FIX_IDs: 数组
     - OUT_IDs: 数组


> 配置文件模块：
```json
{
    "version":"2",
    "members":["A","B","C"],
    "report_title": "X团队 修复问题汇总",
    "report_fmt":"text",
    "rtc":[
        {
            "url":"file:///",
            "fix": ["table1","table2"]
            "out": ["table1"]
        },
        {
            "url": "http://",
            "fix": ["table1","table2"]
            "out": ["table1"]
        }
    ]
}
```



## 统计结果存储

> 存储格式：
```text
Text: 
- initial.dat 
  - initial: xxx 
  - last:   xxx 

history.dat
  - xxx
```

> 初始数据的格式

```json
"initial":
{
    "date":"2019-10-15",
    "A":{
        "fixed":"3",
        "out":"1"
    },
    "B":{
        "fixed":"2",
        "out":"1"
    }
}
```

> 输出结果数据结构：历史数据结构
```json
[
    {
        "createtime":"2020-2-2 17:00:03",
        "delta":
        {
            "date":"2020-1-15",
            "A":{
                "fixed":"90",
                "out":"1"
            },
            "B":{
                "fixed":"62",
                "out":"1"
            }
        }
    },
    ...
]
```



## 输出报告格式模板
### 文本格式输出报告模板

> .................................................................................
>
> 标题:710Q Network团队 修复问题汇总
> 数据采集时间：
> 报告生成时间：
> .................................................................................
>
> 明细：
> 姓名    修复    分析转出    小计
> A       87         3       90
>
> .....
>
> 2020-1-15 ~ 2020-1-23 新增数据
> 姓名    修复    分析转出    小计
> A        3         1        4
>
> ......




### Markdown文本格式报告模板

> ---
> 标题:710Q Network团队 修复问题汇总
> 数据采集时间：
> 报告生成时间：
> 
> ---
> 
> 明细：
> | 姓名 | 修复 | 分析转出 | 小计 |
> | --- | ---- | -------- | ---- |
> | A  | 87   | 3    | 90     |
> 
> ：：：：：：：：：：：：：：：：：：：：：：：
> 
> 2020-1-15 ~ 2020-1-23 新增数据
> | 姓名 | 修复 | 分析转出 | 小计 |
> | --- | ---- | -------- | ---- |
> | A    | 3  | 1       | 4  |
