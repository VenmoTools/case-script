# case-script
生成测试用例脚本语言


# 测试用例
一条测试用例可以用json表示如下
```json
{
  "case": {
    "name": "注册用户",
    "description": "注册新用户（正常流程）",
    "module": "注册模块",
    "condition": [
        "n_exists<admin,unit.item,number(1)>in<数据库>",
        "request<注册>status<status::enable>"
    ],
    "steps": [
      "input<用户名输入框,admin>",
      "input<密码输入框,12345>",
      "click<登录>"
    ],
    "except_result": [
      "except_normal<用户名输入框>",
      "except_normal<密码输入框>",
      "except<登录成功>in<提示框>"
    ],
    "note": [
      ""
    ]
  }
}
```

# 语法
##  前置条件
在测试用例执行前应该满足的条件

### status_is
处于某种状态时

语法：
```
status_is<status>
```

**用法**：
```
status_is<status::enable>
```
含义：

当处于`可用`状态时

> 更多的状态详见[status](#status)
>
### when
处于某种情况时 

语法：
```
when<when>
```

**用法**：
```
when<出现alert弹框>
```
含义：

当处于`出现alert弹框`时

###  situation_is
处于某种情况下时

语法：
```
situation_is<s>
```

**用法**：
```
situation_is<用户名输入框无效>
```
含义：

当处于`用户名输入框无效`情况下


###  value_is
某个内容的值应该为xxx

语法：
```
value_is<内容, 值>
```

**用法**：
```
content_is<用户名输入框,20>
```
含义：

`用户名输入框`的值为`20`

###  exists
某个地方中存在xxx

n_exists<数据,unit.item,number(1)>in<数据库>at<xxx>
语法：
```
exists<内容, 单位, 数量>in<哪里>
exists<数据, 单位, 数量>in<哪里>at<什么情况下>
```

**用法**：
```
exists<数据,unit::item,number(1)>in<数据库>
exists<异常记录,unit::cust(条),number(5)>in<日志平台>
exists<异常记录, unit::cust(条), number(5)>in<日志平台>at<什么情况下>
```
含义：

`数据库`中存在`一项数据`
`日志平台`中存在`5条异常记录`

###  n_exists
某个地方中不存在xxx


语法：
```
n_exists<内容, 单位, 数量>in<哪里>
```

**用法**：
```
n_exists<数据,unit::item,number(1)>in<数据库>
n_exists<异常记录,unit::cust(条),number(5)>in<日志平台>
```
含义：

`数据库`中不存在`一项数据`
`日志平台`中不存在`5条异常记录`

###  request
要求某个事物状态必须为xxx


语法：
```
request<内容>status<状态>
```

**用法**：
```
request<性别单选框>status<status::enable>
```
含义：

`性别单选框`的状态必须为`可用`

###  n_request
要求某个事物状态不能为xxx


语法：
```
n_request<内容>status<状态>
```

**用法**：
```
n_request<性别单选框>status<status::enable>
```
含义：

`性别单选框`的状态不能为`可用`



###  in_list
要求某个事物在列表中


语法：
```
in_list<事物>with[
  项1,
  项2,
  项3,
]
```

**用法**：
```
in_list<数据库>with[
  Mysql,
  mango,
  sqlserver,
]
```
含义：

`数据库`为以下任意一项`[Mysql,mango,sqlserver]`



# status
```
status::enable => 可用状态
status::disable  => 不可用状态
status::exists => 存在状态
status::n_exists => 不存在
status::delete => 删除
status::n_delete => 没有删除
status::active => 激活状态
status::n_active => 失效状态
status::cust(无效) => 无效状态 (自定义状态)
```



# ACTION
click<name>

click<name>in<xxx> | click<name>left<xxx> | click<name>parti_left<xxx>

click<name>at<>

CLICK_WITH_SOMETHING = "点击【{some_thing}】的【{name}】按钮"

# INPUT
input<name,value>

input<name,value>in<xxx>

# DRAG
drag<图片>to<另一个窗口>

drag<图片>left<浏览器>to<另一个窗口>

drag<python.py>left<文件列表>to<输入框>right<红色图标>

drag<图片>to<输入框>right<红色图标>

# OPEN
open<xxx.exe>

open<xxx.exe>situation_is(python被删除)

# SELECT
select<金融>

select<金融>desc<项>

select<金融>bottom<选择框>

select<金融>bottom<选择框>desc<项>

SELECT_PARTICULAR_SOMETHING = "在{location}选择【{name}】"

# OTHER
forward<http://www.example.com>

back_to<桌面>

return_to<上一步>

jump_to<步骤1>

repeat_step<5>

find<输入>do<input<admin>>

# Location
in<文件>

parti_in<浏览器,设置>

left<浏览器>

parti_left<浏览器,设置>

right<浏览器>

parti_right<浏览器,设置>

top<浏览器>

parti_top<浏览器,地址栏>

bottom<浏览器>

parti_bottom<浏览器,地址栏>

b_left<浏览器>

b_right<浏览器>

t_left<浏览器>

t_right<浏览器>

location<location::bottom_left>

location::bottom_left

location::bottom_right

location::top_left

location::top_right

location::top

location::bottom

location::middle

location::left

location::right


# except
except_normal<输入框>

except_normal<输入框>left<浏览器>

EXCEPT_PARTICULAR_SOMEWHERE_DISPLAY = "{location}的【{some_where}】为【{something}】"

except_result<文本框>is`<admin>`

`except<单元框>status_is<status::enable>`

except_alert<提示框>left<输入框>

except<登录成功>in<提示框>

except<红色字体>change_to<蓝色字体>

except_note<请输入用户名>

except_note<请输入用户名>left<用户名输入框>

except_include<用户名,admin>

EXCEPT_EXISTS = "在【{somewhere}】中存在【{something}】{description}"