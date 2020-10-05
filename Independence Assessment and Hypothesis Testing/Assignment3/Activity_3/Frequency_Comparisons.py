from Read_Data import getData
import matplotlib.pyplot as plt
import numpy as np
from Activity_1.Histogram import Data_Interval

scaling=0.44

def weibull(x,a,b):
    return (a * (b**(-a)) * (x**(a - 1)) * np.exp(-(x / b)**a))



def Plot_Histogram(X,Y,b):

    for i,x in enumerate(X):
        plt.bar(x,Y[i],width=b)

    genX=np.arange(0,75)/15
    plt.plot(genX, weibull(genX, a=1.5278996202501096,b=1.2999425079066453)*scaling)

    #wb=np.random.weibull(1.370643447,50)
    #weights=np.ones_like(wb)/len(wb)
    #plt.hist(wb, bins=8, weights=weights, ls='dotted', alpha=0.5, lw=3, color='g',label='Fitted Distribution')

    plt.xlabel('x')
    plt.ylabel('h(x)/f(x)')
    #plt.legend()
    plt.title('Frequency Comparison', fontweight='bold')
    plt.savefig('Frequency Comparison.png')
    #plt.savefig('Frequency with Histograms.png')
    #plt.show()

    '''for i,x in enumerate(X):
        plt.bar(x,Y[i],width=b)
    genX=np.arange(0,5)
    plt.plot(genX, weibull(genX, 1.370643447,1.268287315)*scaling)
    plt.xlabel('x')
    plt.ylabel('h(x)/f(x)')
    plt.title('Frequency Comparison', fontweight='bold')
    plt.savefig('Frequency Comparison for Insufficient Data.png')'''

def Diff_Interval_Plot(data,b=0.1):
    X,Y=Data_Interval(data,b)
    Plot_Histogram(X,Y,b)


if __name__=='__main__':
    Diff_Interval_Plot(getData(), b=.3)