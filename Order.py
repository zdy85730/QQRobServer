import CardQuery

orderDict = {}

def decorate(ordername):
    def decorator(func):
        orderDict[ordername] = func
        def wrapper(*args, **kw):
            return func(*args, **kw)
        return wrapper
    return decorator

def runOrder(order):
    order = order.split('#')
    name = order[0]
    name =  orderDict.get(name, None)
    args = []; kw = {}
    try:
        for arg in order[1:]:
            arg = arg.split("=")
            if len(arg) == 1:
                args.append(arg[0])
            else: kw[arg[0]] = arg[1]
        return name(tuple(args), kw)
    except Exception as err:  
        print(err)
        return "命令格式有误或未找到命令"


@decorate("万智牌")
def queryMagic(args, kw):
    try:
        if len(args) == 0 and len(kw) == 0:return '''可以传递的参数有cardname,num(默认为1),rarity,mainType,color,manaNormal,manaMore
        调用演示:#万智牌查询#color=白色,红色'''
        rets = CardQuery.magic(*args, **kw)
        if len(rets) == 0: return "没有找到卡牌"
        res = ''
        for ret in rets:
            res += ("名称:%s\n类别:%s\n效果:%s\n描述:%s\n攻防:%s 法力:%s 颜色:%s\n系列:%s 稀有度:%s\n价格:%s\n") % (ret['名称'], ret['类别'], ret['效果'], ret['描述'], ret['攻防'], ret['法力'], str(ret['颜色']), ret['系列'], ret['稀有度'], ret['价格'])
        return res
    except Exception as err:
        print(err)
        return '''可以传递的参数有cardname,num(默认为1),rarity,mainType,color,manaNormal,manaMore
        调用演示:#万智牌查询#color=白色,红色'''

#作业查询接口使用了另外的url，所以这个连接收到的作业查询请求返回空
@decorate("作业")
def homeworkEmpty(args, kw):
    return ""