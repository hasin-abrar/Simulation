from Activity_1.Histogram import Data_Interval

def weibull(x,a,b):
    return (a * (b**(-a)) * (x**(a - 1)) * np.exp(-(x / b)**a))

def Plot_Histogram(X,Y,b):

    for i,x in enumerate(X):
        plt.bar(x,Y[i],width=b)

    genX=np.arange(0,75)/15
    plt.plot(genX, weibull(genX, a=1.5278996202501096,b=1.2999425079066453)*scaling)

    plt.xlabel('x')
    plt.ylabel('h(x)/f(x)')
    plt.title('Frequency Comparison', fontweight='bold')
    plt.savefig('Frequency Comparison.png')


def Diff_Interval_Plot(data,b=0.1):
    X,Y=Data_Interval(data,b)
    Plot_Histogram(X,Y,b)
