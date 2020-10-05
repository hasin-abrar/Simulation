data=getData()


from xlwt import Workbook


wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')

row=4
col=1
for x in data:
    sheet1.write(row, col, x)
    row+=1


wb.save('Alpha Beta.xls')
