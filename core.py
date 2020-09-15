# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
import model
import misc
import time
import datetime
import urllib3
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# 根据行政区获取房屋信息
def GetHouseByRegionlist(city, regionlist=[u'xicheng']):
    print("现在对这个城市："+city)
    starttime = datetime.datetime.now()
    for regionname in regionlist:
        logging.info("Get Onsale House Infomation in %s" % regionname)
        try:
            get_house_perregion(city, regionname)
        except Exception as e:
            logging.error(e)
            pass
    endtime = datetime.datetime.now()
    logging.info("Run time: " + str(endtime - starttime))


# 获取单个行政区的房屋信息
def get_house_perregion(city, district):
    baseUrl = u"http://%s.lianjia.com/" % (city)
    url = baseUrl + u"ershoufang/%s/" % district
    source_code = misc.get_source_code(url)
    soup = BeautifulSoup(source_code, 'lxml')
    if check_block(soup):
        return
    total_pages = misc.get_total_pages(url)
    if total_pages == None:
        row = model.Houseinfo.select().count()
        raise RuntimeError("Finish at %s because total_pages is None" % row)

    for page in range(total_pages):
        if page > 0:
            url_page = baseUrl + u"ershoufang/%s/pg%d/" % (district, page)
            source_code = misc.get_source_code(url_page)
            soup = BeautifulSoup(source_code, 'lxml')
        i = 0
        log_progress("GetHouseByRegionlist", district, page + 1, total_pages)
        data_source = []
        hisprice_data_source = []
        for ultag in soup.findAll("ul", {"class": "sellListContent"}):
            for name in ultag.find_all('li'):
                i = i + 1
                info_dict = {}
                try:
                    info_dict.update({u'region': district})
                    housetitle = name.find("div", {"class": "title"})
                    info_dict.update(
                        {u'title': housetitle.a.get_text().strip()})
                    info_dict.update({u'link': housetitle.a.get('href')})
                    houseID = housetitle.a.get('data-housecode')
                    info_dict.update({u'houseID': houseID})

                    houseinfo = name.find("div", {"class": "houseInfo"})
                    info = houseinfo.get_text().split('|')
                    #info_dict.update({u'community': info[0]})
                    info_dict.update({u'housetype': info[0]})
                    info_dict.update({u'square': info[1]})
                    info_dict.update({u'direction': info[2]})
                    info_dict.update({u'decoration': info[3]})
                    info_dict.update({u'floor': info[4]})
                    info_dict.update({u'years': info[5]})

                    housefloor = name.find("div", {"class": "positionInfo"})
                    communityInfo = housefloor.get_text().split('-')
                    info_dict.update({u'community': communityInfo[0]})
                    #info_dict.update({u'years': housefloor.get_text().strip()})
                    #info_dict.update({u'floor': housefloor.get_text().strip()})

                    followInfo = name.find("div", {"class": "followInfo"})
                    if followInfo == None or followInfo =='' or len(followInfo) == 0 :
                        info_dict.update(
                            {u'followInfo': '0' })
                    else:
                        followStr = re.sub("\D","",followInfo.get_text().strip())
                        followNum = int(followStr[0])
                        if followNum >0:
                            info_dict.update(
                                {u'followInfo':0+followNum})
                        else:
                            info_dict.update(
                                {u'followInfo': '0' })

                    taxfree = name.find("span", {"class": "taxfree"})
                    if taxfree == None:
                        info_dict.update({u"taxtype": ""})
                    else:
                        info_dict.update(
                            {u"taxtype": taxfree.get_text().strip()})

                    totalPrice = name.find("div", {"class": "totalPrice"})
                    info_dict.update(
                        {u'totalPrice': totalPrice.span.get_text()})

                    unitPrice = name.find("div", {"class": "unitPrice"})
                    info_dict.update(
                        {u'unitPrice': unitPrice.get("data-price")})
                    # print(info_dict)
                except:

                    continue

                # Houseinfo insert into mysql
                data_source.append(info_dict)
                hisprice_data_source.append(
                    {"houseID": info_dict["houseID"], "totalPrice": info_dict["totalPrice"]})
                # model.Houseinfo.insert(**info_dict).upsert().execute()
                #model.Hisprice.insert(houseID=info_dict['houseID'], totalPrice=info_dict['totalPrice']).upsert().execute()
        # print(data_source)
        with model.database.atomic():
            if data_source:
                model.Houseinfo.insert_many(data_source).upsert().execute()
            if hisprice_data_source:
                model.Hisprice.insert_many(
                    hisprice_data_source).upsert().execute()
        time.sleep(1)

# 检查ip是否被锁
def check_block(soup):
    if soup.title.string == "414 Request-URI Too Large":
        logging.error(
            "Lianjia block your ip, please verify captcha manually at lianjia.com")
        return True
    return False

# 定义log程序
def log_progress(function, address, page, total):
    logging.info("Progress: %s %s: current page %d total pages %d" %
                 (function, address, page, total))
