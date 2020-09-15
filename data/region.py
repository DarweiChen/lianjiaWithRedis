# -*- coding = utf-8 -*-
# @Time : 2020/8/28 4:02 下午
# @Author : 陈达维
# @File : region.py
# @Software : PyCharm
import re
import time

from bs4 import BeautifulSoup

from data.city import askURL

# 可以通过本程序爬取链家所有城市下属的行政区
'''
[['aq', {'大观区': 'daguanqu'}, {'太湖县': 'taihuxian'}, {'宜秀区': 'yixiuqu'}, {'宿松县': 'susongxian'}, {'岳西县': 'yuexixian'}, {'怀宁县': 'huainingxian'}, {'望江县': 'wangjiangxian'}, {'桐城市': 'tongchengshi'}, {'潜山县': 'qianshanxian'}, {'迎江区': 'yingjiangqu'}], ['hf', {'包河': 'baohe'}, {'巢湖市': 'chaohushi'}, {'庐江县': 'lujiangxian'}, {'空港经济示范区': 'konggangjingjishifanqu'}, {'蜀山': 'shushan'}, {'庐阳': 'luyang'}, {'瑶海': 'yaohai'}, {'政务': 'zhengwu'}, {'滨湖新区': 'binhuxinqu'}, {'经开': 'jingkai2'}, {'高新': 'gaoxin8'}, {'新站': 'xinzhan'}, {'肥东': 'feidong'}, {'肥西': 'feixi'}, {'长丰': 'changfeng'}], ['mas', {'博望区': 'bowangqu'}, {'含山县': 'hanshanxian'}, {'和县': 'hexian'}, {'当涂县': 'dangtuxian'}, {'花山区': 'huashanqu'}, {'雨山区': 'yushanqu'}], ['wuhu', {'三山区': 'sanshanqu'}, {'南陵县': 'nanlingxian'}, {'弋江区': 'yijiangqu'}, {'无为县': 'wuweixian'}, {'繁昌县': 'fanchangxian'}, {'经济开发区': 'jingjikaifaqu'}, {'芜湖县': 'wuhuxian'}, {'镜湖区': 'jinghuqu'}, {'鸠江区': 'jiujiangqu'}], ['bj', {'东城': 'dongcheng'}, {'西城': 'xicheng'}, {'朝阳': 'chaoyang'}, {'海淀': 'haidian'}, {'丰台': 'fengtai'}, {'石景山': 'shijingshan'}, {'通州': 'tongzhou'}, {'昌平': 'changping'}, {'大兴': 'daxing'}, {'亦庄开发区': 'yizhuangkaifaqu'}, {'顺义': 'shunyi'}, {'房山': 'fangshan'}, {'门头沟': 'mentougou'}, {'平谷': 'pinggu'}, {'怀柔': 'huairou'}, {'密云': 'miyun'}, {'延庆': 'yanqing'}], ['cq', {'江北': 'jiangbei'}, {'渝北': 'yubei'}, {'南岸': 'nanan'}, {'巴南': 'banan'}, {'沙坪坝': 'shapingba'}, {'九龙坡': 'jiulongpo'}, {'渝中': 'yuzhong'}, {'大渡口': 'dadukou'}, {'江津': 'jiangjing'}, {'北碚': 'beibei'}, {'开州区': 'kaizhouqu'}, {'巫山县': 'wushanxian1'}, {'巫溪县': 'wuxixian'}, {'秀山土家族苗族自治县': 'xiushantujiazumiaozuzizhixian'}, {'酉阳土家族苗族自治县': 'youyangtujiazumiaozuzizhixian'}, {'荣昌区': 'rongchangqu'}, {'彭水苗族土家族自治县': 'pengshuimiaozutujiazuzizhixian'}, {'忠县': 'zhongxian'}, {'奉节县': 'fengjiexian'}, {'垫江县': 'dianjiangxian'}, {'城口县': 'chengkouxian'}, {'铜梁': 'tongliang'}, {'璧山': 'bishan'}, {'合川': 'hechuang'}, {'长寿': 'changshou1'}, {'万州': 'wanzhou'}, {'涪陵': 'fuling'}], ['fz', {'鼓楼区': 'gulouqu3'}, {'台江区': 'taijiangqu1'}, {'晋安区': 'jinanqu1'}, {'马尾区': 'maweiqu1'}, {'仓山区': 'cangshanqu1'}, {'闽侯县': 'minhouxian'}, {'连江县': 'lianjiangxian'}, {'平潭县': 'pingtanxian'}, {'福清市': 'fuqingshi'}], ['quanzhou', {'惠安县': 'huianxian1'}, {'晋江市': 'jinjiangshi'}, {'石狮市': 'shishishi'}, {'南安市': 'nananshi'}, {'永春县': 'yongchunxian'}, {'德化县': 'dehuaxian'}, {'洛江区': 'luojiangqu1'}, {'泉港区': 'quangangqu'}, {'鲤城区': 'lichengqu1'}, {'安溪县': 'anxixian'}, {'丰泽区': 'fengzequ1'}, {'金门县': 'jinmenxian'}], ['xm', {'思明': 'siming'}, {'湖里': 'huli'}, {'海沧': 'haicang'}, {'集美': 'jimei'}, {'翔安': 'xiangan'}, {'同安': 'tongan'}], ['zhangzhou', {'龙文区': 'longwenqu1'}, {'芗城区': 'xiangchengqu3'}, {'漳州港': 'zhangzhougang1'}, {'角美台商投资区': 'jiaomeitaishangtouziqu1'}, {'龙海市': 'longhaishi'}, {'长泰县': 'changtaixian1'}, {'南靖县': 'nanjingxian1'}, {'平和县': 'pinghexian1'}, {'华安县': 'huaanxian'}, {'漳浦县': 'zhangpuxian1'}, {'东山县': 'dongshanxian'}, {'诏安县': 'zhaoanxian'}, {'云霄县': 'yunxiaoxian'}], ['dg', {'南城区': 'nanchengqu'}, {'东城区': 'dongchengqu'}, {'万江区': 'wanjiangqu'}, {'莞城区': 'wanchengqu'}, {'寮步镇': 'liaobuzhen1'}, {'虎门镇': 'humenzhen3'}, {'长安镇': 'changanzhen1'}, {'松山湖': 'songshanhu'}, {'厚街镇': 'houjiezhen2'}, {'高埗镇': 'gaobuzhen1'}, {'道滘镇': 'daojiaozhen'}, {'洪梅镇': 'hongmeizhen'}, {'沙田镇': 'shatianzhen'}, {'大岭山镇': 'dalingshanzhen1'}, {'常平镇': 'changpingzhen'}, {'大朗镇': 'dalangzhen'}, {'黄江镇': 'huangjiangzhen'}, {'樟木头镇': 'zhangmutouzhen'}, {'塘厦镇': 'tangxiazhen'}, {'清溪镇': 'qingxizhen'}, {'凤岗镇': 'fenggangzhen'}, {'东坑镇': 'dongkengzhen'}, {'企石镇': 'qishizhen'}, {'石排镇': 'shipaizhen'}, {'茶山镇': 'chashanzhen'}, {'麻涌镇': 'machongzhen'}, {'横沥镇': 'henglizhen'}, {'石龙镇': 'shilongzhen'}, {'石碣镇': 'shijiezhen1'}, {'中堂镇': 'zhongtangzhen'}, {'望牛墩镇': 'wangniudunzhen'}, {'桥头镇': 'qiaotouzhen'}, {'谢岗镇': 'xiegangzhen'}], ['fs', {'禅城': 'chancheng'}, {'南海': 'nanhai'}, {'顺德': 'shunde'}, {'三水': 'sanshui1'}, {'高明': 'gaoming1'}, {'番禺': 'panyu'}, {'白云': 'baiyun'}], ['gz', {'天河': 'tianhe'}, {'越秀': 'yuexiu'}, {'荔湾': 'liwan'}, {'海珠': 'haizhu'}, {'番禺': 'panyu'}, {'白云': 'baiyun'}, {'黄埔': 'huangpugz'}, {'从化': 'conghua'}, {'增城': 'zengcheng'}, {'花都': 'huadou'}, {'南沙': 'nansha'}, {'南海': 'nanhai'}, {'顺德': 'shunde'}], ['hui', {'惠城': 'huicheng'}, {'仲恺高新技术产业开发区': 'zhongkaigaoxinjishuchanyekaifaqu'}, {'惠阳': 'huiyang'}, {'大亚湾': 'dayawan'}, {'惠东': 'huidong'}, {'博罗': 'boluo'}], ['jiangmen', {'江海区': 'jianghaiqu'}, {'蓬江区': 'pengjiangqu'}, {'新会区': 'xinhuiqu'}, {'台山市': 'taishanshi'}, {'鹤山市': 'heshanshi'}, {'恩平市': 'enpingshi'}, {'开平市': 'kaipingshi'}], ['qy', {'佛冈县': 'fogangxian'}, {'清城区': 'qingchengqu'}, {'清新区': 'qingxinqu'}, {'英德市': 'yingdeshi'}, {'连南瑶族自治县': 'liannanyaozuzizhixian'}, {'连山壮族瑶族自治县': 'lianshanzhuangzuyaozuzizhixian'}, {'连州市': 'lianzhoushi'}, {'阳山县': 'yangshanxian'}], ['sz', {'罗湖区': 'luohuqu'}, {'福田区': 'futianqu'}, {'南山区': 'nanshanqu'}, {'盐田区': 'yantianqu'}, {'宝安区': 'baoanqu'}, {'龙岗区': 'longgangqu'}, {'龙华区': 'longhuaqu'}, {'光明区': 'guangmingqu'}, {'坪山区': 'pingshanqu'}, {'大鹏新区': 'dapengxinqu'}], ['zh', {'香洲区': 'xiangzhouqu'}, {'金湾区': 'jinwanqu'}, {'斗门区': 'doumenqu'}], ['zhanjiang', {'霞山区': 'xiashanqu'}, {'赤坎区': 'chikanqu'}, {'坡头区': 'potouqu'}, {'麻章区': 'mazhangqu'}, {'遂溪县': 'suixixian'}, {'廉江市': 'lianjiangshi'}, {'吴川市': 'wuchuanshi'}, {'雷州市': 'leizhoushi'}, {'徐闻县': 'xuwenxian'}], ['zs', {'小榄镇': 'xiaolanzhen'}, {'板芙镇': 'banfuzhen'}, {'横栏镇': 'henglanzhen'}, {'民众镇': 'minzhongzhen'}, {'神湾镇': 'shenwanzhen'}, {'阜沙镇': 'fushazhen'}, {'黄圃镇': 'huangpuzhen'}, {'三乡镇': 'sanxiangzhen'}, {'三角镇': 'sanjiaozhen'}, {'东凤镇': 'dongfengzhen'}, {'东区': 'dongqu'}, {'东升镇': 'dongshengzhen1'}, {'南头镇': 'nantouzhen'}, {'南朗镇': 'nanlangzhen'}, {'古镇镇': 'guzhenzhen'}, {'坦洲镇': 'tanzhouzhen'}, {'大涌镇': 'dayongzhen'}, {'西区': 'xiqu'}, {'南区': 'nanqu'}, {'石岐区': 'shiqiqu'}, {'火炬': 'huoju'}, {'港口镇': 'gangkouzhen'}, {'沙溪镇': 'shaxizhen'}, {'五桂山': 'wuguishan'}], ['bh', {'合浦县': 'hepuxian'}, {'海城区': 'haichengqu'}, {'铁山港区': 'tieshangangqu'}, {'银海区': 'yinhaiqu'}], ['fcg', {'港口区': 'gangkouqu'}, {'防城区': 'fangchengqu'}], ['gl', {'七星区': 'qixingqu'}, {'临桂区': 'linguiqu'}, {'象山区': 'xiangshanqu'}, {'秀峰区': 'xiufengqu'}, {'叠彩区': 'diecaiqu'}, {'雁山区': 'yanshanqu'}, {'灌阳县': 'guanyangxian'}, {'桂北新区（灵川县）': 'guibeixinqulingchuanxian1'}, {'龙胜各族自治县': 'longshenggezuzizhixian'}, {'永福县': 'yongfuxian'}, {'平乐县': 'pinglexian'}, {'恭城瑶族自治县': 'gongchengyaozuzizhixian'}, {'资源县': 'ziyuanxian'}, {'全州县': 'quanzhouxian'}, {'荔浦县': 'lipuxian'}, {'兴安县': 'xinganxian'}, {'阳朔县': 'yangshuoxian'}], ['liuzhou', {'三江侗族自治县': 'sanjiangdongzuzizhixian'}, {'城中区': 'chengzhongqu2'}, {'柳北区': 'liubeiqu'}, {'柳南区': 'liunanqu'}, {'柳城县': 'liuchengxian'}, {'柳江区': 'liujiangqu'}, {'融安县': 'ronganxian'}, {'融水苗族自治县': 'rongshuimiaozuzizhixian'}, {'鱼峰区': 'yufengqu'}, {'鹿寨县': 'luzhaixian'}], ['nn', {'青秀区': 'qingxiuqu'}, {'江南区': 'jiangnanqu'}, {'西乡塘区': 'xixiangtangqu'}, {'兴宁区': 'xingningqu'}, {'邕宁区': 'yongningqu'}, {'良庆区': 'liangqingqu'}, {'武鸣县': 'wumingxian'}, {'宾阳县': 'binyangxian'}, {'上林县': 'shanglinxian'}, {'马山县': 'mashanxian'}, {'横县': 'hengxian'}, {'隆安县': 'longanxian'}], ['lz', {'七里河区': 'qilihequ'}, {'兰州新区': 'lanzhouxinqu'}, {'城关区': 'chengguanqu'}, {'安宁区': 'anningqu'}, {'榆中县': 'yuzhongxian'}, {'永登县': 'yongdengxian'}, {'皋兰县': 'gaolanxian'}, {'红古区': 'hongguqu'}, {'西固区': 'xiguqu'}], ['gy', {'云岩区': 'yunyanqu'}, {'白云区': 'baiyunqu'}, {'乌当区': 'wudangqu'}, {'南明区': 'nanmingqu'}, {'花溪区': 'huaxiqu'}, {'息烽县': 'xifengxian'}, {'开阳县': 'kaiyangxian'}, {'修文县': 'xiuwenxian'}, {'清镇市': 'qingzhenshi'}, {'观山湖区': 'guanshanhuqu'}], ['bd', {'涞水': 'laishui1'}, {'涿州': 'zhuozhou1'}, {'易县': 'yixian'}, {'高碑店': 'gaobeidian1'}, {'竞秀区': 'jingxiuqu'}, {'莲池区': 'lianchiqu'}, {'满城区': 'manchengqu'}, {'清苑区': 'qingyuanqu'}, {'徐水区': 'xushuiqu'}, {'安国市': 'anguoshi'}, {'定州市': 'dingzhoushi'}, {'博野县': 'boyexian'}, {'涞源县': 'laiyuanxian'}, {'唐县': 'tangxian'}, {'定兴县': 'dingxingxian'}, {'望都县': 'wangduxian'}, {'曲阳县': 'quyangxian'}, {'顺平县': 'shunpingxian'}, {'蠡县': 'lixian1'}, {'高阳县': 'gaoyangxian'}, {'阜平县': 'fupingxian2'}], ['lf', {'燕郊': 'yanjiao'}, {'香河': 'xianghe'}, {'广阳': 'guangyang'}, {'安次': 'anci'}, {'廊坊经济技术开发区': 'langfangjingjijishu'}, {'固安': 'guan'}, {'大厂': 'dachang'}, {'永清': 'yongqing'}], ['sjz', {'裕华': 'yuhua1'}, {'井陉矿区': 'jingxingkuangqu1'}, {'长安': 'changan'}, {'桥西': 'qiaoxi'}, {'新华': 'xinhua'}, {'开发区': 'kaifaqu1'}, {'正定': 'zhengding'}, {'鹿泉': 'luquan'}, {'栾城': 'luancheng'}, {'藁城': 'gaocheng'}, {'元氏县': 'yuanshixian'}, {'辛集市': 'xinjishi'}, {'灵寿县': 'lingshouxian'}, {'平山': 'pingshan1'}, {'井陉县': 'jingxingxian'}, {'赵县': 'zhaoxian'}, {'深泽县': 'shenzexian'}, {'晋州市': 'jinzhoushi'}, {'高邑县': 'gaoyixian'}], ['ts', {'丰南区': 'fengnanqu'}, {'丰润区': 'fengrunqu'}, {'乐亭县': 'laotingxian'}, {'古冶区': 'guyequ'}, {'开平区': 'kaipingqu'}, {'曹妃甸区': 'caofeidianqu'}, {'滦南县': 'luannanxian'}, {'滦州市': 'luanzhoushi'}, {'玉田县': 'yutianxian'}, {'路北区': 'lubeiqu'}, {'路南区': 'lunanqu'}, {'迁安市': 'qiananshi'}, {'迁西县': 'qianxixian'}, {'遵化市': 'zunhuashi'}], ['zjk', {'万全区': 'wanquanqu'}, {'下花园': 'xiahuayuan'}, {'宣化区': 'xuanhuaqu'}, {'尚义县': 'shangyixian'}, {'崇礼区': 'chongliqu1'}, {'崇礼县': 'chonglixian'}, {'康保县': 'kangbaoxian'}, {'张北县': 'zhangbeixian'}, {'怀安县': 'huaianxian'}, {'怀来县': 'huailaixian'}, {'桥东区': 'qiaodongqu3'}, {'桥西区': 'qiaoxiqu3'}, {'沽源县': 'guyuanxian'}, {'涿鹿县': 'zhuoluxian'}, {'蔚县': 'weixian3'}, {'赤城县': 'chichengxian'}, {'阳原县': 'yangyuanxian'}], ['hk', {'秀英': 'xiuyingqu2'}, {'龙华': 'longhuaqu1'}, {'美兰': 'meilanqu1'}, {'琼山': 'qiongshanqu1'}], ['san', {'崖州': 'yazhou1'}, {'天涯': 'tianya1'}, {'海棠': 'haitang1'}, {'吉阳': 'jiyang3'}], ['cs', {'雨花': 'yuhua'}, {'岳麓': 'yuelu'}, {'天心': 'tianxin'}, {'开福': 'kaifu'}, {'芙蓉': 'furong'}, {'望城': 'wangcheng'}, {'宁乡': 'ningxiang'}, {'浏阳': 'liuyang'}, {'长沙县': 'changshaxian'}], ['changde', {'临澧县': 'linlixian'}, {'安乡县': 'anxiangxian'}, {'桃源县': 'taoyuanxian'}, {'武陵区': 'wulingqu'}, {'汉寿县': 'hanshouxian'}, {'津市市': 'jinshishi'}, {'澧县': 'lixian4'}, {'石门县': 'shimenxian'}, {'鼎城区': 'dingchengqu'}], ['yy', {'岳阳楼区': 'yueyanglouqu'}, {'岳阳县': 'yueyangxian'}, {'湘阴县': 'xiangyinxian'}, {'平江县': 'pingjiangxian'}, {'君山区': 'junshanqu'}, {'汨罗市': 'miluoshi'}, {'云溪区': 'yunxiqu'}, {'华容县': 'huarongxian'}, {'临湘市': 'linxiangshi'}], ['zhuzhou', {'天元区': 'tianyuanqu'}, {'芦淞区': 'lusongqu'}, {'荷塘区': 'hetangqu'}, {'石峰区': 'shifengqu'}, {'醴陵市': 'lilingshi'}, {'炎陵县': 'yanlingxian1'}, {'株洲县': 'zhuzhouxian'}, {'攸县': 'youxian'}, {'茶陵县': 'chalingxian'}], ['kf', {'龙亭区': 'longtingqu'}, {'杞县': 'qixian3'}, {'兰考县': 'lankaoxian'}, {'通许县': 'tongxuxian'}, {'祥符区': 'xiangfuqu'}, {'尉氏县': 'weishixian'}, {'鼓楼区': 'gulouqu6'}, {'顺河区': 'shunhequ1'}, {'禹王台区': 'yuwangtaiqu'}], ['luoyang', {'洛龙区': 'luolongqu'}, {'涧西区': 'jianxiqu'}, {'西工区': 'xigongqu'}, {'瀍河回族区': 'chanhehuizuqu'}, {'老城区': 'laochengqu1'}, {'伊川县': 'yichuanxian'}, {'伊滨区': 'yibinqu1'}, {'偃师市': 'yanshishi'}, {'吉利区': 'jiliqu'}, {'孟津县': 'mengjinxian'}, {'宜阳县': 'yiyangxian'}, {'嵩县': 'songxian'}, {'新安县': 'xinanxian'}, {'栾川县': 'luanchuanxian'}, {'汝阳县': 'ruyangxian'}, {'洛宁县': 'luoningxian'}], ['xinxiang', {'红旗区': 'hongqiqu'}, {'卫滨区': 'weibinqu2'}, {'牧野区': 'muyequ'}], ['xc', {'建安区': 'jiananqu'}, {'禹州市': 'yuzhoushi'}, {'襄城县': 'xiangchengxian2'}, {'鄢陵县': 'yanlingxian'}, {'长葛市': 'changgeshi'}, {'魏都区': 'weiduqu'}], ['zz', {'二七': 'erqi'}, {'郑东新区': 'zhengdongxinqu'}, {'荥阳市': 'xingyangshi'}, {'新郑市': 'xinzhengshi'}, {'上街区': 'shangjiequ'}, {'巩义市': 'gongyishi'}, {'新密市': 'xinmishi'}, {'登封市': 'dengfengshi'}, {'中牟县': 'zhongmuxian'}, {'经开区': 'jingkaiqu'}, {'高新': 'gaoxin9'}, {'航空港区': 'hangkonggangqu'}, {'中原': 'zhongyuan'}, {'管城回族区': 'guanchenghuizuqu'}, {'惠济': 'huiji'}, {'金水': 'jinshui'}], ['zk', {'商水县': 'shangshuixian'}, {'太康县': 'taikangxian'}, {'川汇区': 'chuanhuiqu'}, {'扶沟县': 'fugouxian'}, {'沈丘县': 'chenqiuxian'}, {'淮阳县': 'huaiyangxian'}, {'西华县': 'xihuaxian'}, {'郸城县': 'danchengxian'}, {'项城市': 'xiangchengshi'}, {'鹿邑县': 'luyixian'}], ['zmd', {'上蔡县': 'shangcaixian'}, {'平舆县': 'pingyuxian'}, {'新蔡县': 'xincaixian'}, {'正阳县': 'zhengyangxian'}, {'汝南县': 'runanxian'}, {'泌阳县': 'biyangxian'}, {'确山县': 'queshanxian'}, {'西平县': 'xipingxian'}, {'遂平县': 'suipingxian'}, {'驿城区': 'yichengqu1'}], ['ez', {'鄂城区': 'echengqu'}, {'葛店开发区': 'gediankaifaqu'}, {'梁子湖区': 'liangzihuqu'}, {'华容区': 'huarongqu'}], ['huangshi', {'西塞山区': 'xisaishanqu'}, {'黄石港区': 'huangshigangqu'}, {'阳新县': 'yangxinxian2'}, {'铁山区': 'tieshanqu'}, {'下陆区': 'xialuqu'}, {'大冶市': 'dayeshi'}], ['wh', {'江岸': 'jiangan'}, {'江汉': 'jianghan'}, {'硚口': 'qiaokou'}, {'东西湖': 'dongxihu'}, {'武昌': 'wuchang'}, {'青山': 'qingshan'}, {'洪山': 'hongshan'}, {'汉阳': 'hanyang'}, {'东湖高新': 'donghugaoxin'}, {'江夏': 'jiangxia'}, {'蔡甸': 'caidian'}, {'黄陂': 'huangbei'}, {'新洲': 'xinzhou'}, {'沌口开发区': 'zhuankoukaifaqu'}, {'汉南': 'hannan'}], ['xy', {'襄城区': 'xiangchengqu1'}, {'襄州区': 'xiangzhouqu1'}, {'樊城区': 'fanchengqu'}], ['yichang', {'西陵区': 'xilingqu'}, {'伍家岗区': 'wujiagangqu'}, {'夷陵区': 'yilingqu'}, {'宜都市': 'yidushi'}, {'枝江市': 'zhijiangshi'}, {'当阳市': 'dangyangshi'}, {'秭归县': 'ziguixian'}, {'猇亭区': 'xiaotingqu'}, {'点军区': 'dianjunqu'}, {'兴山县': 'xingshanxian'}, {'远安县': 'yuananxian'}, {'五峰土家族自治县': 'wufengtujiazuzizhixian'}, {'长阳土家族自治县': 'changyangtujiazuzizhixian'}], ['hrb', {'平房': 'pingfang'}, {'道外': 'daowai'}, {'道里': 'daoli'}, {'南岗': 'nangang'}, {'香坊': 'xiangfang'}, {'松北': 'songbei'}, {'尚志市': 'shangzhishi'}, {'巴彦县': 'bayanxian'}, {'呼兰区': 'hulanqu'}, {'阿城区': 'achengqu'}, {'延寿县': 'yanshouxian'}, {'依兰县': 'yilanxian'}, {'木兰县': 'mulanxian'}, {'宾县': 'binxian'}, {'通河县': 'tonghexian'}, {'五常市': 'wuchangshi'}, {'双城区': 'shuangchengqu'}, {'方正县': 'fangzhengxian'}, {'肇东市': 'zhaodongshi2'}], ['ganzhou', {'章贡区': 'zhanggongqu'}, {'赣县区': 'ganxianqu'}, {'南康区': 'nankangqu'}, {'于都县': 'yuduxian'}, {'瑞金市': 'ruijinshi'}, {'宁都县': 'ningduxian'}, {'上犹县': 'shangyouxian'}, {'会昌县': 'huichangxian'}, {'信丰县': 'xinfengxian'}, {'全南县': 'quannanxian'}, {'兴国县': 'xingguoxian'}, {'大余县': 'dayuxian'}, {'安远县': 'anyuanxian'}, {'定南县': 'dingnanxian'}, {'寻乌县': 'xunwuxian'}, {'崇义县': 'chongyixian'}, {'石城县': 'shichengxian'}, {'龙南县': 'longnanxian'}], ['jiujiang', {'修水县': 'xiushuixian'}, {'共青城市': 'gongqingchengshi'}, {'庐山市': 'lushanshi'}, {'彭泽县': 'pengzexian'}, {'德安县': 'deanxian'}, {'柴桑区': 'chaisangqu'}, {'武宁县': 'wuningxian'}, {'永修县': 'yongxiuxian'}, {'浔阳区': 'xunyangqu'}, {'湖口县': 'hukouxian'}, {'濂溪区': 'lianxiqu'}, {'瑞昌市': 'ruichangshi'}, {'都昌县': 'duchangxian'}], ['jian', {'吉州区': 'jizhouqu2'}, {'青原区': 'qingyuanqu2'}, {'吉安县': 'jianxian'}, {'吉水县': 'jishuixian'}, {'泰和县': 'taihexian2'}, {'安福县': 'anfuxian'}, {'永新县': 'yongxinxian'}, {'永丰县': 'yongfengxian'}, {'遂川县': 'suichuanxian'}, {'峡江县': 'xiajiangxian'}], ['nc', {'东湖区': 'donghuqu'}, {'南昌县': 'nanchangxian'}, {'安义县': 'anyixian'}, {'新建区': 'xinjianqu'}, {'湾里区': 'wanliqu'}, {'红谷滩': 'honggutan1'}, {'西湖区': 'xihuqu'}, {'进贤县': 'jinxianxian'}, {'青云谱区': 'qingyunpuqu'}, {'青山湖区': 'qingshanhuqu'}, {'高新区': 'gaoxinqu11'}, {'经开区': 'jingkaiqu8'}], ['sr', {'上饶县': 'shangraoxian'}, {'信州区': 'xinzhouqu'}, {'广丰区': 'guangfengqu'}], ['changzhou', {'武进区': 'wujinqu'}, {'金坛区': 'jintanqu'}, {'钟楼区': 'zhonglouqu'}, {'溧阳市': 'liyangshi'}, {'天宁区': 'tianningqu'}, {'新北区': 'xinbeiqu'}], ['haimen', {'包场': 'baochang'}, {'滨江': 'binjiang3'}, {'川姜': 'chuanjiang'}, {'海门': 'haimen1'}, {'海门市': 'haimenshi1'}, {'姜灶': 'jiangzao'}, {'金新': 'jinxin'}, {'临江': 'linjiang'}, {'启东市': 'qidongshi1'}, {'三厂': 'sanchang'}, {'三余': 'sanyu'}, {'四甲': 'sijia'}, {'张芝山': 'zhangzhishan'}], ['ha', {'清江浦区': 'qingjiangpuqu'}, {'淮阴区': 'huaiyinqu'}, {'淮安区': 'huaianqu'}, {'洪泽区': 'hongzequ'}, {'涟水县': 'lianshuixian'}], ['jy', {'长泾镇': 'changjingzhen'}, {'澄江街道': 'chengjiangjiedao'}, {'高新区': 'gaoxinqu14'}, {'顾山镇': 'gushanzhen'}, {'璜土镇': 'huangtuzhen'}, {'华士镇': 'huashizhen'}, {'江阴': 'jiangyin'}, {'临港经济开发区': 'lingangjingjikaifaqu'}, {'南闸街道': 'nanzhajiedao'}, {'青阳镇': 'qingyangzhen'}, {'新桥镇': 'xinqiaozhen'}, {'徐霞客镇': 'xuxiakezhen'}, {'月城镇': 'yuechengzhen'}, {'云亭街道': 'yuntingjiedao'}, {'周庄镇': 'zhouzhuangzhen'}, {'祝塘镇': 'zhutangzhen'}], ['ks', {'巴城': 'bacheng'}, {'淀山湖': 'dianshanhu'}, {'花桥': 'huaqiao'}, {'锦溪': 'jinxi'}, {'开发区': 'kaifaqu5'}, {'陆家': 'lujia'}, {'甪直': 'luzhi'}, {'千灯': 'qiandeng'}, {'玉山城北': 'yushanchengbei'}, {'玉山城南': 'yushanchengnan'}, {'玉山城西': 'yushanchengxi'}, {'玉山高新区': 'yushangaoxinqu'}, {'玉山老城区': 'yushanlaochengqu'}, {'张浦': 'zhangpu'}, {'周市': 'zhoushi'}, {'周庄': 'zhouzhuang'}], ['nj', {'鼓楼': 'gulou'}, {'建邺': 'jianye'}, {'秦淮': 'qinhuai'}, {'玄武': 'xuanwu'}, {'雨花台': 'yuhuatai'}, {'栖霞': 'qixia'}, {'江宁': 'jiangning'}, {'浦口': 'pukou'}, {'六合': 'liuhe'}, {'溧水': 'lishui'}, {'高淳': 'gaochun'}], ['nt', {'南通经济技术开发区': 'nantongjingjijishukaifaqu'}, {'启东市': 'qidongshi'}, {'如东县': 'rudongxian'}, {'如皋市': 'rugaoshi'}, {'崇川区': 'chongchuanqu'}, {'海安县': 'haianxian'}, {'海门区': 'haimenqu'}, {'港闸区': 'gangzhaqu'}, {'通州区': 'tongzhouqu'}], ['su', {'工业园区': 'gongyeyuan'}, {'吴中': 'wuzhong'}, {'姑苏': 'gusu'}, {'高新': 'gaoxin1'}, {'相城': 'xiangcheng'}, {'吴江': 'wujiang'}, {'昆山': 'kunshan'}], ['wx', {'滨湖': 'binhu'}, {'梁溪': 'liangxi'}, {'新吴': 'xinwu'}, {'惠山': 'huishan'}, {'锡山': 'xishan'}, {'江阴市': 'jiangyinshi'}, {'宜兴市': 'yixingshi'}], ['xz', {'云龙区': 'yunlongqu'}, {'鼓楼区': 'gulouqu1'}, {'泉山区': 'quanshanqu'}, {'铜山区': 'tongshanqu'}, {'金山桥开发区': 'jinshanqiaokaifaqu'}, {'新城区': 'xinchengqu3'}, {'贾汪区': 'jiawangqu'}, {'邳州市': 'pizhoushi'}, {'新沂市': 'xinyishi'}, {'睢宁县': 'suiningxian'}, {'沛县': 'peixian'}, {'丰县': 'fengxian1'}], ['yc', {'东台市': 'dongtaishi'}, {'亭湖区': 'tinghuqu'}, {'响水县': 'xiangshuixian'}, {'大丰区': 'dafengqu'}, {'射阳县': 'sheyangxian'}, {'建湖县': 'jianhuxian'}, {'滨海县': 'binhaixian'}, {'盐都区': 'yanduqu'}, {'阜宁县': 'funingxian'}], ['zj', {'丹徒区': 'dantuqu'}, {'丹阳市': 'danyangshi'}, {'京口': 'jingkou'}, {'句容': 'jurong'}, {'扬中市': 'yangzhongshi'}, {'润州': 'runzhou'}], ['cc', {'九台区': 'jiutaiqu'}, {'二道区': 'erdaoqu'}, {'农安县': 'nonganxian'}, {'朝阳区': 'chaoyangqu'}, {'南关区': 'nanguanqu'}, {'双阳区': 'shuangyangqu'}, {'宽城区': 'kuanchengqu'}, {'德惠市': 'dehuishi'}, {'净月区': 'jingyuequ'}, {'榆树市': 'yushushi'}, {'汽车产业开发区': 'qichechanyekaifaqu'}, {'经开北区': 'jingkaibeiqu'}, {'经开区': 'jingkaiqu1'}, {'绿园区': 'lvyuanqu'}, {'高新北区': 'gaoxinbeiqu'}, {'高新区': 'gaoxinqu16'}], ['jl', {'丰满区': 'fengmanqu'}, {'船营区': 'chuanyingqu'}, {'昌邑区': 'changyiqu'}, {'龙潭区': 'longtanqu'}, {'桦甸市': 'huadianshi'}, {'永吉县': 'yongjixian'}, {'磐石市': 'panshishi'}, {'舒兰市': 'shulanshi'}, {'蛟河市': 'jiaoheshi'}], ['dl', {'甘井子': 'ganjingzi'}, {'沙河口': 'shahekou'}, {'中山': 'zhongshan'}, {'西岗': 'xigang'}, {'高新园区': 'gaoxinyuanqu'}, {'开发区': 'kaifaqudl'}, {'金州': 'jinzhou'}, {'旅顺口': 'lvshunkou'}, {'普兰店': 'pulandian'}, {'瓦房店': 'wafangdian'}], ['dd', {'东港市': 'donggangshi'}, {'元宝区': 'yuanbaoqu'}, {'凤城市': 'fengchengshi'}, {'宽甸满族自治县': 'kuandianmanzuzizhixian'}, {'振兴区': 'zhenxingqu'}, {'振安区': 'zhenanqu'}], ['sy', {'康平县': 'kangpingxian'}, {'新民市': 'xinminshi'}, {'法库县': 'fakuxian'}, {'辽中区': 'liaozhongqu'}, {'铁西': 'tiexi'}, {'和平': 'heping1'}, {'沈河': 'shenhe'}, {'浑南': 'hunnan'}, {'大东': 'dadong'}, {'皇姑': 'huanggu'}, {'于洪': 'yuhong'}, {'苏家屯': 'sujiatun'}, {'沈北新区': 'shenbeixinqu'}], ['baotou', {'东河区': 'donghequ'}, {'石拐区': 'shiguaiqu'}, {'青山区': 'qingshanqu'}, {'九原区': 'jiuyuanqu'}, {'白云鄂博矿区': 'baiyunebokuangqu'}, {'昆都仑区': 'kundoulunqu'}, {'土默特右旗': 'tumoteyouqi'}, {'达尔罕茂明安联合旗': 'daerhanmaominganlianheqi'}, {'固阳县': 'guyangxian'}, {'稀土高新区': 'xitugaoxinqu'}, {'滨河新区': 'binhexinqu'}], ['cf', {'宁城县': 'ningchengxian'}, {'元宝山区': 'yuanbaoshanqu'}, {'喀喇沁旗': 'kalaqinqi'}, {'克什克腾旗': 'keshiketengqi'}, {'林西县': 'linxixian'}, {'巴林左旗': 'balinzuoqi'}, {'巴林右旗': 'balinyouqi'}, {'翁牛特旗': 'wengniuteqi'}, {'松山区': 'songshanqu'}, {'阿鲁科尔沁旗': 'alukeerqinqi'}, {'红山区': 'hongshanqu'}, {'敖汉旗': 'aohanqi'}, {'新城区': 'xinchengqu8'}], ['hhht', {'和林格尔县': 'helingeerxian'}, {'回民区': 'huiminqu'}, {'土默特左旗': 'tumotezuoqi'}, {'托克托县': 'tuoketuoxian'}, {'新城区': 'xinchengqu1'}, {'武川县': 'wuchuanxian'}, {'清水河县': 'qingshuihexian'}, {'玉泉区': 'yuquanqu'}, {'赛罕区': 'saihanqu'}, {'金川开发区': 'jinchuankaifaqu1'}], ['yinchuan', {'兴庆区': 'xingqingqu'}, {'永宁县': 'yongningxian'}, {'灵武市': 'lingwushi'}, {'西夏区': 'xixiaqu'}, {'贺兰县': 'helanxian'}, {'金凤区': 'jinfengqu'}], ['heze', {'牡丹区': 'mudanqu'}, {'单县': 'shanxian'}, {'成武县': 'chengwuxian'}, {'定陶区': 'dingtaoqu'}, {'曹县': 'caoxian'}, {'巨野县': 'juyexian'}, {'东明县': 'dongmingxian'}, {'鄄城县': 'juanchengxian'}, {'郓城县': 'yunchengxian'}], ['jn', {'历下': 'lixia'}, {'市中': 'shizhong'}, {'天桥': 'tianqiao'}, {'历城': 'licheng'}, {'槐荫': 'huaiyin'}, {'高新': 'gaoxin'}, {'济阳': 'jiyang'}, {'商河': 'shanghe'}, {'平阴': 'pingyin'}, {'章丘': 'zhangqiu1'}, {'长清': 'changqing'}], ['jining', {'任城区': 'renchengqu'}, {'兖州区': 'yanzhouqu'}, {'嘉祥县': 'jiaxiangxian'}, {'微山县': 'weishanxian'}, {'曲阜市': 'qufushi'}, {'梁山县': 'liangshanxian'}, {'汶上县': 'wenshangxian'}, {'泗水县': 'sishuixian'}, {'邹城市': 'zouchengshi'}, {'金乡县': 'jinxiangxian'}, {'鱼台县': 'yutaixian'}], ['linyi', {'兰山区': 'lanshanqu'}, {'罗庄区': 'luozhuangqu'}, {'河东区': 'hedongqu'}, {'蒙阴县': 'mengyinxian'}, {'莒南县': 'junanxian'}, {'临沭县': 'linshuxian'}, {'平邑县': 'pingyixian'}, {'费县': 'feixian'}, {'沂水县': 'yishuixian'}, {'郯城县': 'tanchengxian'}, {'沂南县': 'yinanxian'}, {'兰陵县': 'lanlingxian'}], ['qd', {'市南': 'shinan'}, {'市北': 'shibei'}, {'李沧': 'licang'}, {'崂山': 'laoshan'}, {'黄岛': 'huangdao'}, {'城阳': 'chengyang'}, {'胶州': 'jiaozhou'}, {'即墨': 'jimo'}, {'平度': 'pingdu'}, {'莱西': 'laixi'}], ['ta', {'东平县': 'dongpingxian'}, {'宁阳县': 'ningyangxian'}, {'岱岳区': 'daiyuequ'}, {'新泰市': 'xintaishi'}, {'泰山区': 'taishanqu'}, {'肥城市': 'feichengshi'}], ['wf', {'临朐县': 'linquxian'}, {'坊子区': 'fangziqu'}, {'奎文区': 'kuiwenqu'}, {'安丘市': 'anqiushi'}, {'寒亭区': 'hantingqu'}, {'寿光市': 'shouguangshi'}, {'昌乐县': 'changlexian'}, {'昌邑市': 'changyishi'}, {'潍城区': 'weichengqu'}, {'诸城市': 'zhuchengshi'}, {'青州市': 'qingzhoushi'}, {'高密市': 'gaomishi'}, {'高新技术产业开发区': 'gaoxinjishuchanyekaifaqu'}], ['weihai', {'环翠区': 'huancuiqu'}, {'经区': 'jingqu1'}, {'高区': 'gaoqu1'}, {'荣成市': 'rongchengshi'}, {'文登区': 'wendengqu'}, {'乳山市': 'rushanshi'}], ['yt', {'芝罘': 'zhifu'}, {'莱山': 'laishan'}, {'福山': 'fushan'}, {'开发区': 'kaifaqu4'}, {'高新区': 'gaoxinqu'}, {'牟平': 'mouping'}, {'蓬莱': 'penglai'}, {'长岛县': 'changdaoxian'}, {'龙口': 'longkou'}, {'莱阳': 'laiyang'}, {'莱州': 'laizhou'}, {'海阳': 'haiyang'}], ['zb', {'临淄区': 'linziqu'}, {'博山区': 'boshanqu'}, {'周村区': 'zhoucunqu'}, {'张店区': 'zhangdianqu'}, {'桓台县': 'huantaixian'}, {'沂源县': 'yiyuanxian'}, {'淄川区': 'zichuanqu'}, {'经开区': 'jingkaiqu5'}, {'高新区': 'gaoxinqu7'}, {'高青县': 'gaoqingxian'}], ['bz', {'南江县': 'nanjiangxian'}, {'巴州区': 'bazhouqu'}, {'平昌县': 'pingchangxian'}, {'恩阳区': 'enyangqu'}, {'通江县': 'tongjiangxian'}, {'中坝区': 'zhongbaqu1'}], ['cd', {'锦江': 'jinjiang'}, {'青羊': 'qingyang'}, {'武侯': 'wuhou'}, {'高新': 'gaoxin7'}, {'成华': 'chenghua'}, {'金牛': 'jinniu'}, {'天府新区': 'tianfuxinqu'}, {'高新西': 'gaoxinxi1'}, {'双流': 'shuangliu'}, {'温江': 'wenjiang'}, {'郫都': 'pidou'}, {'龙泉驿': 'longquanyi'}, {'新都': 'xindou'}, {'天府新区南区': 'tianfuxinqunanqu'}, {'青白江': 'qingbaijiang'}, {'都江堰': 'doujiangyan'}, {'彭州': 'pengzhou'}, {'简阳': 'jianyang'}, {'新津': 'xinjin'}, {'崇州': 'chongzhou1'}, {'大邑': 'dayi'}, {'金堂': 'jintang'}, {'蒲江': 'pujiang'}, {'邛崃': 'qionglai'}], ['dy', {'旌阳区': 'jingyangqu'}, {'罗江县': 'luojiangxian'}, {'什邡市': 'shifangshi'}, {'广汉市': 'guanghanshi'}, {'绵竹市': 'mianzhushi'}, {'中江县': 'zhongjiangxian'}], ['dazhou', {'达川区': 'dachuanqu'}, {'通川区': 'tongchuanqu'}], ['guangyuan', {'利州区': 'lizhouqu'}, {'剑阁县': 'jiangexian'}, {'旺苍县': 'wangcangxian'}, {'昭化区': 'zhaohuaqu'}, {'朝天区': 'chaotianqu'}, {'苍溪县': 'cangxixian'}, {'青川县': 'qingchuanxian'}], ['liangshan', {'长安片区': 'changanpianqu'}, {'城南片区': 'chengnanpianqu1'}, {'老城片区': 'laochengpianqu'}, {'宁远桥片区': 'ningyuanqiaopianqu'}, {'邛海片区': 'qionghaipianqu'}, {'三岔口片区': 'sanchakoupianqu'}, {'市中心片区': 'shizhongxinpianqu'}, {'西部新城片区': 'xibuxinchengpianqu'}], ['mianyang', {'涪城区': 'fuchengqu'}, {'游仙区': 'youxianqu'}, {'安州区': 'anzhouqu'}, {'江油市': 'jiangyoushi'}, {'三台县': 'santaixian'}], ['nanchong', {'仪陇县': 'yilongxian'}, {'南部县': 'nanbuxian'}, {'嘉陵区': 'jialingqu'}, {'营山县': 'yingshanxian'}, {'蓬安县': 'penganxian'}, {'西充县': 'xichongxian'}, {'阆中市': 'langzhongshi'}, {'顺庆区': 'shunqingqu'}, {'高坪区': 'gaopingqu'}], ['sn', {'大英县': 'dayingxian'}, {'安居区': 'anjuqu'}, {'射洪县': 'shehongxian'}, {'船山区': 'chuanshanqu'}, {'蓬溪县': 'pengxixian'}], ['yibin', {'兴文县': 'xingwenxian'}, {'南溪区': 'nanxiqu'}, {'叙州区': 'xuzhouqu'}, {'屏山县': 'pingshanxian1'}, {'江安县': 'jianganxian'}, {'珙县': 'gongxian'}, {'筠连县': 'junlianxian'}, {'翠屏区': 'cuipingqu'}, {'长宁县': 'changningxian2'}, {'高县': 'gaoxian'}], ['baoji', {'凤县': 'fengxian3'}, {'凤翔县': 'fengxiangxian'}, {'千阳县': 'qianyangxian'}, {'太白县': 'taibaixian'}, {'岐山县': 'qishanxian'}, {'扶风县': 'fufengxian'}, {'渭滨区': 'weibinqu'}, {'眉县': 'meixian'}, {'金台区': 'jintaiqu'}, {'陇县': 'longxian'}, {'陈仓区': 'chencangqu'}, {'麟游县': 'linyouxian'}], ['hanzhong', {'汉台区': 'hantaiqu'}, {'南郑区': 'nanzhengqu'}], ['xa', {'碑林': 'beilin'}, {'未央': 'weiyang'}, {'灞桥': 'baqiao'}, {'新城区': 'xinchengqu'}, {'临潼': 'lintong'}, {'阎良': 'yanliang'}, {'长安': 'changan4'}, {'莲湖': 'lianhu'}, {'雁塔': 'yanta'}, {'蓝田': 'lantian'}, {'鄠邑区': 'huyiqu'}, {'周至': 'zhouzhi'}, {'高陵': 'gaoling1'}, {'西咸新区（西安）': 'xixianxinquxian'}], ['xianyang', {'泾阳县': 'jingyangxian'}, {'长武县': 'changwuxian'}, {'礼泉县': 'liquanxian'}, {'三原县': 'sanyuanxian'}, {'乾县': 'qianxian'}, {'旬邑县': 'xunyixian'}, {'渭城区': 'weichengqu2'}, {'秦都区': 'qinduqu'}, {'彬县': 'binxian1'}, {'永寿县': 'yongshouxian'}, {'淳化县': 'chunhuaxian'}, {'武功县': 'wugongxian'}, {'杨陵区': 'yanglingqu'}, {'兴平市': 'xingpingshi'}, {'西咸新区（咸阳）': 'xixianxinquxianyang'}], ['jz', {'介休市': 'jiexiushi'}, {'和顺县': 'heshunxian'}, {'太谷县': 'taiguxian'}, {'寿阳县': 'shouyangxian'}, {'左权县': 'zuoquanxian'}, {'平遥县': 'pingyaoxian'}, {'昔阳县': 'xiyangxian'}, {'榆次区': 'yuciqu1'}, {'榆社县': 'yushexian'}, {'灵石县': 'lingshixian'}, {'祁县': 'qixian2'}], ['ty', {'杏花岭区': 'xinghualingqu'}, {'迎泽区': 'yingzequ'}, {'万柏林区': 'wanbolinqu'}, {'小店区': 'xiaodianqu'}, {'尖草坪区': 'jiancaopingqu'}, {'晋源区': 'jinyuanqu'}, {'阳曲县': 'yangquxian'}, {'娄烦县': 'loufanxian'}, {'古交市': 'gujiaoshi'}, {'清徐县': 'qingxuxian'}], ['sh', {'浦东': 'pudong'}, {'闵行': 'minhang'}, {'宝山': 'baoshan'}, {'徐汇': 'xuhui'}, {'普陀': 'putuo'}, {'杨浦': 'yangpu'}, {'长宁': 'changning'}, {'松江': 'songjiang'}, {'嘉定': 'jiading'}, {'黄浦': 'huangpu'}, {'静安': 'jingan'}, {'虹口': 'hongkou'}, {'青浦': 'qingpu'}, {'奉贤': 'fengxian'}, {'金山': 'jinshan'}, {'崇明': 'chongming'}, {'上海周边': 'shanghaizhoubian'}], ['tj', {'和平': 'heping'}, {'南开': 'nankai'}, {'河西': 'hexi'}, {'河北': 'hebei'}, {'河东': 'hedong'}, {'红桥': 'hongqiao'}, {'西青': 'xiqing'}, {'北辰': 'beichen'}, {'东丽': 'dongli'}, {'津南': 'jinnan'}, {'塘沽': 'tanggu'}, {'开发区': 'kaifaqutj'}, {'武清': 'wuqing'}, {'滨海新区': 'binhaixinqu'}, {'宝坻': 'baodi'}, {'蓟州': 'jizhou'}, {'海河教育园区': 'haihejiaoyuyuanqu'}, {'静海': 'jinghai'}], ['wlmq', {'乌鲁木齐县': 'wulumuqixian'}, {'天山区': 'tianshanqu'}, {'头屯河区': 'toutunhequ'}, {'新市区': 'xinshiqu'}, {'水磨沟区': 'shuimogouqu'}, {'沙依巴克区': 'shayibakequ'}, {'米东区': 'midongqu'}, {'达坂城区': 'dabanchengqu'}], ['dali', {'凤仪': 'fengyi'}, {'古城': 'gucheng3'}, {'海东': 'haidong'}, {'经开区': 'jingkaiqu10'}, {'满江片区': 'manjiangpianqu'}, {'市区': 'shiqu'}, {'下关北区': 'xiaguanbeiqu'}], ['km', {'五华': 'wuhua'}, {'盘龙': 'panlong'}, {'官渡': 'guandu'}, {'西山': 'xishan23'}, {'呈贡': 'chenggong'}, {'晋宁': 'jinning'}, {'嵩明': 'songming'}, {'东川': 'dongchuan'}, {'富民': 'fumin'}, {'宜良': 'yiliang'}, {'石林': 'shilin'}, {'寻甸': 'xundian'}, {'禄劝': 'luquan1'}, {'安宁': 'anning'}], ['hz', {'西湖': 'xihu'}, {'大江东': 'dajiangdong1'}, {'钱塘新区': 'qiantangxinqu'}, {'下城': 'xiacheng'}, {'江干': 'jianggan'}, {'拱墅': 'gongshu'}, {'上城': 'shangcheng'}, {'滨江': 'binjiang'}, {'余杭': 'yuhang'}, {'萧山': 'xiaoshan'}, {'桐庐': 'tonglu1'}, {'淳安': 'chunan1'}, {'建德': 'jiande'}, {'富阳': 'fuyang'}, {'临安': 'linan'}], ['huzhou', {'南浔区': 'nanxunqu'}, {'长兴县': 'changxingxian'}, {'德清县': 'deqingxian2'}, {'吴兴区': 'wuxingqu'}, {'安吉县': 'anjixian'}], ['jx', {'南湖区': 'nanhuqu'}, {'桐乡市': 'tongxiangshi'}, {'嘉善县': 'jiashanxian'}, {'秀洲区': 'xiuzhouqu'}, {'海宁市': 'hainingshi1'}, {'海盐县': 'haiyanxian'}, {'平湖市': 'pinghushi'}], ['jh', {'东阳市': 'dongyangshi'}, {'义乌市': 'yiwushi'}, {'兰溪市': 'lanxishi'}, {'婺城区': 'wuchengqu'}, {'武义县': 'wuyixian'}, {'永康市': 'yongkangshi'}, {'浦江县': 'pujiangxian'}, {'磐安县': 'pananxian'}, {'金东区': 'jindongqu'}], ['nb', {'海曙区': 'haishuqu1'}, {'江北区': 'jiangbeiqu1'}, {'镇海区': 'zhenhaiqu1'}, {'北仑区': 'beilunqu1'}, {'鄞州区': 'yinzhouqu2'}, {'余姚市': 'yuyaoshi'}, {'慈溪市': 'cixishi'}, {'奉化区': 'fenghuaqu'}, {'象山县': 'xiangshanxian'}, {'宁海县': 'ninghaixian'}], ['quzhou', {'常山县': 'changshanxian'}, {'开化县': 'kaihuaxian'}, {'柯城区': 'kechengqu'}, {'江山市': 'jiangshanshi'}, {'衢江区': 'qujiangqu'}, {'龙游县': 'longyouxian'}], ['sx', {'上虞区': 'shangyuqu'}, {'嵊州市': 'shengzhoushi'}, {'新昌县': 'xinchangxian'}, {'柯桥区': 'keqiaoqu'}, {'诸暨市': 'zhujishi'}, {'越城区': 'yuechengqu'}], ['taizhou', {'三门县': 'sanmenxian'}, {'临海市': 'linhaishi'}, {'仙居县': 'xianjuxian'}, {'天台县': 'tiantaixian'}, {'椒江区': 'jiaojiangqu'}, {'温岭市': 'wenlingshi'}, {'玉环市': 'yuhuanshi'}, {'路桥区': 'luqiaoqu'}, {'黄岩区': 'huangyanqu'}], ['wz', {'鹿城区': 'luchengqu'}, {'瓯海区': 'ouhaiqu'}, {'龙湾区': 'longwanqu'}, {'乐清市': 'yueqingshi'}, {'瑞安市': 'ruianshi'}, {'苍南县': 'cangnanxian'}, {'平阳县': 'pingyangxian'}, {'洞头区': 'dongtouqu'}, {'泰顺县': 'taishunxian'}, {'永嘉县': 'yongjiaxian'}, {'龙港市': 'longgangshi'}], ['yw', {'北苑': 'beiyuan'}, {'城西': 'chengxi3'}, {'稠城': 'choucheng'}, {'稠江': 'choujiang'}, {'佛堂': 'fotang'}, {'福田': 'futian'}, {'后宅': 'houzhai'}, {'江东': 'jiangdong4'}, {'廿三里': 'niansanli'}, {'苏溪': 'suxi'}, {'义亭': 'yiting'}, {'义乌市': 'yiwushi1'}]]
'''


