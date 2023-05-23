import json
import urllib.request as ur
import re


# 获取沪深300股票代码
def get_300_data():
    try:
        # get data
        data = ur.urlopen(
            'http://95.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112404771239869461046_1614993327596&pn=1&pz=300&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:BK0500+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1614993327597')\
            .read().decode("utf-8", "ignore")
        # delete characters at the beginning and the end
        data = re.sub('^.*?\(', "", data)
        data = re.sub('\).*?$', "", data)
        # take data
        json_data = json.loads(data)
        # 存储数据的空列表
        re_list = []
        for item in json_data['data']['diff']:
            re_list.append(item['f12'])
        return re_list
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    dat = get_300_data()
    with open("300code.json",'w') as f:
        f.write(json.dumps(dat))
    print(dat)
