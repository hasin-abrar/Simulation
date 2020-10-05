from Read_Data import getData
import numpy as np
import matplotlib.pyplot as plt

def Fitted_Distr(x,a=1.5278996202501096,b=1.2999425079066453):
    return (1-np.exp((-(x / b)**a)))

def getFitted_Xq(data,qi):
    return np.percentile(data,qi)

def Distr_Diff(data,fitted_data,x=0.1):
    incr=0
    n=len(data)
    X=[]
    Y=[]
    for i,d in enumerate(data,1):
        X.append((d))
        Y.append(getFitted_Xq(fitted_data,(i-0.5)/n))
    return X,Y

def Plot_Diff(X,Y):
    plt.plot(X,Y)
    plt.xlabel('Sample x')
    plt.ylabel('Fitted x')
    plt.title('Q-Q Plot', fontweight='bold')
    plt.savefig('Q-Q Plot.png')
    #plt.show()

if __name__=='__main__':
    data=getData()
    data.sort()
    fitted_data=np.random.weibull(1.370643447,100)
    fitted_data.sort()
    X,Y=Distr_Diff(data,fitted_data,x=0.01)
    Plot_Diff(X,Y)