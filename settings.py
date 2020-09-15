# -*- coding: utf-8 -*-
DBENGINE = 'mysql'  # ENGINE OPTIONS: mysql, sqlite3, postgresql
DBNAME = 'ershoufang'
DBUSER = 'root'
DBPASSWORD = 'MySqlPass8!'
DBHOST = '39.98.150.177'
# DBHOST = '127.0.0.1'
DBPORT = 3306

CITYLIST = [['安徽', {'安庆': 'aq'}, {'滁州': 'cz.fang'}, {'合肥': 'hf'}, {'马鞍山': 'mas'}, {'芜湖': 'wuhu'}], ['北京', {'北京': 'bj'}],
            ['重庆', {'重庆': 'cq'}], ['福建', {'福州': 'fz'}, {'泉州': 'quanzhou'}, {'厦门': 'xm'}, {'漳州': 'zhangzhou'}],
            ['广东', {'东莞': 'dg'}, {'佛山': 'fs'}, {'广州': 'gz'}, {'惠州': 'hui'}, {'江门': 'jiangmen'}, {'清远': 'qy'},
             {'深圳': 'sz'}, {'珠海': 'zh'}, {'湛江': 'zhanjiang'}, {'中山': 'zs'}],
            ['广西', {'北海': 'bh'}, {'防城港': 'fcg'}, {'桂林': 'gl'}, {'柳州': 'liuzhou'}, {'南宁': 'nn'}], ['甘肃', {'兰州': 'lz'}],
            ['贵州', {'贵阳': 'gy'}],
            ['河北', {'保定': 'bd'}, {'廊坊': 'lf'}, {'秦皇岛': 'qhd.fang'}, {'石家庄': 'sjz'}, {'唐山': 'ts'}, {'张家口': 'zjk'}],
            ['海南', {'保亭': 'bt.fang'}, {'澄迈': 'cm.fang'}, {'儋州': 'dz.fang'}, {'海口': 'hk'}, {'临高': 'lg.fang'},
             {'乐东': 'ld.fang'}, {'陵水': 'ls.fang'}, {'琼海': 'qh.fang'}, {'三亚': 'san'}, {'五指山': 'wzs.fang'},
             {'文昌': 'wc.fang'}, {'万宁': 'wn.fang'}],
            ['湖南', {'长沙': 'cs'}, {'常德': 'changde'}, {'岳阳': 'yy'}, {'株洲': 'zhuzhou'}],
            ['河南', {'开封': 'kf'}, {'洛阳': 'luoyang'}, {'三门峡': 'smx.fang'}, {'新乡': 'xinxiang'}, {'许昌': 'xc'}, {'郑州': 'zz'},
             {'周口': 'zk'}, {'驻马店': 'zmd'}],
            ['湖北', {'鄂州': 'ez'}, {'黄石': 'huangshi'}, {'武汉': 'wh'}, {'襄阳': 'xy'}, {'宜昌': 'yichang'}],
            ['黑龙江', {'哈尔滨': 'hrb'}],
            ['江西', {'赣州': 'ganzhou'}, {'九江': 'jiujiang'}, {'吉安': 'jian'}, {'南昌': 'nc'}, {'上饶': 'sr'}],
            ['江苏', {'常州': 'changzhou'}, {'海门': 'haimen'}, {'淮安': 'ha'}, {'江阴': 'jy'}, {'昆山': 'ks'}, {'南京': 'nj'},
             {'南通': 'nt'}, {'苏州': 'su'}, {'无锡': 'wx'}, {'徐州': 'xz'}, {'盐城': 'yc'}, {'镇江': 'zj'}],
            ['吉林', {'长春': 'cc'}, {'吉林': 'jl'}], ['辽宁', {'大连': 'dl'}, {'丹东': 'dd'}, {'沈阳': 'sy'}],
            ['内蒙古', {'包头': 'baotou'}, {'赤峰': 'cf'}, {'呼和浩特': 'hhht'}], ['宁夏', {'银川': 'yinchuan'}],
            ['山东', {'菏泽': 'heze'}, {'济南': 'jn'}, {'济宁': 'jining'}, {'临沂': 'linyi'}, {'青岛': 'qd'}, {'泰安': 'ta'},
             {'潍坊': 'wf'}, {'威海': 'weihai'}, {'烟台': 'yt'}, {'淄博': 'zb'}],
            ['四川', {'巴中': 'bz'}, {'成都': 'cd'}, {'德阳': 'dy'}, {'达州': 'dazhou'}, {'广元': 'guangyuan'},
             {'乐山': 'leshan.fang'}, {'凉山': 'liangshan'}, {'绵阳': 'mianyang'}, {'眉山': 'ms.fang'}, {'南充': 'nanchong'},
             {'遂宁': 'sn'}, {'宜宾': 'yibin'}],
            ['陕西', {'宝鸡': 'baoji'}, {'汉中': 'hanzhong'}, {'西安': 'xa'}, {'咸阳': 'xianyang'}],
            ['山西', {'晋中': 'jz'}, {'太原': 'ty'}], ['上海', {'上海': 'sh'}], ['天津', {'天津': 'tj'}], ['新疆', {'乌鲁木齐': 'wlmq'}],
            ['云南', {'大理': 'dali'}, {'昆明': 'km'}, {'西双版纳': 'xsbn.fang'}],
            ['浙江', {'杭州': 'hz'}, {'湖州': 'huzhou'}, {'嘉兴': 'jx'}, {'金华': 'jh'}, {'宁波': 'nb'}, {'衢州': 'quzhou'},
             {'绍兴': 'sx'}, {'台州': 'taizhou'}, {'温州': 'wz'}, {'义乌': 'yw'}]]
