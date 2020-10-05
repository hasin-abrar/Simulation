from Read_Data import getData
import numpy as np
import matplotlib.pyplot as plt
import math

def Fitted_Distr(y,a=1.5278996202501096,b=1.2999425079066453):
    #return (1-np.exp((-(x / b)**a)))
    result = b * (-(math.log(1 - y))) ** (1 / a)
    return result

def getFitted_Xq(data,qi):
    return np.percentile(data,qi)

def Distr_Diff(data,fitted_data,x=0.1):
    incr=0
    n=len(data)
    X=[]
    Y=[]
    for i,d in enumerate(data,1):
        X.append((Fitted_Distr((i-0.5)/n)))
        Y.append((d))
    return X,Y

def Plot_Diff(X,Y):
    plt.plot(X,Y)
    plt.xlabel('Fitted x')
    plt.ylabel('Sample x')

    plt.title('Q-Q Plot', fontweight='bold')
    plt.plot(Y,Y,color='r',ls='--')
    plt.savefig('Q-Q Plot.png')
    #plt.show()

if __name__=='__main__':
    data=getData()
    data.sort()
    fitted_data=np.random.weibull(1.370643447,100)
    fitted_data.sort()
    X,Y=Distr_Diff(data,fitted_data,x=0.01)
    Plot_Diff(X,Y)