allinon = ['aq', 'hf', 'mas', 'wuhu', 'bj', 'cq', 'fz', 'quanzhou', 'xm', 'zhangzhou', 'dg', 'fs', 'gz', 'hui',
           'jiangmen',
           'qy', 'sz', 'zh', 'zhanjiang', 'zs', 'bh', 'fcg', 'gl', 'liuzhou', 'nn', 'lz', 'gy', 'bd', 'lf', 'sjz', 'ts',
           'zjk',
           'hk', 'san', 'cs', 'changde', 'yy', 'zhuzhou', 'kf', 'luoyang', 'xinxiang', 'xc', 'zz', 'zk', 'zmd', 'ez',
           'huangshi', 'wh', 'xy', 'yichang', 'hrb', 'ganzhou', 'jiujiang', 'jian', 'nc', 'sr', 'changzhou', 'haimen',
           'ha',
           'jy', 'ks', 'nj', 'nt', 'su', 'wx', 'xz', 'yc', 'zj', 'cc', 'jl', 'dl', 'dd', 'sy', 'baotou', 'cf', 'hhht',
           'yinchuan', 'heze', 'jn', 'jining', 'linyi', 'qd', 'ta', 'wf', 'weihai', 'yt', 'zb', 'bz', 'cd', 'dy',
           'dazhou',
           'guangyuan', 'liangshan', 'mianyang', 'nanchong', 'sn', 'yibin', 'baoji', 'hanzhong', 'xa', 'xianyang', 'jz',
           'ty',
           'sh', 'tj', 'wlmq', 'dali', 'km', 'hz', 'huzhou', 'jx', 'jh', 'nb', 'quzhou', 'sx', 'taizhou', 'wz', 'yw']

