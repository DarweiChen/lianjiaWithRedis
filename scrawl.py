# -*- coding: utf-8 -*-
import logging
import socket
import time

import core
import model
import settings
import redis
import redisInit


if __name__ == "__main__":
    redisConn = redis.Redis(host="39.98.150.177", port=6379, password="cdw964930361")
    redisCity = redisConn.spop("city")
    while True:
        if redisCity is not None:
            city = redisCity.decode("utf-8")
            redisReginlist = redisConn.smembers(city) # 获取城市下属行政区拼音
            regionlist = []
            for r in redisReginlist:
                temp = r.decode("utf-8")
                regionlist.append(temp)
            # print(city)
            # print(regionlist)
            # print("=-=-=-=-=-=-=-=-")
            # 自此，从Redis服务器获取到需要爬取到城市和行政区列表

            # 开始获取房屋信息（城市，行政区列表）
            core.GetHouseByRegionlist(city, regionlist)

            time.sleep(5)
            # 再从redis获取新的目标城市
            redisCity = redisConn.spop("city")
        else:
            # 表示目标城市集合已清空，暂停进程
            time.sleep(3600)
            # 往Redis填充数据
            redisInit.cityInit()
            redisCity = redisConn.spop("city")
