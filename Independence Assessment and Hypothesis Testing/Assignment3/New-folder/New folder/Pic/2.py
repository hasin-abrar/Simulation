def Scatter(data):
    X=[]
    Y = []
    for i in range(len(data)-1):
        X.append(data[i])
        Y.append(data[i+1])
    return X,Y

def Scatter_Plot(X,Y):
    plt.scatter(X,Y)
    plt.xlabel('X[i]')
    plt.ylabel('X[i+1]')
    plt.title('Scatter Plot', fontweight='bold')
    #plt.show()
    plt.savefig('Scatter_Plot.png')
