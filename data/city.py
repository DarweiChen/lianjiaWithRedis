# -*- coding = utf-8 -*-
# @Time : 2020/8/28 2:16 下午
# @Author : 陈达维
# @File : city.py
# @Software : PyCharm
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request , urllib.error  # 制定URL，获取网页数据
import xlwt # excel操作
import sqlite3  # 进行SQLite数据库操作

import ssl
ssl._create_default_https_context = ssl._create_unverified_context



# 可以通过本程序获取链家所有城市列表代号列表，如下：
# ['安徽', {'安庆': 'aq'}, {'滁州': 'cz.fang'}, {'合肥': 'hf'}, {'马鞍山': 'mas'}, {'芜湖': 'wuhu'}]
# getData中有示例注释的那一行会对单个省份列表进行输出
# 截止至代码完成前爬取到的完整列表：
'''
很长很长
[['安徽', {'安庆': 'aq'}, {'滁州': 'cz.fang'}, {'合肥': 'hf'}, {'马鞍山': 'mas'}, {'芜湖': 'wuhu'}], ['北京', {'北京': 'bj'}], ['重庆', {'重庆': 'cq'}], ['福建', {'福州': 'fz'}, {'泉州': 'quanzhou'}, {'厦门': 'xm'}, {'漳州': 'zhangzhou'}], ['广东', {'东莞': 'dg'}, {'佛山': 'fs'}, {'广州': 'gz'}, {'惠州': 'hui'}, {'江门': 'jiangmen'}, {'清远': 'qy'}, {'深圳': 'sz'}, {'珠海': 'zh'}, {'湛江': 'zhanjiang'}, {'中山': 'zs'}], ['广西', {'北海': 'bh'}, {'防城港': 'fcg'}, {'桂林': 'gl'}, {'柳州': 'liuzhou'}, {'南宁': 'nn'}], ['甘肃', {'兰州': 'lz'}], ['贵州', {'贵阳': 'gy'}], ['河北', {'保定': 'bd'}, {'廊坊': 'lf'}, {'秦皇岛': 'qhd.fang'}, {'石家庄': 'sjz'}, {'唐山': 'ts'}, {'张家口': 'zjk'}], ['海南', {'保亭': 'bt.fang'}, {'澄迈': 'cm.fang'}, {'儋州': 'dz.fang'}, {'海口': 'hk'}, {'临高': 'lg.fang'}, {'乐东': 'ld.fang'}, {'陵水': 'ls.fang'}, {'琼海': 'qh.fang'}, {'三亚': 'san'}, {'五指山': 'wzs.fang'}, {'文昌': 'wc.fang'}, {'万宁': 'wn.fang'}], ['湖南', {'长沙': 'cs'}, {'常德': 'changde'}, {'岳阳': 'yy'}, {'株洲': 'zhuzhou'}], ['河南', {'开封': 'kf'}, {'洛阳': 'luoyang'}, {'三门峡': 'smx.fang'}, {'新乡': 'xinxiang'}, {'许昌': 'xc'}, {'郑州': 'zz'}, {'周口': 'zk'}, {'驻马店': 'zmd'}], ['湖北', {'鄂州': 'ez'}, {'黄石': 'huangshi'}, {'武汉': 'wh'}, {'襄阳': 'xy'}, {'宜昌': 'yichang'}], ['黑龙江', {'哈尔滨': 'hrb'}], ['江西', {'赣州': 'ganzhou'}, {'九江': 'jiujiang'}, {'吉安': 'jian'}, {'南昌': 'nc'}, {'上饶': 'sr'}], ['江苏', {'常州': 'changzhou'}, {'海门': 'haimen'}, {'淮安': 'ha'}, {'江阴': 'jy'}, {'昆山': 'ks'}, {'南京': 'nj'}, {'南通': 'nt'}, {'苏州': 'su'}, {'无锡': 'wx'}, {'徐州': 'xz'}, {'盐城': 'yc'}, {'镇江': 'zj'}], ['吉林', {'长春': 'cc'}, {'吉林': 'jl'}], ['辽宁', {'大连': 'dl'}, {'丹东': 'dd'}, {'沈阳': 'sy'}], ['内蒙古', {'包头': 'baotou'}, {'赤峰': 'cf'}, {'呼和浩特': 'hhht'}], ['宁夏', {'银川': 'yinchuan'}], ['山东', {'菏泽': 'heze'}, {'济南': 'jn'}, {'济宁': 'jining'}, {'临沂': 'linyi'}, {'青岛': 'qd'}, {'泰安': 'ta'}, {'潍坊': 'wf'}, {'威海': 'weihai'}, {'烟台': 'yt'}, {'淄博': 'zb'}], ['四川', {'巴中': 'bz'}, {'成都': 'cd'}, {'德阳': 'dy'}, {'达州': 'dazhou'}, {'广元': 'guangyuan'}, {'乐山': 'leshan.fang'}, {'凉山': 'liangshan'}, {'绵阳': 'mianyang'}, {'眉山': 'ms.fang'}, {'南充': 'nanchong'}, {'遂宁': 'sn'}, {'宜宾': 'yibin'}], ['陕西', {'宝鸡': 'baoji'}, {'汉中': 'hanzhong'}, {'西安': 'xa'}, {'咸阳': 'xianyang'}], ['山西', {'晋中': 'jz'}, {'太原': 'ty'}], ['上海', {'上海': 'sh'}], ['天津', {'天津': 'tj'}], ['新疆', {'乌鲁木齐': 'wlmq'}], ['云南', {'大理': 'dali'}, {'昆明': 'km'}, {'西双版纳': 'xsbn.fang'}], ['浙江', {'杭州': 'hz'}, {'湖州': 'huzhou'}, {'嘉兴': 'jx'}, {'金华': 'jh'}, {'宁波': 'nb'}, {'衢州': 'quzhou'}, {'绍兴': 'sx'}, {'台州': 'taizhou'}, {'温州': 'wz'}, {'义乌': 'yw'}]]
'''



def main():
    baseurl = "https://www.lianjia.com/city/"
    datalist = getData(baseurl)
    print("===========")
    print(datalist)


# <div class="city_list_tit c_b">安徽</div>
findProvinces = re.compile(r'<div class="city_list_tit c_b">(.*?)</div>')

# <a href="https://aq.lianjia.com/">安庆</a>
findCity = re.compile(r'.lianjia.com/">(.*?)</a>')
findCityCode = re.compile(r'<a href="https://(.*?).lianjia.com/">')  # 创建正则表达式对象，表示字符串匹配规则


# 爬取网页
def getData(baseurl):
    html = askURL(baseurl)  # 保存获取到到网页源码
    datalist = []

    # 2. 逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_="city_province"):  # 每个省份
        perProvince = []
        item = str(item)

        # re库用来通过正则表达式查指定的字符串
        province = re.findall(findProvinces, item)
        perProvince.append(province[0])  # 省份加入头部

        cityName = re.findall(findCity, item)
        cityCode = re.findall(findCityCode, item)
        # print(cityCode)
        i = 0
        for temp in cityName:
            citySet = {temp: cityCode[i]}
            perProvince.append(citySet)
            i += 1
        # print(perProvince)  # 示例： ['安徽', {'安庆': 'aq'}, {'滁州': 'cz.fang'}, {'合肥': 'hf'}, {'马鞍山': 'mas'}, {'芜湖': 'wuhu'}]
        datalist.append(perProvince)
    return datalist


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/84.0.4147.125 Safari/537.36 "
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    print("爬取完毕")



