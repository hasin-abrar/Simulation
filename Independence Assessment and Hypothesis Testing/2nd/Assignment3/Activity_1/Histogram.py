from Read_Data import getData
import math
import matplotlib.pyplot as plt

def Data_Interval(data,b=0.1):
    n=len(data)
    max_range=math.ceil(max(data))
    X=[]
    Y=[]
    low=0
    high=b
    while(high<=max_range):
        X.append(high)
        Y.append((len([d for d in data if low<=d<high]))/n)
        low=high
        high+=b

    return X,Y

def Plot_Histogram(X,Y,b):
    for i,x in enumerate(X):
        plt.bar(x, Y[i], width=b)

    plt.xlabel('x (b = '+str(b)+')')
    plt.ylabel('h(x)')
    plt.title('Histogram', fontweight='bold')
    plt.savefig('Histogram Plot for b='+str(b)+'.png')


def Diff_Interval_Plot(data,b=0.1):
    X,Y=Data_Interval(data,b)
    Plot_Histogram(X,Y,b)


if __name__=='__main__':
    data=getData()
    Diff_Interval_Plot(data,b=0.2)

