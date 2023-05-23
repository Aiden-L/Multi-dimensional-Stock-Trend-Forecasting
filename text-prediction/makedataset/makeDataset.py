import json
import os
import pandas as pd

POS_PATH = "dataset/pos.csv"
NEG_PATH = "dataset/neg.csv"
COM_PATH = "dataset/combined.csv"


def makedataset(stock_code):
    data = pd.read_csv('data/' + stock_code + 'news.csv', sep=',', names=['contents', 'author', 'time']).astype(str)

    # 通过lambda表达式，处理时间列，提取时间信息
    la = lambda x: x.split(" ")[0]
    data['time'] = data['time'].apply(la)

    # 继续处理，添加年份
    import datetime
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    count = 0
    for ltime in data['time']:
        # print(ltime.split("-")[0])
        try:
            datamonth = int(ltime.split("-")[0])
            # 数据中的月份，如果跨年，则year-1
            if month == 1 and datamonth == 12:
                year -= 1
            month = datamonth
            data['time'][count] = str(year) + "-" + ltime
        except Exception as e:
            # 记录错误数据
            data['time'][count] = "ERROR"
        count += 1

    # 新增一列，用于存结果
    data['value'] = data['time']
    count2 = 0
    # 读取到天价格数据
    with open("../makedataset/savedpricedata/" + stock_code + "price.json") as f:
        priceobj = json.loads(f.read())
    seq = priceobj["seq"]
    pricedict = priceobj["pricedict"]
    for thisday in data['time']:
        try:
            # 计算下一天
            # dayarray = thisday.split("-")
            # nextday = (datetime.datetime(int(dayarray[0]), int(dayarray[1]), int(dayarray[2])) + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
            # 计算涨跌
            thisdate = ""
            nextdate = ""
            for i in range(len(seq)):
                if thisday < seq[i]:
                    if i == 0:
                        break
                    thisdate = seq[i - 1]
                    nextdate = seq[i]
                    break
            if pricedict[thisdate] > pricedict[nextdate]:
                data['value'][count2] = 0
                with open(NEG_PATH, 'a', encoding="utf-8") as f:
                    f.write(data['contents'][count2] + "\n")
            else:
                data['value'][count2] = 1
                with open(POS_PATH, 'a', encoding="utf-8") as f:
                    f.write(data['contents'][count2] + "\n")
            with open(COM_PATH, 'a', encoding="utf-8") as f:
                f.write(data['contents'][count2] + "," + str(data['value'][count2]) + "\n")
        except Exception as e:
            # 记录错误数据
            # print("ERROR: ", e)
            data['value'][count2] = "ERROR"
        count2 += 1
    # print(data)


def makeall():
    # 存在先删除，避免后续追加写入重复
    if os.path.exists(NEG_PATH):
        os.remove(NEG_PATH)
    if os.path.exists(POS_PATH):
        os.remove(POS_PATH)
    if os.path.exists(COM_PATH):
        os.remove(COM_PATH)
    # 读取300code,逐一写入
    with open("300code.json", 'r') as f:
        codes = json.loads(f.read())
    count = 0
    for code in codes:
        count += 1
        print("正在制作数据"+code+"["+str(count)+"/300]")
        makedataset(code)


if __name__ == '__main__':
    # makedataset("600030")
    makeall()