from statistics import median,mean,variance
from Read_Data import getData
import math
from scipy.stats import skew


def CV(data):
    var=variance(data)
    mean_data=mean(data)
    return (math.sqrt(var)/mean_data)

def Lexis_Ratio(data):
    var=variance(data)
    mean_data = mean(data)
    return (var/mean_data)



if __name__=='__main__':
    data = getData()

    min_value=min(data)
    max_value = max(data)
    print('Minimum: ',min_value)
    print('Maximum: ', max_value)

    mean_data=mean(data)
    print('Mean: ', mean_data)

    median_data = median(data)
    print('Median: ', median_data)

    var = variance(data)
    print('Variance: ', var)

    cv=CV(data)
    print('Coeff. of Variance: ',cv)

    lr=Lexis_Ratio(data)
    print('Lexis Ratio: ',lr)

    skewness=skew(data)
    print('Skewness: ',skewness)
