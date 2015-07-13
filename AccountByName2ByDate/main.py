#-*- coding=utf-8 -*-
__author__ = 'dongxu'

from config import *
import xlrd
import json
import xlwt

# 将日期字段转换为日期列表
# 日期字段的格式为：
# 2015-03-01,02,03,04\n
# 2015-04-02,05,06,22,30\n
# 2015-05-03,05,11,22
def format_date_col(date_str):
    result = []
    dates_line = dates.strip().split("\n")
    for date_line in dates_line:
        year_month_days = date_line.split("-")
        year = year_month_days[0].strip()
        month = year_month_days[1].strip()
        days = year_month_days[2].split(",")
        for day in days:
            date = "%s-%s-%s" % (year, month, day.strip())
            result.append(date)
    return result


# 将字符串数组通过","字符连接起来成为一个字符串
def cat_str_list(str_list):
    result_str = ""
    idx = 1
    for _str in str_list:
        result_str += _str
        if len(str_list) == idx:
            break
        result_str += ","
        idx = idx + 1
    return result_str


if __name__ == "__main__":
    excel_file = u"D:/account.xls"
    workbook = xlrd.open_workbook(excel_file)
    table_by_name = workbook.sheet_by_name(u"按人名报账")

    # 报账类型为加班餐的 ，按日期维度的报账
    dinner_date_map_name = {}

    for row_idx in range(dinner_row_start, dinner_row_end):
        row = table_by_name.row_values(row_idx)
        if row:
            name = row[name_col]
            dates = row[date_col]
            if name and dates:
                date_list = format_date_col(dates)
                for date in date_list:
                    date_mapped_name = dinner_date_map_name.get(date)
                    if not date_mapped_name:
                        date_mapped_name = []
                        dinner_date_map_name[date] = date_mapped_name
                    date_mapped_name.append(name)
            else:
                pass
            # print "name:%s, date:%s" % (row[name_col], row[date_col])

    sorted_map_list = sorted(dinner_date_map_name.iteritems(), key=lambda d:d[0],reverse=False)

    for i in sorted_map_list:
        date_str = i[0]
        name_list = i[1]
        print "date:%s, name_list:%s" % (date_str, cat_str_list(name_list))
        # print "date:%s, name_list:%s" % (date_str, json.dumps(name_list, encoding="UTF-8", ensure_ascii=False))

    need_write = False
    need_write = True
    if need_write:
        temp_excel_file = excel_file + u".bydate"
        write_excel = xlwt.Workbook()
        sheet = write_excel.add_sheet(u"按日期报账")
        idx = 0
        for i in sorted_map_list:
            date_str = i[0]
            name_list = i[1]
            sheet.write(idx, 0, date_str)
            sheet.write(idx, 1, cat_str_list(name_list))
            sheet.write(idx, 2, len(name_list))
            sheet.write(idx, 3, len(name_list) * 15)
            idx += 1
        write_excel.save(temp_excel_file)

