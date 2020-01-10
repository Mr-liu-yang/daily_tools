import xlrd
import json
import codecs

#把excel表格中指定sheet转为json
def Excel2Json(file_path):
    #打开excel文件
    if get_data(file_path) is not None:
        book = get_data(file_path)
        #抓取所有sheet页的名称
        worksheets = book.sheet_names()
        print("该Excel包含的表单列表为：\n")
        for sheet in worksheets:
            print ('%s,%s' %(worksheets.index(sheet),sheet)) # sheet为表单名
        inp = 0  # 请输入表单名对应的编号，对应表单将自动转为json
        sheet = book.sheet_by_index(int(inp))
        # import pdb;pdb.set_trace()
        row_0 = sheet.row(0)     #第一行是表单标题
        nrows=sheet.nrows       #行号
        ncols=sheet.ncols       #列号

        result={}   #定义json对象
        result["title"]=file_path   #表单标题
        result["rows"]=nrows        #行号
        result["children"]=[]      #每一行作为数组的一项
        #遍历所有行，将excel转化为json对象
        for i in range(nrows):
            if i==0:
                continue
            tmp={}
            #遍历当前行所有列
            for j in range(ncols):
                #获取当前列中文标题
                title_de=str(row_0[j])
                title_cn= title_de.split("'")[1]
                #获取单元格的值
                tmp[title_cn]=sheet.row_values(i)[j]
            with open('/Users/smart_liu/Desktop/111_download/{}.json'.format(out_name), 'a') as f:
                f.write(json.dumps(tmp, ensure_ascii=False) + '\n')
            result["children"].append(tmp)
        # json_data=json.dumps(result,indent= 4,ensure_ascii=False, sort_keys=True)
        # saveFile(os.getcwd(),worksheets[int(inp)],json_data)
        # print(json_data)

# 获取excel数据源
def get_data(file_path):
    """获取excel数据源"""
    try:
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print('excel表格读取失败：%s' %e)
        return None

def saveFile(file_path,file_name,data):
    
    output = codecs.open(file_path+"/"+ out_name +".json",'w',"utf-8")
    output.write(data)
    output.close()

if __name__ == '__main__':
    import sys
    file_path = sys.argv[1] # 要转换的Excel路径
    out_name = sys.argv[2] # 输出json文件名前缀
    json_data=Excel2Json(file_path)
