from Read_Data import getData
import numpy as np
import matplotlib.pyplot as plt

def Fitted_Distr(x,a=1.5278996202501096,b=1.2999425079066453):
    return (1-np.exp((-(x / b)**a)))

def Sample_Distr(data,x):
    n=len(data)
    cnt=0
    for d in data:
        if d<=x:
            cnt+=1
    return cnt/n

def Distr_Diff(data,x=0.1):
    incr=0
    max_range=max(data)
    X=[]
    Y=[]
    for i,d in enumerate(data):
        X.append(Sample_Distr(data,d))
        Y.append(Fitted_Distr(d))
    return X,Y

def Plot_Diff(X,Y):
    plt.plot(X,Y)
    plt.plot([0,1],[0,1],color='r',ls='--')
    plt.xlabel('Sample F(x)')
    plt.ylabel('Fitted F(x)')
    plt.title('P-P Plot', fontweight='bold')
    plt.savefig('P-P Plot.png')
    #plt.show()

if __name__=='__main__':
    data=getData()
    data.sort()
    X,Y=Distr_Diff(data,x=0.01)
    Plot_Diff(X,Y)