from Read_Data import getData
import matplotlib.pyplot as plt

data=getData()


from xlwt import Workbook


wb = Workbook()

sheet1 = wb.add_sheet('Sheet 1')

row=4
col=1
for x in data:
    sheet1.write(row, col, x)
    row+=1


wb.save('Alpha Beta_2.xls')



'''import seaborn as sb
sb.distplot(data)
plt.xlabel('x')
plt.ylabel('h(x)/f(x)')
#plt.legend()
plt.title('Maximum Likelihood (for Weibull)', fontweight='bold')
#plt.savefig('MLE.png')
plt.show()'''