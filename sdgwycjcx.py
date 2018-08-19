
"""
    2017年山东省考成绩查询链接
    省直：http://www.rsks.sdhrss.gov.cn/17gwycjbohENwu6NrjE/login.aspx  （可以打开，监控消失）
    济南：http://rsks.jnhrss.gov.cn/kscx/front/show/showCjcxDetail.do?tableName=excel_20&showName=2017%25E5%25B9%25B4%25E6%25B5%258E%25E5%258D%2597%25E5%25B8%2582%25E8%2580%2583%25E8%25AF%2595%25E5%25BD%2595%25E7%2594%25A8%25E5%2585%25AC%25E5%258A%25A1%25E5%2591%2598%25E7%25AC%2594%25E8%25AF%2595%25E6%2588%2590%25E7%25BB%25A9%25E6%259F%25A5%25E8%25AF%25A2
    淄博：http://222.134.135.155:9004/ostm/login.jsp  （可以打开）
    潍坊：http://www.wfrsks.com/chaxun/gwycj   （可以打开 正在维护）
    青岛：http://www.qdhrss.gov.cn/UnifiedPublicServicePlatform/page/business/dscx/tycj.jsp （可以打开 没有公考信息）
    威海：http://221.2.141.198:8065/cjcx/adfasdfasdf17jhkhkjh/index.asp （链接失败）
    烟台：http://kszx.yt12333.com/wsbm/webregister/login/preLogin.aspx?timeID=11&examSort=99&examDate=201704 （网站有问题）
    东营：http://www.dyrsks.gov.cn/examQuery/simpleExamQuery.seam?examId=30 （可以打开）
    滨州：http://124.128.225.21/wb_binzhougwy/webregister/index.aspx （服务器错误）
    德州：http://222.133.32.5/wsbm1/cjcx/DbfCjcx/cjcx.htm （404）
    聊城：http://www.lcks.com.cn/cjcxD/index.aspx （可以打开 无公考信息）
    枣庄：http://218.56.155.46:9090/gwy2017/webregister/index.aspx （服务器错误）
    菏泽：http://www.hzrsks.gov.cn/new_cjcx/cjcx.htm（可以打开 无公考信息）
    济宁：http://218.57.204.123/gwy2014/webregister/login/login.aspx （页面失效）
    临沂：http://www.lyrs.gov.cn/default/xxcx/21/（可以打开 无公考信息）
    泰安：http://124.130.146.14:35269/gwybm/webRegister/index.aspx（可以打开 无公考信息）
    日照：http://rzhrss.gov.cn/rz12333/e/tool/gwykscj/2017/2017index.php（404）
    莱芜：http://www.eoffcn.com/kszx/cjcx/416258.html （链接失败）


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


def get_data():
    ''' 获取数据
        传入比对数据 '''
    # 德州人社局成绩查询网址：http://222.133.32.5/wsbm1/cjcx/DbfCjcx/cjcx.htm
    list_url = [{'p': '德州', 'u': 'http://222.133.32.5/wsbm1/cjcx/DbfCjcx/cjcx.htm'},
                {'p': '济南', 'u': 'http://2naive.cn'}]
    list_res = []
    for dict_url in list_url:
        print(dict_url['p'])
        url = dict_url['u']
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        try:
            open_web = urllib.request.urlopen(req)
            if open_web:
                list_res.append({"p": dict_url['p'], 'u': dict_url['u'] })
            else:
                list_res.append({"p": dict_url['p'], 'u': False})
        except:
            list_res.append({"p": dict_url['p'], 'u': False})
            continue
        time.sleep(1)
        return list_res

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
    re_data = 'Sorry, Page Not Found'
    # 初始输出信息
    now_data = '<meta charset="UTF-8">' \
               '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">' \
               '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />' \
               '<center>山东省公务员考试 各地市监控系统</center><br><center>' + ' 正在监控中...</center><br>'
    wr_index(now_data)
    while True:
        dict_get = get_data()
        # data_get = dict_get[1]
        print(dict_get)
        for dict_p in dict_get:
            data_get = dict_p['u']
            if data_get:
                content = '''
监控结果通知：
    时间：%s
    事件：%s 成绩公布页面开放
    查看：%s
            山东省公务员考试成绩监控系统
                    ''' % (str(datetime.datetime.now()), dict_p['p'], dict_p['u'])
                ret = mail(content)
                ret = '1'
                wr_index(str(datetime.datetime.now()) + " %s 成绩查询页面开放 <a href='%s'>点击查询<a>(%s)<br>" % (dict_p['p'], dict_p['u'], ret))
            d += 1
        # 心跳消息/条/小时(每小时的第10分钟返回)
        if  datetime.datetime.now().minute == 10 and datetime.datetime.now().hour % 2 == 0:
            now_data = str(datetime.datetime.now())+' 第 %d 次监控中...<br>' % d
            wr_index(now_data)
        # 每 n s检测一次
        time.sleep(15)
# 入口函数
main()
