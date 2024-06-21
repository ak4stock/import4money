
import requests
import time
import json

def get_zt_data(date):
    url = 'https://push2ex.eastmoney.com/getTopicZTPool?cb=callbackdata194825&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=1000&sort=fbt%3Aasc&date={0}&_='
    timestamp = int(time.time() * 1000)
    myurl = url.format(date) + str(timestamp)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
        'Origin': 'http://www.eastmoney.com/',
        'Referer': 'http://www.eastmoney.com/',
        'Cookie': 'eastmoney_'
    }
    res = requests.get(myurl, headers=headers)
    try:
        if res.status_code == 200:
            data_text = res.text.replace('callbackdata194825', '')[1:-1].replace('(','').replace(')','').replace(';','')
            res_json = json.loads(data_text).get('data').get('pool')
            return res_json
        else:
            print('请求异常', res)
    except:
        raise ('中断')

def handle(date):
    zt = get_zt_data(date)
    hyd = {}
    fbzjList = []
    fbzjList2 = []
    ltszList = []
    lbtsList = []
    for d in zt:
        fbzj = round(d.get('fund')/10000,2)  # 封板资金 万
        fbzj2 = round(d.get('fund')/100000000,4)  # 封板资金 亿
        fbzjList.append(fbzj)
        fbzjList2.append(fbzj2)
        ltsz = round(d.get('ltsz')/100000000,2) # 流通市值 亿
        ltszList.append(ltsz)
        lbts = d.get('lbc') # 连板天数
        lbtsList.append(lbts)
        hybk = str(d.get('hybk')) # 行业板块
        if hyd.get(hybk) is not None:
            hyd[hybk] = hyd[hybk] + 1
        else:
            hyd[hybk] = 1
    hyd = sorted(hyd.items(), key=lambda item: item[1], reverse=True)
    print(date + ' 日涨停数量:= ' + str(len(zt)))
    print(date + ' 日最高板:= ' + str(max(lbtsList)))
    print('封板最大流通市值（亿）:= ' + str(max(ltszList)))
    print('封板最小流通市值（亿）:= ' + str(min(ltszList)))
    print('封板资金最大值（万）:= ' + str(max(fbzjList)))
    print('封板资金最小值（万）:= ' + str(min(fbzjList)))
    print('总封板资金(亿):= ' + str(sum(fbzjList2)))
    print('行业涨停数量分布情况（前5）:= ')
    print(str(json.dumps(hyd[0:5], ensure_ascii=False, indent=4)))
    return len(zt), sum(fbzjList2)


if __name__ == '__main__':
    dd1 = '20240619'
    dd2 = '20240620'
    print('不含ST，涨停股票统计情况： \n')
    s1, d1 = handle(dd1)
    s2, d2 = handle(dd2)
    print(dd1 + ' ~ ' + dd2 + ' 两日涨停数量增减情况(个)：= ' + str(s2 - s1))
    print(dd1 + ' ~ ' + dd2 + ' 两日封板资金增减情况(亿)：= ' + str(round(d2-d1, 4)))
