from statistics import median,mean,variance
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

min_value=min(data)
max_value = max(data)
mean_data=mean(data)
median_data = median(data)
var = variance(data)
skewness=skew(data)
