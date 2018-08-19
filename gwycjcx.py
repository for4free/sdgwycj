
"""
    1、自动抓取德州人社局成绩查询页面
    2、大约每分钟比对一次
    3、记录匹配结果并保存页面
    4、出现页面更改时邮件通知
    作者：mengf
    最后更新：2018-05-20
"""

# coding=utf-8

import urllib.request
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def mail(content = '请查看结果'):
    ''' 发生变化时
        邮件通知监控结果
        QQ邮箱 '''
    my_sender = 'xxx@qq.com'  # 发件人邮箱账号
    my_pass = 'xxx'  # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = 'xxx@qq.com'  # 收件人邮箱账号
    ret = "通知成功"
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["山东省公务员考试成绩监控中心", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["山东公考考生", my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "山东省公务员考试成绩监控结果"                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()# 关闭连接
    except Exception:# 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = "通知失败"
    return ret


def get_data(re_data):
    ''' 获取数据
        传入比对数据 '''
    # http://www.wfrsks.com/chaxun/gwycj
    url = 'http://www.wfrsks.com/chaxun/gwycj'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    try:
        open_web = urllib.request.urlopen(req)
        data = open_web.read().decode("utf-8", "ignore")  # 读取页面数据 并转换成str类型
        if data.startswith(re_data):
            return False
        else:
            return data
    except:
        return '404'


def wr_index(content):
    ''' 向主页内写入数据
        传入追加内容 '''
    file_data_index = content
    file_index = open('index.html', 'ab')
    file_index.write(file_data_index.encode('utf-8'))
    file_index.close()


def save_page(file_name, data_get):
    ''' 保存变更的页面
        传入文件名和文件内容 '''
    file = open(file_name, 'wb')
    file_data = data_get.encode('utf-8')
    file.write(file_data)
    file.close()


def main():
    ''' 主函数：处理数据
            1、页面更改：获取更改后的页面并保存，将更改信息写入主页内
            2、页面未更改：不进行任何信息更改
            3、链接出错：将出错信息（非系统信息）写入主页
            4、心跳消息：每小时（00：10）返回一条心跳消息，防止程序宕掉 '''
    # 计数：循环次数
    d = 1
    # 标记网络错误的输出
    flag_404 = True
    # 初始数据（德州人社局网站目前404）
    re_data = '网站正在维护，请稍后再试！'
    # 初始输出信息
    now_data = '<meta charset="UTF-8">' \
               '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">' \
               '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' \
               '<center>山东省公务员考试 成绩公布监控(潍坊)</center><br>'+ str(datetime.datetime.now()) + ' 第 1 次监控中...<br>'
    wr_index(now_data)
    while True:
        data_get = get_data(re_data)
        if data_get:
            if data_get == '404':
                # falg_404 防止网络错误信息一直输出
                if flag_404:
                    wr_index(str(datetime.datetime.now()) + " 成绩公布页面无法访问<br>")
                    flag_404 = False
            else:
                flag_404 = True
                # 将更改后的网页的前几位赋值到对比数据变量中
                re_data = data_get[:21]
                file_name_time = str(int(time.time()))
                file_name = file_name_time + '.html'
                # print(datetime.datetime.now(), 'the page is changed , click<a href="./'+file_name+'">'+file_name_time+'</a> to view')
                # 邮件通知
                content = '''
监控结果通知：
    时间：%s
    事件：潍坊成绩公布页面开放
    查看：http://www.wfrsks.com/chaxun/gwycj
            山东省公务员考试成绩监控系统
                ''' % (str(datetime.datetime.now()))

                ret = mail(content)
                # 主页文件
                wr_index(str(datetime.datetime.now()) + ' 成绩公布页面出现改变，点击 <a href="./' + file_name + '">' + file_name_time + '</a> 查看(%s)<br>' % ret)
                # 页面变更文件（保存件）
                save_page(file_name, data_get)
                 # else:
                 #     print(datetime.datetime.now(), 'False')
        d += 1
        # 心跳消息/条/小时(每小时的第10分钟返回)
        if  datetime.datetime.now().minute == 55 and datetime.datetime.now().hour % 2 == 0:
            now_data = str(datetime.datetime.now())+' 第 %d 次监控中...<br>' % d
            wr_index(now_data)
        # 每 n s检测一次
        time.sleep(58)
# 入口函数
main()
