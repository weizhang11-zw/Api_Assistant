import time


# 获取当前时间
def getNowtime():
    # 方法一：return time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
    # 方法二：
    return time.strftime('%Y-%m-%d %H_%M_%S')
