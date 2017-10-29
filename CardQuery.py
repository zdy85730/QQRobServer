import requests
import json

def magic(cardname=None, num=1, rarity=None, mainType=None, color=None, manaNormal=None, manaMore=None):
    s = requests.session()
    colordic = {'白色':'white', '蓝色':'blue', '黑色':'black', '红色':'red', '绿色':'green', '无色':'colorless'}
    data={
        'name':cardname,
        'statistic':'total',
        'token':'',
        'page':'0',
        'size':num,
        'rarity':rarity,
        'manaNormal':manaNormal, 
        'manaMore':manaMore,
        'mainType':mainType,
        'colorAll':1
    }
    if color:
        color = color.split(",")
        for c in color:
            ec = colordic.get(c, False)
            if ec: data[ec] = 1

    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':'http://www.iyingdi.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453',
        'X-Requested-With':'XMLHttpRequest'
    }
    res = []
    ret = s.post(url='http://www.iyingdi.com/magic/card/search/vertical', headers=headers, data=data)
    ret = json.loads(str(ret.content, encoding='utf8'))
    if ret['success']:
        colordic = {'white':'白色', 'blue':'蓝色', 'black':'黑色', 'red':'红色', 'green':'绿色', 'colorless':'无色'}
        raritydic = {'Mythic Rare,':'秘稀', 'Rare':'稀有', 'Uncommon':'非普通', 'Common':'普通', 'Special':'其他'}
        cards=ret['data']['cards']
        for card in cards:
            dic={
                "名称":("%s %s") % (card['cname'].strip(), card['ename'].strip()),
                "类别":('%s~%s') % (card['mainType'], card['subType']),
                "描述":card['description'].strip(),
                "效果":card['rule'].strip(),
                "系列":card['seriesName'].strip(),
                "攻防":("%d/%d") % (card["attack"], card["defense"]),
                "法力":card["mana"],
                "稀有度":raritydic.get(card["rarity"], ""), "颜色":[],
                "价格":("高价:%d，平均价:%d，低价:%d") % (card['maxPrice'], card['midPrice'], card['minPrice'])
            }
            for color in colordic.keys():
                if card[color]:
                    dic["颜色"].append(colordic[color])
            card['description']
            res.append(dic)
    return res

'''def hearthstone(name=None, num=1):
    s = requests.session()
    colordic = {'白色':'white', '蓝色':'blue', '黑色':'black', '红色':'red', '绿色':'green', '无色':'colorless'}
    data={
        'name':cardname,
        'statistic':'total',
        'token':'',
        'page':'0',
        'size':num,
        'rarity':rarity,
        'manaNormal':manaNormal, 
        'manaMore':manaMore,
        'mainType':mainType,
        'colorAll':1
    }
    if color:
        color = color.split(",")
        for c in color:
            ec = colordic.get(c, False)
            if ec: data[ec] = 1

    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':'http://www.iyingdi.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453',
        'X-Requested-With':'XMLHttpRequest'
    }
    res = []
    ret = s.post(url='http://www.iyingdi.com/magic/card/search/vertical', headers=headers, data=data)
    ret = json.loads(str(ret.content, encoding='utf8'))'''


