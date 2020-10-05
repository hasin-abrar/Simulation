from Read_Data import getData
from statistics import mean,median
import matplotlib.pyplot as plt



def Quantile(data):
    data.sort()
    n=len(data)
    i=(n+1)//2
    median_data = median(data)
    print('Median: ',median_data)
    j=(i+1)//2
    quartile0=data[j-1]
    print('\nQuantile[0]: ',quartile0)
    quartile1=data[(n-j+1)-1]
    print('Quantile[1]: ', quartile1)
    quartile=(quartile0+quartile1)/2
    print('Quantile Midpoint: ', quartile)
    k=(j+1)//2
    octile0=data[k-1]
    print('\nOctile[0]: ', octile0)
    octile1=data[(n-k+1)-1]
    print('Octile[1]: ', octile1)
    octile=(octile0+octile1)/2
    print('Octile Midpoint: ', octile)
    extreme=(data[0]+data[n-1])/2
    print('\nExtreme[0]: ', data[0])
    print('Extreme[1]: ', data[n-1])
    print('Extreme Midpoint: ', extreme)

    return median_data,quartile,octile,extreme


def Box_Plot(data,median,quartile,octile,extreme):
    plt.boxplot(data, showmeans=True, whis=max(data)+10, vert=False)

    plt.axvline(median, color='cyan', label='Median_Midpoint')
    plt.axvline(quartile, color='blue', label='Quartile_Midpoint')
    plt.axvline(octile, color='green', label='Octile_Midpoint')
    plt.axvline(extreme, color='red', label='Extreme_Midpoint')

    plt.legend()
    plt.title('Box Plot', fontweight='bold')
    #plt.show()
    plt.savefig('Box Plot.png')


if __name__=='__main__':
    data=getData()
    median,quartile,octile,extreme=Quantile(data)
    Box_Plot(data,median,octile,quartile,extreme)
