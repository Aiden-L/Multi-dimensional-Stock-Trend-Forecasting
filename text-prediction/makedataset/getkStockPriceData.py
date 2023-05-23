import json
import os
import time
import urllib.request as ur
import re

SAVE_PATH = "savedpricedata/"

# 获取K线数据
def getklinedata(stock_code):
    try:
        # get data
        data = ur.urlopen(
            'http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112406346334614643425_1599729791684&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=1.'
            + stock_code + '&beg=0&end=20500000&_=1599729791863').read().decode("utf-8", "ignore")
        # delete characters at the beginning and the end
        data = re.sub('^.*?\(', "", data)
        data = re.sub('\).*?$', "", data)
        # take data
        json_data = json.loads(data)
        if json_data['data']:
            data_list = json_data['data']['klines']
            re_list = []
            # 取获得数据后300发送
            for item in data_list[-100:]:
                re_list.append(item.split(','))
            return re_list, json_data['data']['name']
        else:
            # get data
            data = ur.urlopen(
                'http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112406346334614643425_1599729791684&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&ut=7eea3edcaed734bea9cbfc24409ed989&klt=101&fqt=1&secid=0.'
                + stock_code + '&beg=0&end=20500000&_=1599729791863').read().decode("utf-8", "ignore")
            # delete characters at the beginning and the end
            data = re.sub('^.*?\(', "", data)
            data = re.sub('\).*?$', "", data)
            # take data
            json_data = json.loads(data)
            data_list = json_data['data']['klines']
            re_list = []
            # 取获得数据发送
            for item in data_list:
                re_list.append(item.split(','))
            return re_list, json_data['data']['name']
    except Exception as e:
        print(e)
        return False


def formattedkdata(stock_code):
    Kdata, stock_name = getklinedata(stock_code)
    categories = []
    series = [{
        "name": "",
        "data": []
    }]
    series[0]["name"] = stock_name
    for d in Kdata:
        categories.append(d[0].replace("-", "/"))
        series[0]["data"].append([float(d[1]), float(d[2]), float(d[4]), float(d[3])])
    candle = {
        "categories": categories,
        "series": series
    }
    return candle


# 带存储和获取旧数据
def getstockkdata(stock_code, get_old):
    now_date = time.strftime("%Y%m%d", time.localtime())
    if get_old:
        # 开启加载旧数据模式
        if os.path.exists(SAVE_PATH + now_date + stock_code + ".json"):
            # 之前存过，直接加载之前的数据
            with open(SAVE_PATH + now_date + stock_code + ".json", 'r') as f:
                return json.loads(f.read())
        else:
            # 之前没存过，重新存
            text_data_obj = formattedkdata(stock_code)
            with open(SAVE_PATH + now_date + stock_code + ".json", 'w') as f:
                f.write(json.dumps(text_data_obj))
            return text_data_obj
    else:
        # 不开加载旧数据模式，和重新获取数据一样
        text_data_obj = formattedkdata(stock_code)
        with open(SAVE_PATH + now_date + stock_code + ".json", 'w') as f:
            f.write(json.dumps(text_data_obj))
        return text_data_obj
# -------------------------------------》以上来自项目stockbackend/crawlers/getkstockdata.py


# 创建时间和收盘价对应的字典
def formatpricedatadict(stock_code):
    # print(getklinedata(stock_code))
    Kdata, stock_name = getklinedata(stock_code)
    seq = []
    for d in Kdata:
        seq.append(d[0])
    pricedict = dict.fromkeys(seq)
    for d in Kdata:
        pricedict[d[0]] = float(d[2])
    ret = {
        "seq": seq,
        "pricedict": pricedict
    }
    # 写入文件
    with open(SAVE_PATH + stock_code + "price.json", 'w') as f:
        f.write(json.dumps(ret))
    return ret


# 存贮存储沪深300股票价格时间对应json
def get300pricefile():
    with open("300code.json", 'r') as f:
        codes = json.loads(f.read())
    count = 0
    for code in codes:
        count += 1
        print("正在获取数据"+code+"["+str(count)+"/300]")
        formatpricedatadict(code)


if __name__ == '__main__':
    # 单个股票测试
    # print(formatpricedatadict("600030"))
    # 存300股价格数据到savedpricedata
    get300pricefile()