# allinon = ['cq']


def main():
    allRegionList = []
    for city in allinon:
        baseUrl = u"http://%s.lianjia.com/ershoufang/" % (city)
        datalist = getData(baseUrl,city)
        if len(datalist) == 0:

            continue
        print(datalist)
        allRegionList.append(datalist)

    print("===========")
    print(allRegionList)


findRegion = re.compile(r'在售二手房 ">(.*?)</a>')
findRegionCode = re.compile(r'<a href="/ershoufang/(.*?)/" title')


def getData(baseurl,city):
    html = askURL(baseurl)  # 保存获取到到网页源码
    # datalist = []

    # 2. 逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    # for item in soup.find_all('div', class_="ershoufang"):  # 每个省份
    # for item in soup.select('div.position > dl > dd > div > div '):  # 每个省份
    item = soup.select('div.position > dl > dd > div > div ')[0]
            # try:

    perCity = []
    perCity.append(city)
    item = str(item)
    regionName = re.findall(findRegion, item)
    regionCode = re.findall(findRegionCode, item)
    i = 0
    # print(regionName)
    # print(regionCode)
    for temp in regionName:
        regionSet = {temp: regionCode[i]}
        perCity.append(regionSet)
        i += 1
    # print(perCity)  # 示例：['aq', {'大观区': 'daguanqu'}, {'太湖县': 'taihuxian'}, {'宜秀区': 'yixiuqu'}, {'宿松县': 'susongxian'}, {'岳西县': 'yuexixian'}, {'怀宁县': 'huainingxian'}, {'望江县': 'wangjiangxian'}, {'桐城市': 'tongchengshi'}, {'潜山县': 'qianshanxian'}, {'迎江区': 'yingjiangqu'}]

    # datalist.append(perCity)
    time.sleep(1)
