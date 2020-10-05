from statistics import mean
def S2(data):
    n=len(data)
    mean_value=mean(data)
    s2=0
    for x in data:
        s2+=(x-mean_value)**2
    s2/=(n-1)
    return s2

def Cj(data,j):
    n=len(data)
    mean_value=mean(data)

    cj=0
    for i in range(n-j):
        cj+=(data[i]-mean_value)*(data[i+j]-mean_value)
    cj/=(n-j)
    return cj

def Pj(data,j):
    return Cj(data,j)/S2(data)


def Corr(data,j=None):
    if(j==None):
        j=len(data)-1

    X = [i for i in range(1, j+1)]
    Y = []
    for x in X:
        Y.append(Pj(data, x))
    return X,Y

def Corr_Plot(X,Y):
    plt.axhline(0, color='red')
    plt.scatter(X,Y)
    plt.xlabel('j')
    plt.ylabel('Estimated(Pj)')
    plt.title('Correlation Plot',fontweight='bold')
    plt.savefig('Correlation_Plot j= '+str(len(X))+'.png')
