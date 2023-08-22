# 对往来资金的处理
import xlrd
import xlwings as xw
def decode_data(FileName: str,take: bool,keyword :str,onlyHead: bool):
    # Filename -> 文件名 
    # take -> 是否显示已领，true代表显示，false代表不显示
    # keyword -> 搜索的关键词
    # onlyHead -> 只显示抬头是我们的
    data = xlrd.open_workbook(FileName,encoding_override="utf-8",formatting_info=True)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    allcount = 0
    allmoney = 0
    result = []
    for i in range(4,nrows):
        alldata = table.row_values(i)
        hidden = table.rowinfo_map[i].hidden
        name = alldata[4]
        money = alldata[5]
        if onlyHead:
            temp = name[0:len(keyword)]
        else:
            temp = name
        if keyword in temp:
            if hidden and take == False:
                continue
            allcount += 1
            allmoney += money
            result.append({'name':name,'money':money})
    return result,allcount,allmoney



# 下面根据res造表

def getXls(FileName: str,take: bool,keyword :str,onlyHead: bool,LastName:str,Date1: str,Date2: str):
    res,count,money = decode_data(FileName,take,keyword,onlyHead)  #这个是默认查询方式
    if(count <= 0):
        return "无数据"
    
    temp = "区国库集中支付中心：\n " + \
        "    根据" + str(Date1) + "未录指标更新，我单位未录指标共有" + str(count) +"笔，共计"+ str(money) +"元。"

    app = xw.App(visible=False,add_book=False)
    app.display_alerts = False
    app.screen_updating = False


    workbook = app.books.open("model.xls")

    workbook.sheets['sheet1'].range('A3').value = temp

    sht1 = workbook.sheets['sheet1']

    # 数据都在res

    sht1.range('A5:E5').api.Copy()



    i = 5
    for detail in res:
        name = detail['name']
        money1 = detail['money']
        ge1 = 'B' + str(i)
        ge2 = 'C' + str(i)
        sht1.range('A' + str(i)).row_height = 43
        sht1.range('A' + str(i)).api.Select()
        sht1.api.Paste()
        sht1.range(ge1).value = name
        sht1.range(ge2).value = money1
        sht1.range('A' + str(i)).value = i - 4
        i += 1
    sht1.range('A' + str(i)).row_height = 43
    sht1.range('A' + str(i)).api.Select()
    sht1.api.Paste()

    sht1.range('A' + str(i) + ':' + 'B' + str(i)).merge()
    sht1.range('A' + str(i)).value = "合 计"

    sht1.range('A' + str(i)).horizontal_alignment = 'center'
    sht1.range('A' + str(i)).vertical_alignment  = 'center'
    sht1.range('A' + str(i)).value = "合 计"
    sht1.range('C' + str(i)).value = money

    sht1.range('C' + str(i + 4) + ':' + 'D' + str(i + 5)).merge()
    sht1.range('C' + str(i + 4)).api.HorizontalAlignment = -4108
    sht1.range('C' + str(i + 4)).row_height = 30
    sht1.range('C' + str(i + 4)).value = LastName


    sht1.range('C' + str(i + 6) + ':' + 'D' + str(i + 6)).merge()
    sht1.range('C' + str(i + 6)).api.HorizontalAlignment = -4108
    sht1.range('C' + str(i + 6)).row_height = 30
    sht1.range('C' + str(i + 6)).value = Date2

    workbook.save("./files/" + LastName+'.xls')

    workbook.close()

    app.quit()
    return LastName+'.xls'
    