# except:
#     continue

    return perCity


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    print("爬取完毕")



'''
所有城市下属{行政区：代码}

[[['aq', {'大观区': 'daguanqu'}, {'太湖县': 'taihuxian'}, {'宜秀区': 'yixiuqu'}, {'宿松县': 'susongxian'}, 
{'岳西县': 'yuexixian'}, {'怀宁县': 'huainingxian'}, {'望江县': 'wangjiangxian'}, {'桐城市': 'tongchengshi'}, 
{'潜山县': 'qianshanxian'}, {'迎江区': 'yingjiangqu'}]], [['hf', {'包河': 'baohe'}, {'巢湖市': 'chaohushi'}, 
{'庐江县': 'lujiangxian'}, {'空港经济示范区': 'konggangjingjishifanqu'}, {'蜀山': 'shushan'}, {'庐阳': 'luyang'}, {'瑶海': 'yaohai'}, 
{'政务': 'zhengwu'}, {'滨湖新区': 'binhuxinqu'}, {'经开': 'jingkai2'}, {'高新': 'gaoxin8'}, {'新站': 'xinzhan'}, 
{'肥东': 'feidong'}, {'肥西': 'feixi'}, {'长丰': 'changfeng'}]], [['mas', {'博望区': 'bowangqu'}, {'含山县': 'hanshanxian'}, 
{'和县': 'hexian'}, {'当涂县': 'dangtuxian'}, {'花山区': 'huashanqu'}, {'雨山区': 'yushanqu'}]], [['wuhu', {'三山区': 'sanshanqu'}, 
{'南陵县': 'nanlingxian'}, {'弋江区': 'yijiangqu'}, {'无为县': 'wuweixian'}, {'繁昌县': 'fanchangxian'}, {'经济开发区': 
'jingjikaifaqu'}, {'芜湖县': 'wuhuxian'}, {'镜湖区': 'jinghuqu'}, {'鸠江区': 'jiujiangqu'}]], [['fz', {'鼓楼区': 'gulouqu3'}, 
{'台江区': 'taijiangqu1'}, {'晋安区': 'jinanqu1'}, {'马尾区': 'maweiqu1'}, {'仓山区': 'cangshanqu1'}, {'闽侯县': 'minhouxian'}, 
{'连江县': 'lianjiangxian'}, {'平潭县': 'pingtanxian'}, {'福清市': 'fuqingshi'}]], [['quanzhou', {'惠安县': 'huianxian1'}, 
{'晋江市': 'jinjiangshi'}, {'石狮市': 'shishishi'}, {'南安市': 'nananshi'}, {'永春县': 'yongchunxian'}, {'德化县': 'dehuaxian'}, 
{'洛江区': 'luojiangqu1'}, {'泉港区': 'quangangqu'}, {'鲤城区': 'lichengqu1'}, {'安溪县': 'anxixian'}, {'丰泽区': 'fengzequ1'}, 
{'金门县': 'jinmenxian'}]], [['zhangzhou', {'龙文区': 'longwenqu1'}, {'芗城区': 'xiangchengqu3'}, {'漳州港': 'zhangzhougang1'}, 
{'角美台商投资区': 'jiaomeitaishangtouziqu1'}, {'龙海市': 'longhaishi'}, {'长泰县': 'changtaixian1'}, {'南靖县': 'nanjingxian1'}, 
{'平和县': 'pinghexian1'}, {'华安县': 'huaanxian'}, {'漳浦县': 'zhangpuxian1'}, {'东山县': 'dongshanxian'}, 
{'诏安县': 'zhaoanxian'}, {'云霄县': 'yunxiaoxian'}]], [['hui', {'惠城': 'huicheng'}, {'仲恺高新技术产业开发区': 
'zhongkaigaoxinjishuchanyekaifaqu'}, {'惠阳': 'huiyang'}, {'大亚湾': 'dayawan'}, {'惠东': 'huidong'}, {'博罗': 'boluo'}]], 
[['jiangmen', {'江海区': 'jianghaiqu'}, {'蓬江区': 'pengjiangqu'}, {'新会区': 'xinhuiqu'}, {'台山市': 'taishanshi'}, 
{'鹤山市': 'heshanshi'}, {'恩平市': 'enpingshi'}, {'开平市': 'kaipingshi'}]], [['qy', {'佛冈县': 'fogangxian'}, 
{'清城区': 'qingchengqu'}, {'清新区': 'qingxinqu'}, {'英德市': 'yingdeshi'}, {'连南瑶族自治县': 'liannanyaozuzizhixian'}, 
{'连山壮族瑶族自治县': 'lianshanzhuangzuyaozuzizhixian'}, {'连州市': 'lianzhoushi'}, {'阳山县': 'yangshanxian'}]], [['zh', 
{'香洲区': 'xiangzhouqu'}, {'金湾区': 'jinwanqu'}, {'斗门区': 'doumenqu'}]], [['zhanjiang', {'霞山区': 'xiashanqu'}, 
{'赤坎区': 'chikanqu'}, {'坡头区': 'potouqu'}, {'麻章区': 'mazhangqu'}, {'遂溪县': 'suixixian'}, {'廉江市': 'lianjiangshi'}, 
{'吴川市': 'wuchuanshi'}, {'雷州市': 'leizhoushi'}, {'徐闻县': 'xuwenxian'}]], [['zs', {'小榄镇': 'xiaolanzhen'}, 
{'板芙镇': 'banfuzhen'}, {'横栏镇': 'henglanzhen'}, {'民众镇': 'minzhongzhen'}, {'神湾镇': 'shenwanzhen'}, {'阜沙镇': 'fushazhen'}, 
{'黄圃镇': 'huangpuzhen'}, {'三乡镇': 'sanxiangzhen'}, {'三角镇': 'sanjiaozhen'}, {'东凤镇': 'dongfengzhen'}, {'东区': 'dongqu'}, 
{'东升镇': 'dongshengzhen1'}, {'南头镇': 'nantouzhen'}, {'南朗镇': 'nanlangzhen'}, {'古镇镇': 'guzhenzhen'}, 
{'坦洲镇': 'tanzhouzhen'}, {'大涌镇': 'dayongzhen'}, {'西区': 'xiqu'}, {'南区': 'nanqu'}, {'石岐区': 'shiqiqu'}, {'火炬': 'huoju'}, 
{'港口镇': 'gangkouzhen'}, {'沙溪镇': 'shaxizhen'}, {'五桂山': 'wuguishan'}]], [['bh', {'合浦县': 'hepuxian'}, 
{'海城区': 'haichengqu'}, {'铁山港区': 'tieshangangqu'}, {'银海区': 'yinhaiqu'}]], [['fcg', {'港口区': 'gangkouqu'}, 
{'防城区': 'fangchengqu'}]], [['gl', {'七星区': 'qixingqu'}, {'临桂区': 'linguiqu'}, {'象山区': 'xiangshanqu'}, 
{'秀峰区': 'xiufengqu'}, {'叠彩区': 'diecaiqu'}, {'雁山区': 'yanshanqu'}, {'灌阳县': 'guanyangxian'}, {'桂北新区（灵川县）': 
'guibeixinqulingchuanxian1'}, {'龙胜各族自治县': 'longshenggezuzizhixian'}, {'永福县': 'yongfuxian'}, {'平乐县': 'pinglexian'}, 
{'恭城瑶族自治县': 'gongchengyaozuzizhixian'}, {'资源县': 'ziyuanxian'}, {'全州县': 'quanzhouxian'}, {'荔浦县': 'lipuxian'}, 
{'兴安县': 'xinganxian'}, {'阳朔县': 'yangshuoxian'}]], [['liuzhou', {'三江侗族自治县': 'sanjiangdongzuzizhixian'}, 
{'城中区': 'chengzhongqu2'}, {'柳北区': 'liubeiqu'}, {'柳南区': 'liunanqu'}, {'柳城县': 'liuchengxian'}, {'柳江区': 'liujiangqu'}, 
{'融安县': 'ronganxian'}, {'融水苗族自治县': 'rongshuimiaozuzizhixian'}, {'鱼峰区': 'yufengqu'}, {'鹿寨县': 'luzhaixian'}]], [['nn', 
{'青秀区': 'qingxiuqu'}, {'江南区': 'jiangnanqu'}, {'西乡塘区': 'xixiangtangqu'}, {'兴宁区': 'xingningqu'}, {'邕宁区': 'yongningqu'}, 
{'良庆区': 'liangqingqu'}, {'武鸣县': 'wumingxian'}, {'宾阳县': 'binyangxian'}, {'上林县': 'shanglinxian'}, 
{'马山县': 'mashanxian'}, {'横县': 'hengxian'}, {'隆安县': 'longanxian'}]], [['lz', {'七里河区': 'qilihequ'}, 
{'兰州新区': 'lanzhouxinqu'}, {'城关区': 'chengguanqu'}, {'安宁区': 'anningqu'}, {'榆中县': 'yuzhongxian'}, 
{'永登县': 'yongdengxian'}, {'皋兰县': 'gaolanxian'}, {'红古区': 'hongguqu'}, {'西固区': 'xiguqu'}]], [['gy', 
{'云岩区': 'yunyanqu'}, {'白云区': 'baiyunqu'}, {'乌当区': 'wudangqu'}, {'南明区': 'nanmingqu'}, {'花溪区': 'huaxiqu'}, 
{'息烽县': 'xifengxian'}, {'开阳县': 'kaiyangxian'}, {'修文县': 'xiuwenxian'}, {'清镇市': 'qingzhenshi'}, 
{'观山湖区': 'guanshanhuqu'}]], [['bd', {'涞水': 'laishui1'}, {'涿州': 'zhuozhou1'}, {'易县': 'yixian'}, 
{'高碑店': 'gaobeidian1'}, {'竞秀区': 'jingxiuqu'}, {'莲池区': 'lianchiqu'}, {'满城区': 'manchengqu'}, {'清苑区': 'qingyuanqu'}, 
{'徐水区': 'xushuiqu'}, {'安国市': 'anguoshi'}, {'定州市': 'dingzhoushi'}, {'博野县': 'boyexian'}, {'涞源县': 'laiyuanxian'}, 
{'唐县': 'tangxian'}, {'定兴县': 'dingxingxian'}, {'望都县': 'wangduxian'}, {'曲阳县': 'quyangxian'}, {'顺平县': 'shunpingxian'}, 
{'蠡县': 'lixian1'}, {'高阳县': 'gaoyangxian'}, {'阜平县': 'fupingxian2'}]], [['lf', {'燕郊': 'yanjiao'}, {'香河': 'xianghe'}, 
{'广阳': 'guangyang'}, {'安次': 'anci'}, {'廊坊经济技术开发区': 'langfangjingjijishu'}, {'固安': 'guan'}, {'大厂': 'dachang'}, 
{'永清': 'yongqing'}]], [['ts', {'丰南区': 'fengnanqu'}, {'丰润区': 'fengrunqu'}, {'乐亭县': 'laotingxian'}, {'古冶区': 'guyequ'}, 
{'开平区': 'kaipingqu'}, {'曹妃甸区': 'caofeidianqu'}, {'滦南县': 'luannanxian'}, {'滦州市': 'luanzhoushi'}, 
{'玉田县': 'yutianxian'}, {'路北区': 'lubeiqu'}, {'路南区': 'lunanqu'}, {'迁安市': 'qiananshi'}, {'迁西县': 'qianxixian'}, 
{'遵化市': 'zunhuashi'}]], [['zjk', {'万全区': 'wanquanqu'}, {'下花园': 'xiahuayuan'}, {'宣化区': 'xuanhuaqu'}, 
{'尚义县': 'shangyixian'}, {'崇礼区': 'chongliqu1'}, {'崇礼县': 'chonglixian'}, {'康保县': 'kangbaoxian'}, 
{'张北县': 'zhangbeixian'}, {'怀安县': 'huaianxian'}, {'怀来县': 'huailaixian'}, {'桥东区': 'qiaodongqu3'}, {'桥西区': 'qiaoxiqu3'}, 
{'沽源县': 'guyuanxian'}, {'涿鹿县': 'zhuoluxian'}, {'蔚县': 'weixian3'}, {'赤城县': 'chichengxian'}, {'阳原县': 'yangyuanxian'}]], 
[['hk', {'秀英': 'xiuyingqu2'}, {'龙华': 'longhuaqu1'}, {'美兰': 'meilanqu1'}, {'琼山': 'qiongshanqu1'}]], [['san', 
{'崖州': 'yazhou1'}, {'天涯': 'tianya1'}, {'海棠': 'haitang1'}, {'吉阳': 'jiyang3'}]], [['changde', {'临澧县': 'linlixian'}, 
{'安乡县': 'anxiangxian'}, {'桃源县': 'taoyuanxian'}, {'武陵区': 'wulingqu'}, {'汉寿县': 'hanshouxian'}, {'津市市': 'jinshishi'}, 
{'澧县': 'lixian4'}, {'石门县': 'shimenxian'}, {'鼎城区': 'dingchengqu'}]], [['yy', {'岳阳楼区': 'yueyanglouqu'}, 
{'岳阳县': 'yueyangxian'}, {'湘阴县': 'xiangyinxian'}, {'平江县': 'pingjiangxian'}, {'君山区': 'junshanqu'}, {'汨罗市': 'miluoshi'}, 
{'云溪区': 'yunxiqu'}, {'华容县': 'huarongxian'}, {'临湘市': 'linxiangshi'}]], [['zhuzhou', {'天元区': 'tianyuanqu'}, 
{'芦淞区': 'lusongqu'}, {'荷塘区': 'hetangqu'}, {'石峰区': 'shifengqu'}, {'醴陵市': 'lilingshi'}, {'炎陵县': 'yanlingxian1'}, 
{'株洲县': 'zhuzhouxian'}, {'攸县': 'youxian'}, {'茶陵县': 'chalingxian'}]], [['kf', {'龙亭区': 'longtingqu'}, 
{'杞县': 'qixian3'}, {'兰考县': 'lankaoxian'}, {'通许县': 'tongxuxian'}, {'祥符区': 'xiangfuqu'}, {'尉氏县': 'weishixian'}, 
{'鼓楼区': 'gulouqu6'}, {'顺河区': 'shunhequ1'}, {'禹王台区': 'yuwangtaiqu'}]], [['luoyang', {'洛龙区': 'luolongqu'}, 
{'涧西区': 'jianxiqu'}, {'西工区': 'xigongqu'}, {'瀍河回族区': 'chanhehuizuqu'}, {'老城区': 'laochengqu1'}, {'伊川县': 'yichuanxian'}, 
{'伊滨区': 'yibinqu1'}, {'偃师市': 'yanshishi'}, {'吉利区': 'jiliqu'}, {'孟津县': 'mengjinxian'}, {'宜阳县': 'yiyangxian'}, 
{'嵩县': 'songxian'}, {'新安县': 'xinanxian'}, {'栾川县': 'luanchuanxian'}, {'汝阳县': 'ruyangxian'}, {'洛宁县': 'luoningxian'}]], 
[['xinxiang', {'红旗区': 'hongqiqu'}, {'卫滨区': 'weibinqu2'}, {'牧野区': 'muyequ'}]], [['xc', {'建安区': 'jiananqu'}, 
{'禹州市': 'yuzhoushi'}, {'襄城县': 'xiangchengxian2'}, {'鄢陵县': 'yanlingxian'}, {'长葛市': 'changgeshi'}, 
{'魏都区': 'weiduqu'}]], [['zk', {'商水县': 'shangshuixian'}, {'太康县': 'taikangxian'}, {'川汇区': 'chuanhuiqu'}, 
{'扶沟县': 'fugouxian'}, {'沈丘县': 'chenqiuxian'}, {'淮阳县': 'huaiyangxian'}, {'西华县': 'xihuaxian'}, {'郸城县': 'danchengxian'}, 
{'项城市': 'xiangchengshi'}, {'鹿邑县': 'luyixian'}]], [['zmd', {'上蔡县': 'shangcaixian'}, {'平舆县': 'pingyuxian'}, 
{'新蔡县': 'xincaixian'}, {'正阳县': 'zhengyangxian'}, {'汝南县': 'runanxian'}, {'泌阳县': 'biyangxian'}, {'确山县': 'queshanxian'}, 
{'西平县': 'xipingxian'}, {'遂平县': 'suipingxian'}, {'驿城区': 'yichengqu1'}]], [['ez', {'鄂城区': 'echengqu'}, 
{'葛店开发区': 'gediankaifaqu'}, {'梁子湖区': 'liangzihuqu'}, {'华容区': 'huarongqu'}]], [['huangshi', {'西塞山区': 'xisaishanqu'}, 
{'黄石港区': 'huangshigangqu'}, {'阳新县': 'yangxinxian2'}, {'铁山区': 'tieshanqu'}, {'下陆区': 'xialuqu'}, {'大冶市': 'dayeshi'}]], 
[['xy', {'襄城区': 'xiangchengqu1'}, {'襄州区': 'xiangzhouqu1'}, {'樊城区': 'fanchengqu'}]], [['yichang', {'西陵区': 'xilingqu'}, 
{'伍家岗区': 'wujiagangqu'}, {'夷陵区': 'yilingqu'}, {'宜都市': 'yidushi'}, {'枝江市': 'zhijiangshi'}, {'当阳市': 'dangyangshi'}, 
{'秭归县': 'ziguixian'}, {'猇亭区': 'xiaotingqu'}, {'点军区': 'dianjunqu'}, {'兴山县': 'xingshanxian'}, {'远安县': 'yuananxian'}, 
{'五峰土家族自治县': 'wufengtujiazuzizhixian'}, {'长阳土家族自治县': 'changyangtujiazuzizhixian'}]], [['hrb', {'平房': 'pingfang'}, 
{'道外': 'daowai'}, {'道里': 'daoli'}, {'南岗': 'nangang'}, {'香坊': 'xiangfang'}, {'松北': 'songbei'}, {'尚志市': 'shangzhishi'}, 
{'巴彦县': 'bayanxian'}, {'呼兰区': 'hulanqu'}, {'阿城区': 'achengqu'}, {'延寿县': 'yanshouxian'}, {'依兰县': 'yilanxian'}, 
{'木兰县': 'mulanxian'}, {'宾县': 'binxian'}, {'通河县': 'tonghexian'}, {'五常市': 'wuchangshi'}, {'双城区': 'shuangchengqu'}, 
{'方正县': 'fangzhengxian'}, {'肇东市': 'zhaodongshi2'}]], [['ganzhou', {'章贡区': 'zhanggongqu'}, {'赣县区': 'ganxianqu'}, 
{'南康区': 'nankangqu'}, {'于都县': 'yuduxian'}, {'瑞金市': 'ruijinshi'}, {'宁都县': 'ningduxian'}, {'上犹县': 'shangyouxian'}, 
{'会昌县': 'huichangxian'}, {'信丰县': 'xinfengxian'}, {'全南县': 'quannanxian'}, {'兴国县': 'xingguoxian'}, {'大余县': 'dayuxian'}, 
{'安远县': 'anyuanxian'}, {'定南县': 'dingnanxian'}, {'寻乌县': 'xunwuxian'}, {'崇义县': 'chongyixian'}, {'石城县': 'shichengxian'}, 
{'龙南县': 'longnanxian'}]], [['jiujiang', {'修水县': 'xiushuixian'}, {'共青城市': 'gongqingchengshi'}, {'庐山市': 'lushanshi'}, 
{'彭泽县': 'pengzexian'}, {'德安县': 'deanxian'}, {'柴桑区': 'chaisangqu'}, {'武宁县': 'wuningxian'}, {'永修县': 'yongxiuxian'}, 
{'浔阳区': 'xunyangqu'}, {'湖口县': 'hukouxian'}, {'濂溪区': 'lianxiqu'}, {'瑞昌市': 'ruichangshi'}, {'都昌县': 'duchangxian'}]], 
[['jian', {'吉州区': 'jizhouqu2'}, {'青原区': 'qingyuanqu2'}, {'吉安县': 'jianxian'}, {'吉水县': 'jishuixian'}, 
{'泰和县': 'taihexian2'}, {'安福县': 'anfuxian'}, {'永新县': 'yongxinxian'}, {'永丰县': 'yongfengxian'}, {'遂川县': 'suichuanxian'}, 
{'峡江县': 'xiajiangxian'}]], [['nc', {'东湖区': 'donghuqu'}, {'南昌县': 'nanchangxian'}, {'安义县': 'anyixian'}, 
{'新建区': 'xinjianqu'}, {'湾里区': 'wanliqu'}, {'红谷滩': 'honggutan1'}, {'西湖区': 'xihuqu'}, {'进贤县': 'jinxianxian'}, 
{'青云谱区': 'qingyunpuqu'}, {'青山湖区': 'qingshanhuqu'}, {'高新区': 'gaoxinqu11'}, {'经开区': 'jingkaiqu8'}]], [['sr', 
{'上饶县': 'shangraoxian'}, {'信州区': 'xinzhouqu'}, {'广丰区': 'guangfengqu'}]], [['changzhou', {'武进区': 'wujinqu'}, 
{'金坛区': 'jintanqu'}, {'钟楼区': 'zhonglouqu'}, {'溧阳市': 'liyangshi'}, {'天宁区': 'tianningqu'}, {'新北区': 'xinbeiqu'}]], 
[['haimen', {'包场': 'baochang'}, {'滨江': 'binjiang3'}, {'川姜': 'chuanjiang'}, {'海门': 'haimen1'}, {'海门市': 'haimenshi1'}, 
{'姜灶': 'jiangzao'}, {'金新': 'jinxin'}, {'临江': 'linjiang'}, {'启东市': 'qidongshi1'}, {'三厂': 'sanchang'}, {'三余': 'sanyu'}, 
{'四甲': 'sijia'}, {'张芝山': 'zhangzhishan'}]], [['ha', {'清江浦区': 'qingjiangpuqu'}, {'淮阴区': 'huaiyinqu'}, 
{'淮安区': 'huaianqu'}, {'洪泽区': 'hongzequ'}, {'涟水县': 'lianshuixian'}]], [['jy', {'长泾镇': 'changjingzhen'}, 
{'澄江街道': 'chengjiangjiedao'}, {'高新区': 'gaoxinqu14'}, {'顾山镇': 'gushanzhen'}, {'璜土镇': 'huangtuzhen'}, 
{'华士镇': 'huashizhen'}, {'江阴': 'jiangyin'}, {'临港经济开发区': 'lingangjingjikaifaqu'}, {'南闸街道': 'nanzhajiedao'}, 
{'青阳镇': 'qingyangzhen'}, {'新桥镇': 'xinqiaozhen'}, {'徐霞客镇': 'xuxiakezhen'}, {'月城镇': 'yuechengzhen'}, 
{'云亭街道': 'yuntingjiedao'}, {'周庄镇': 'zhouzhuangzhen'}, {'祝塘镇': 'zhutangzhen'}]], [['ks', {'巴城': 'bacheng'}, 
{'淀山湖': 'dianshanhu'}, {'花桥': 'huaqiao'}, {'锦溪': 'jinxi'}, {'开发区': 'kaifaqu5'}, {'陆家': 'lujia'}, {'甪直': 'luzhi'}, 
{'千灯': 'qiandeng'}, {'玉山城北': 'yushanchengbei'}, {'玉山城南': 'yushanchengnan'}, {'玉山城西': 'yushanchengxi'}, 
{'玉山高新区': 'yushangaoxinqu'}, {'玉山老城区': 'yushanlaochengqu'}, {'张浦': 'zhangpu'}, {'周市': 'zhoushi'}, 
{'周庄': 'zhouzhuang'}]], [['nt', {'南通经济技术开发区': 'nantongjingjijishukaifaqu'}, {'启东市': 'qidongshi'}, 
{'如东县': 'rudongxian'}, {'如皋市': 'rugaoshi'}, {'崇川区': 'chongchuanqu'}, {'海安县': 'haianxian'}, {'海门区': 'haimenqu'}, 
{'港闸区': 'gangzhaqu'}, {'通州区': 'tongzhouqu'}]], [['xz', {'云龙区': 'yunlongqu'}, {'鼓楼区': 'gulouqu1'}, 
{'泉山区': 'quanshanqu'}, {'铜山区': 'tongshanqu'}, {'金山桥开发区': 'jinshanqiaokaifaqu'}, {'新城区': 'xinchengqu3'}, 
{'贾汪区': 'jiawangqu'}, {'邳州市': 'pizhoushi'}, {'新沂市': 'xinyishi'}, {'睢宁县': 'suiningxian'}, {'沛县': 'peixian'}, 
{'丰县': 'fengxian1'}]], [['yc', {'东台市': 'dongtaishi'}, {'亭湖区': 'tinghuqu'}, {'响水县': 'xiangshuixian'}, 
{'大丰区': 'dafengqu'}, {'射阳县': 'sheyangxian'}, {'建湖县': 'jianhuxian'}, {'滨海县': 'binhaixian'}, {'盐都区': 'yanduqu'}, 
{'阜宁县': 'funingxian'}]], [['zj', {'丹徒区': 'dantuqu'}, {'丹阳市': 'danyangshi'}, {'京口': 'jingkou'}, {'句容': 'jurong'}, 
{'扬中市': 'yangzhongshi'}, {'润州': 'runzhou'}]], [['cc', {'九台区': 'jiutaiqu'}, {'二道区': 'erdaoqu'}, {'农安县': 'nonganxian'}, 
{'朝阳区': 'chaoyangqu'}, {'南关区': 'nanguanqu'}, {'双阳区': 'shuangyangqu'}, {'宽城区': 'kuanchengqu'}, {'德惠市': 'dehuishi'}, 
{'净月区': 'jingyuequ'}, {'榆树市': 'yushushi'}, {'汽车产业开发区': 'qichechanyekaifaqu'}, {'经开北区': 'jingkaibeiqu'}, 
{'经开区': 'jingkaiqu1'}, {'绿园区': 'lvyuanqu'}, {'高新北区': 'gaoxinbeiqu'}, {'高新区': 'gaoxinqu16'}]], [['jl', 
{'丰满区': 'fengmanqu'}, {'船营区': 'chuanyingqu'}, {'昌邑区': 'changyiqu'}, {'龙潭区': 'longtanqu'}, {'桦甸市': 'huadianshi'}, 
{'永吉县': 'yongjixian'}, {'磐石市': 'panshishi'}, {'舒兰市': 'shulanshi'}, {'蛟河市': 'jiaoheshi'}]], [['dd', 
{'东港市': 'donggangshi'}, {'元宝区': 'yuanbaoqu'}, {'凤城市': 'fengchengshi'}, {'宽甸满族自治县': 'kuandianmanzuzizhixian'}, 
{'振兴区': 'zhenxingqu'}, {'振安区': 'zhenanqu'}]], [['baotou', {'东河区': 'donghequ'}, {'石拐区': 'shiguaiqu'}, 
{'青山区': 'qingshanqu'}, {'九原区': 'jiuyuanqu'}, {'白云鄂博矿区': 'baiyunebokuangqu'}, {'昆都仑区': 'kundoulunqu'}, 
{'土默特右旗': 'tumoteyouqi'}, {'达尔罕茂明安联合旗': 'daerhanmaominganlianheqi'}, {'固阳县': 'guyangxian'}, {'稀土高新区': 
'xitugaoxinqu'}, {'滨河新区': 'binhexinqu'}]], [['cf', {'宁城县': 'ningchengxian'}, {'元宝山区': 'yuanbaoshanqu'}, 
{'喀喇沁旗': 'kalaqinqi'}, {'克什克腾旗': 'keshiketengqi'}, {'林西县': 'linxixian'}, {'巴林左旗': 'balinzuoqi'}, 
{'巴林右旗': 'balinyouqi'}, {'翁牛特旗': 'wengniuteqi'}, {'松山区': 'songshanqu'}, {'阿鲁科尔沁旗': 'alukeerqinqi'}, 
{'红山区': 'hongshanqu'}, {'敖汉旗': 'aohanqi'}, {'新城区': 'xinchengqu8'}]], [['hhht', {'和林格尔县': 'helingeerxian'}, 
{'回民区': 'huiminqu'}, {'土默特左旗': 'tumotezuoqi'}, {'托克托县': 'tuoketuoxian'}, {'新城区': 'xinchengqu1'}, 
{'武川县': 'wuchuanxian'}, {'清水河县': 'qingshuihexian'}, {'玉泉区': 'yuquanqu'}, {'赛罕区': 'saihanqu'}, {'金川开发区': 
'jinchuankaifaqu1'}]], [['yinchuan', {'兴庆区': 'xingqingqu'}, {'永宁县': 'yongningxian'}, {'灵武市': 'lingwushi'}, 
{'西夏区': 'xixiaqu'}, {'贺兰县': 'helanxian'}, {'金凤区': 'jinfengqu'}]], [['heze', {'牡丹区': 'mudanqu'}, {'单县': 'shanxian'}, 
{'成武县': 'chengwuxian'}, {'定陶区': 'dingtaoqu'}, {'曹县': 'caoxian'}, {'巨野县': 'juyexian'}, {'东明县': 'dongmingxian'}, 
{'鄄城县': 'juanchengxian'}, {'郓城县': 'yunchengxian'}]], [['jn', {'历下': 'lixia'}, {'市中': 'shizhong'}, {'天桥': 'tianqiao'}, 
{'历城': 'licheng'}, {'槐荫': 'huaiyin'}, {'高新': 'gaoxin'}, {'济阳': 'jiyang'}, {'商河': 'shanghe'}, {'平阴': 'pingyin'}, 
{'章丘': 'zhangqiu1'}, {'长清': 'changqing'}]], [['jining', {'任城区': 'renchengqu'}, {'兖州区': 'yanzhouqu'}, 
{'嘉祥县': 'jiaxiangxian'}, {'微山县': 'weishanxian'}, {'曲阜市': 'qufushi'}, {'梁山县': 'liangshanxian'}, 
{'汶上县': 'wenshangxian'}, {'泗水县': 'sishuixian'}, {'邹城市': 'zouchengshi'}, {'金乡县': 'jinxiangxian'}, 
{'鱼台县': 'yutaixian'}]], [['linyi', {'兰山区': 'lanshanqu'}, {'罗庄区': 'luozhuangqu'}, {'河东区': 'hedongqu'}, 
{'蒙阴县': 'mengyinxian'}, {'莒南县': 'junanxian'}, {'临沭县': 'linshuxian'}, {'平邑县': 'pingyixian'}, {'费县': 'feixian'}, 
{'沂水县': 'yishuixian'}, {'郯城县': 'tanchengxian'}, {'沂南县': 'yinanxian'}, {'兰陵县': 'lanlingxian'}]], [['ta', 
{'东平县': 'dongpingxian'}, {'宁阳县': 'ningyangxian'}, {'岱岳区': 'daiyuequ'}, {'新泰市': 'xintaishi'}, {'泰山区': 'taishanqu'}, 
{'肥城市': 'feichengshi'}]], [['wf', {'临朐县': 'linquxian'}, {'坊子区': 'fangziqu'}, {'奎文区': 'kuiwenqu'}, 
{'安丘市': 'anqiushi'}, {'寒亭区': 'hantingqu'}, {'寿光市': 'shouguangshi'}, {'昌乐县': 'changlexian'}, {'昌邑市': 'changyishi'}, 
{'潍城区': 'weichengqu'}, {'诸城市': 'zhuchengshi'}, {'青州市': 'qingzhoushi'}, {'高密市': 'gaomishi'}, {'高新技术产业开发区': 
'gaoxinjishuchanyekaifaqu'}]], [['weihai', {'环翠区': 'huancuiqu'}, {'经区': 'jingqu1'}, {'高区': 'gaoqu1'}, 
{'荣成市': 'rongchengshi'}, {'文登区': 'wendengqu'}, {'乳山市': 'rushanshi'}]], [['yt', {'芝罘': 'zhifu'}, {'莱山': 'laishan'}, 
{'福山': 'fushan'}, {'开发区': 'kaifaqu4'}, {'高新区': 'gaoxinqu'}, {'牟平': 'mouping'}, {'蓬莱': 'penglai'}, 
{'长岛县': 'changdaoxian'}, {'龙口': 'longkou'}, {'莱阳': 'laiyang'}, {'莱州': 'laizhou'}, {'海阳': 'haiyang'}]], [['zb', 
{'临淄区': 'linziqu'}, {'博山区': 'boshanqu'}, {'周村区': 'zhoucunqu'}, {'张店区': 'zhangdianqu'}, {'桓台县': 'huantaixian'}, 
{'沂源县': 'yiyuanxian'}, {'淄川区': 'zichuanqu'}, {'经开区': 'jingkaiqu5'}, {'高新区': 'gaoxinqu7'}, {'高青县': 'gaoqingxian'}]], 
[['bz', {'南江县': 'nanjiangxian'}, {'巴州区': 'bazhouqu'}, {'平昌县': 'pingchangxian'}, {'恩阳区': 'enyangqu'}, 
{'通江县': 'tongjiangxian'}, {'中坝区': 'zhongbaqu1'}]], [['dy', {'旌阳区': 'jingyangqu'}, {'罗江县': 'luojiangxian'}, 
{'什邡市': 'shifangshi'}, {'广汉市': 'guanghanshi'}, {'绵竹市': 'mianzhushi'}, {'中江县': 'zhongjiangxian'}]], [['dazhou', 
{'达川区': 'dachuanqu'}, {'通川区': 'tongchuanqu'}]], [['guangyuan', {'利州区': 'lizhouqu'}, {'剑阁县': 'jiangexian'}, 
{'旺苍县': 'wangcangxian'}, {'昭化区': 'zhaohuaqu'}, {'朝天区': 'chaotianqu'}, {'苍溪县': 'cangxixian'}, 
{'青川县': 'qingchuanxian'}]], [['liangshan', {'长安片区': 'changanpianqu'}, {'城南片区': 'chengnanpianqu1'}, 
{'老城片区': 'laochengpianqu'}, {'宁远桥片区': 'ningyuanqiaopianqu'}, {'邛海片区': 'qionghaipianqu'}, {'三岔口片区': 
'sanchakoupianqu'}, {'市中心片区': 'shizhongxinpianqu'}, {'西部新城片区': 'xibuxinchengpianqu'}]], [['mianyang', 
{'涪城区': 'fuchengqu'}, {'游仙区': 'youxianqu'}, {'安州区': 'anzhouqu'}, {'江油市': 'jiangyoushi'}, {'三台县': 'santaixian'}]], 
[['nanchong', {'仪陇县': 'yilongxian'}, {'南部县': 'nanbuxian'}, {'嘉陵区': 'jialingqu'}, {'营山县': 'yingshanxian'}, 
{'蓬安县': 'penganxian'}, {'西充县': 'xichongxian'}, {'阆中市': 'langzhongshi'}, {'顺庆区': 'shunqingqu'}, 
{'高坪区': 'gaopingqu'}]], [['sn', {'大英县': 'dayingxian'}, {'安居区': 'anjuqu'}, {'射洪县': 'shehongxian'}, 
{'船山区': 'chuanshanqu'}, {'蓬溪县': 'pengxixian'}]], [['yibin', {'兴文县': 'xingwenxian'}, {'南溪区': 'nanxiqu'}, 
{'叙州区': 'xuzhouqu'}, {'屏山县': 'pingshanxian1'}, {'江安县': 'jianganxian'}, {'珙县': 'gongxian'}, {'筠连县': 'junlianxian'}, 
{'翠屏区': 'cuipingqu'}, {'长宁县': 'changningxian2'}, {'高县': 'gaoxian'}]], [['baoji', {'凤县': 'fengxian3'}, 
{'凤翔县': 'fengxiangxian'}, {'千阳县': 'qianyangxian'}, {'太白县': 'taibaixian'}, {'岐山县': 'qishanxian'}, 
{'扶风县': 'fufengxian'}, {'渭滨区': 'weibinqu'}, {'眉县': 'meixian'}, {'金台区': 'jintaiqu'}, {'陇县': 'longxian'}, 
{'陈仓区': 'chencangqu'}, {'麟游县': 'linyouxian'}]], [['hanzhong', {'汉台区': 'hantaiqu'}, {'南郑区': 'nanzhengqu'}]], 
[['xianyang', {'泾阳县': 'jingyangxian'}, {'长武县': 'changwuxian'}, {'礼泉县': 'liquanxian'}, {'三原县': 'sanyuanxian'}, 
{'乾县': 'qianxian'}, {'旬邑县': 'xunyixian'}, {'渭城区': 'weichengqu2'}, {'秦都区': 'qinduqu'}, {'彬县': 'binxian1'}, 
{'永寿县': 'yongshouxian'}, {'淳化县': 'chunhuaxian'}, {'武功县': 'wugongxian'}, {'杨陵区': 'yanglingqu'}, 
{'兴平市': 'xingpingshi'}, {'西咸新区（咸阳）': 'xixianxinquxianyang'}]], [['jz', {'介休市': 'jiexiushi'}, {'和顺县': 'heshunxian'}, 
{'太谷县': 'taiguxian'}, {'寿阳县': 'shouyangxian'}, {'左权县': 'zuoquanxian'}, {'平遥县': 'pingyaoxian'}, {'昔阳县': 'xiyangxian'}, 
{'榆次区': 'yuciqu1'}, {'榆社县': 'yushexian'}, {'灵石县': 'lingshixian'}, {'祁县': 'qixian2'}]], [['ty', 
{'杏花岭区': 'xinghualingqu'}, {'迎泽区': 'yingzequ'}, {'万柏林区': 'wanbolinqu'}, {'小店区': 'xiaodianqu'}, 
{'尖草坪区': 'jiancaopingqu'}, {'晋源区': 'jinyuanqu'}, {'阳曲县': 'yangquxian'}, {'娄烦县': 'loufanxian'}, {'古交市': 'gujiaoshi'}, 
{'清徐县': 'qingxuxian'}]], [['wlmq', {'乌鲁木齐县': 'wulumuqixian'}, {'天山区': 'tianshanqu'}, {'头屯河区': 'toutunhequ'}, 
{'新市区': 'xinshiqu'}, {'水磨沟区': 'shuimogouqu'}, {'沙依巴克区': 'shayibakequ'}, {'米东区': 'midongqu'}, 
{'达坂城区': 'dabanchengqu'}]], [['dali', {'凤仪': 'fengyi'}, {'古城': 'gucheng3'}, {'海东': 'haidong'}, 
{'经开区': 'jingkaiqu10'}, {'满江片区': 'manjiangpianqu'}, {'市区': 'shiqu'}, {'下关北区': 'xiaguanbeiqu'}]], [['km', 
{'五华': 'wuhua'}, {'盘龙': 'panlong'}, {'官渡': 'guandu'}, {'西山': 'xishan23'}, {'呈贡': 'chenggong'}, {'晋宁': 'jinning'}, 
{'嵩明': 'songming'}, {'东川': 'dongchuan'}, {'富民': 'fumin'}, {'宜良': 'yiliang'}, {'石林': 'shilin'}, {'寻甸': 'xundian'}, 
{'禄劝': 'luquan1'}, {'安宁': 'anning'}]], [['huzhou', {'南浔区': 'nanxunqu'}, {'长兴县': 'changxingxian'}, 
{'德清县': 'deqingxian2'}, {'吴兴区': 'wuxingqu'}, {'安吉县': 'anjixian'}]], [['jx', {'南湖区': 'nanhuqu'}, 
{'桐乡市': 'tongxiangshi'}, {'嘉善县': 'jiashanxian'}, {'秀洲区': 'xiuzhouqu'}, {'海宁市': 'hainingshi1'}, {'海盐县': 'haiyanxian'}, 
{'平湖市': 'pinghushi'}]], [['jh', {'东阳市': 'dongyangshi'}, {'义乌市': 'yiwushi'}, {'兰溪市': 'lanxishi'}, 
{'婺城区': 'wuchengqu'}, {'武义县': 'wuyixian'}, {'永康市': 'yongkangshi'}, {'浦江县': 'pujiangxian'}, {'磐安县': 'pananxian'}, 
{'金东区': 'jindongqu'}]], [['nb', {'海曙区': 'haishuqu1'}, {'江北区': 'jiangbeiqu1'}, {'镇海区': 'zhenhaiqu1'}, 
{'北仑区': 'beilunqu1'}, {'鄞州区': 'yinzhouqu2'}, {'余姚市': 'yuyaoshi'}, {'慈溪市': 'cixishi'}, {'奉化区': 'fenghuaqu'}, 
{'象山县': 'xiangshanxian'}, {'宁海县': 'ninghaixian'}]], [['quzhou', {'常山县': 'changshanxian'}, {'开化县': 'kaihuaxian'}, 
{'柯城区': 'kechengqu'}, {'江山市': 'jiangshanshi'}, {'衢江区': 'qujiangqu'}, {'龙游县': 'longyouxian'}]], [['sx', 
{'上虞区': 'shangyuqu'}, {'嵊州市': 'shengzhoushi'}, {'新昌县': 'xinchangxian'}, {'柯桥区': 'keqiaoqu'}, {'诸暨市': 'zhujishi'}, 
{'越城区': 'yuechengqu'}]], [['taizhou', {'三门县': 'sanmenxian'}, {'临海市': 'linhaishi'}, {'仙居县': 'xianjuxian'}, 
{'天台县': 'tiantaixian'}, {'椒江区': 'jiaojiangqu'}, {'温岭市': 'wenlingshi'}, {'玉环市': 'yuhuanshi'}, {'路桥区': 'luqiaoqu'}, 
{'黄岩区': 'huangyanqu'}]], [['wz', {'鹿城区': 'luchengqu'}, {'瓯海区': 'ouhaiqu'}, {'龙湾区': 'longwanqu'}, 
{'乐清市': 'yueqingshi'}, {'瑞安市': 'ruianshi'}, {'苍南县': 'cangnanxian'}, {'平阳县': 'pingyangxian'}, {'洞头区': 'dongtouqu'}, 
{'泰顺县': 'taishunxian'}, {'永嘉县': 'yongjiaxian'}, {'龙港市': 'longgangshi'}]], [['yw', {'北苑': 'beiyuan'}, 
{'城西': 'chengxi3'}, {'稠城': 'choucheng'}, {'稠江': 'choujiang'}, {'佛堂': 'fotang'}, {'福田': 'futian'}, {'后宅': 'houzhai'}, 
{'江东': 'jiangdong4'}, {'廿三里': 'niansanli'}, {'苏溪': 'suxi'}, {'义亭': 'yiting'}, {'义乌市': 'yiwushi1'}]]] '''