# print(len(CITYLIST)) #29
ALLCITYCODE=[]  # 存放所有城市代号的列表
ALLPRIVINCE=[]  # 存放所有省份的列表
for item in CITYLIST: # item = ['安徽', {'安庆': 'aq'}, {'滁州': 'cz.fang'}, {'合肥': 'hf'}, {'马鞍山': 'mas'}, {'芜湖': 'wuhu'}]
    i = 0
    ALLPRIVINCE.append(item[0])
    perProvince=[]
    while i < len(item)-1 :
        perProvince.append(str(list(item[i+1].values())[0]))
        i+=1
    # print(perProvince)# 示例：['aq', 'cz.fang', 'hf', 'mas', 'wuhu']
    ALLCITYCODE.append(perProvince)

# print(ALLPRIVINCE)
'''
示例：
['安徽', '北京', '重庆', '福建', '广东', '广西', '甘肃', '贵州', '河北', '海南', '湖南', '河南', '湖北', '黑龙江', '江西',
 '江苏', '吉林', '辽宁', '内蒙古', '宁夏', '山东', '四川', '陕西', '山西', '上海', '天津', '新疆', '云南', '浙江']
'''
# print(ALLCITYCODE)
'''示例： 
[['aq', 'cz.fang', 'hf', 'mas', 'wuhu'], ['bj'], ['cq'], ['fz', 'quanzhou', 'xm', 'zhangzhou'], ['dg', 'fs', 
'gz', 'hui', 'jiangmen', 'qy', 'sz', 'zh', 'zhanjiang', 'zs'], ['bh', 'fcg', 'gl', 'liuzhou', 'nn'], ['lz'], ['gy'], 
['bd', 'lf', 'qhd.fang', 'sjz', 'ts', 'zjk'], ['bt.fang', 'cm.fang', 'dz.fang', 'hk', 'lg.fang', 'ld.fang', 
'ls.fang', 'qh.fang', 'san', 'wzs.fang', 'wc.fang', 'wn.fang'], ['cs', 'changde', 'yy', 'zhuzhou'], ['kf', 'luoyang', 
'smx.fang', 'xinxiang', 'xc', 'zz', 'zk', 'zmd'], ['ez', 'huangshi', 'wh', 'xy', 'yichang'], ['hrb'], ['ganzhou', 
'jiujiang', 'jian', 'nc', 'sr'], ['changzhou', 'haimen', 'ha', 'jy', 'ks', 'nj', 'nt', 'su', 'wx', 'xz', 'yc', 'zj'], 
['cc', 'jl'], ['dl', 'dd', 'sy'], ['baotou', 'cf', 'hhht'], ['yinchuan'], ['heze', 'jn', 'jining', 'linyi', 'qd', 
'ta', 'wf', 'weihai', 'yt', 'zb'], ['bz', 'cd', 'dy', 'dazhou', 'guangyuan', 'leshan.fang', 'liangshan', 'mianyang', 
'ms.fang', 'nanchong', 'sn', 'yibin'], ['baoji', 'hanzhong', 'xa', 'xianyang'], ['jz', 'ty'], ['sh'], ['tj'], 
['wlmq'], ['dali', 'km', 'xsbn.fang'], ['hz', 'huzhou', 'jx', 'jh', 'nb', 'quzhou', 'sx', 'taizhou', 'wz', 'yw']] 
'''
allinone=[]
for list in ALLCITYCODE:
    for k in list:
        if k.__contains__(".fang"):
            continue
        allinone.append(k)
# print(allinone)
# 最终链家上有二手房的城市：
'''['aq', 'hf', 'mas', 'wuhu', 'bj', 'cq', 'fz', 'quanzhou', 'xm', 'zhangzhou', 'dg', 'fs', 'gz', 'hui', 'jiangmen', 
'qy', 'sz', 'zh', 'zhanjiang', 'zs', 'bh', 'fcg', 'gl', 'liuzhou', 'nn', 'lz', 'gy', 'bd', 'lf', 'sjz', 'ts', 'zjk', 
'hk', 'san', 'cs', 'changde', 'yy', 'zhuzhou', 'kf', 'luoyang', 'xinxiang', 'xc', 'zz', 'zk', 'zmd', 'ez', 
'huangshi', 'wh', 'xy', 'yichang', 'hrb', 'ganzhou', 'jiujiang', 'jian', 'nc', 'sr', 'changzhou', 'haimen', 'ha', 
'jy', 'ks', 'nj', 'nt', 'su', 'wx', 'xz', 'yc', 'zj', 'cc', 'jl', 'dl', 'dd', 'sy', 'baotou', 'cf', 'hhht', 
'yinchuan', 'heze', 'jn', 'jining', 'linyi', 'qd', 'ta', 'wf', 'weihai', 'yt', 'zb', 'bz', 'cd', 'dy', 'dazhou', 
'guangyuan', 'liangshan', 'mianyang', 'nanchong', 'sn', 'yibin', 'baoji', 'hanzhong', 'xa', 'xianyang', 'jz', 'ty', 
'sh', 'tj', 'wlmq', 'dali', 'km', 'hz', 'huzhou', 'jx', 'jh', 'nb', 'quzhou', 'sx', 'taizhou', 'wz', 'yw'] '''


