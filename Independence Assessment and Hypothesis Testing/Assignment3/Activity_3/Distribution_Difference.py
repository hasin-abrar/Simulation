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
    diff=[]
    while(incr<=max_range):
        X.append(incr)
        diff.append(Fitted_Distr(incr)-Sample_Distr(data,incr))
        incr+=x
    return X,diff

def Plot_Diff(X,Y):
    plt.plot(X,Y)
    plt.axhline(0, color='green')
    plt.axhline(0.05, color='blue')
    plt.axhline(0.1, color='red')
    plt.axhline(-0.05, color='blue')
    plt.axhline(-0.1, color='red')
    plt.xlabel('x')
    plt.ylabel('Fitted F(x) - Sample F(x)')
    plt.title('Distribution Difference', fontweight='bold')
    plt.savefig('Distribution Diffrernce.png')
    #plt.show()

if __name__=='__main__':
    data=getData()
    X,Y=Distr_Diff(data,x=0.01)
    Plot_Diff(X,Y)