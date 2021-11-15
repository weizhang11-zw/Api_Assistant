# Api_Assistant
API接口自动化框架v1.0（unnitest（单元测试框架）+DDT（数据驱动）+ HTMLTestRunnerNew （测试报告框架）+ SMTP发送邮件）

接口自动化测试框架
一、框架说明
开发语言：python 3.0+；
框架&方法：unnitest（单元测试框架）+DDT（数据驱动）+ HTMLTestRunnerNew
（测试报告框架）+ SMTP发送邮件；

详细框架结构：

![4c90e27cb62182d686c5cdcab74da6c](https://user-images.githubusercontent.com/58303130/141709846-44250ce7-c4ef-431a-9fd9-aad4bb1ad878.png)


二、工程目录

![image](https://user-images.githubusercontent.com/58303130/141046978-b5bcc2e6-47b4-4870-b605-97b8cadd2504.png)

三、实战操作
1、测试用例输入方法
（1）测试用例输入模板

![image](https://user-images.githubusercontent.com/58303130/141047004-4ff0fec0-b146-4957-ab80-33938da76fd4.png)


（2）用例需要输入的内容


CASE_NO = 1            # 用例编号：必填（格式：test_x）

MODULE_NAME = 2        # 项目名称：非必填

CASE_NAME = 3          # 用例名称：非必填

RUN_FLAG = 4           # 用例是否运行：必填（格式：是/否）

URL = 5                # 接口url：必填

REQUEST_METHOD = 6     # 请求类型post/get：必填（格式：post/get）

HEADERS = 7            # 请求头：非必填（填写：以json的格式输入）

COOKIES = 8            # cookies依赖：非必填（${test_02}表示存在用例返回cookie依赖）

REQUEST_PARAM = 9      # 请求体：必填（格式：json；依赖填写：1、${test_01.xx}表示存在用例返回结果依赖；2、test_01表示依赖用例编号；3、xx为json解析表达式，使用 . 表示层级。）

EXP_RESULT = 10        # 期望响应结果：必填

STATUS_CODE = 11       # 响应code：不填，自动化生成

RESPONSE_TEXT = 12     # 实际响应结果：不填，自动生成

ASSET_TYPE = 13        # 断言类型：必填（相等/包含/正则）

ASSET_PATTERN = 14     # 断言规则：非必填

EXEC_RESULT = 15       # 是否成功pass/fail：不填，自动化生成



请求体填写举例：

1、无依赖数据，直接填写json传参内容；

2、{"id":"${test_05.data}"}：
说明传参依赖测试用例5的响应返回结果的data字段数据；

3、{"id":"${test_05.data.healthStewardName}"}：
说明传参依赖测试用例5的响应返回结果data字典的healthStewardName字段数据；

4、{"id":"${test_05.data[0].healthStewardName}"}：
说明传参依赖测试用例5的响应返回结果data列表的第一个字段healthStewardName数据；




期望结果和断言填写举例：

1、断言类型（相等）+断言规则（空）
期望响应结果和实际响应结果全部相等，顾期望响应结果需填写和实际响应结果一致；

2、断言类型（相等）+断言规则（正则）
举例：断言规则---data.healthStewardName
断言预期和实际响应结果的data属性healthStewardName字段内容相等，顾期望响应结果可以填写和实际响应结果一致；

3、断言类型（包含）+断言规则（空）
实际响应结果包含期望响应结果，顾期望响应结果只需填写包含的断言内容即可；
举例："code":"1000"

4、断言类型（正则）+断言规则（空）
实则响应结果正则包含期望响应结果，顾期望响应结果只需填写正则断言内容即可；
举例：.*"code":"1000","message":"接口调用成功",.*


2、测试报告和日志

![image](https://user-images.githubusercontent.com/58303130/141047016-9d602480-9f3b-4857-a336-b662be70933d.png)
![image](https://user-images.githubusercontent.com/58303130/141047022-8bb59aba-39c1-4cf0-aba9-635198c70747.png)



3、邮件内容

![image](https://user-images.githubusercontent.com/58303130/141047035-e155214f-79bd-407d-b5f5-9b621a20d52a.png)
