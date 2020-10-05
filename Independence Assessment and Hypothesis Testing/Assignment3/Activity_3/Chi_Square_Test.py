from Read_Data import getData
import matplotlib.pyplot as plt
import math

def Inv_Distr(y,a=1.5278996202501096,b=1.2999425079066453):

    result = b * (-(math.log(1 - y))) ** (1 / a)
    return result

def Indiv_Chi(Nj,nPj):
    x=(Nj-nPj)**2
    x/=nPj
    return x

def Calc_Chi_Square(data,k):
    n=len(data)
    Pj = 1 / k
    nPj = n * Pj
    chi=0
    a0=0.0
    a1=0.0
    for i in range(1,k):
        a1=Inv_Distr(i/k)
        cnt=0
        for d in data:
            if a0<=d<a1:
                cnt+=1
        chi+=Indiv_Chi(cnt,nPj)
        print('j: %d Interval= [%f, %f) nPj= %f  Nj= %d ((Nj-nPj)^2)/nPj= %f'%(i,a0,a1,nPj,cnt,Indiv_Chi(cnt,nPj)))
        a0=a1


    #last interval
    a0=a1
    a1=max(data)+0.1
    cnt = 0
    for d in data:
        if a0 <= d < a1:
            cnt += 1
    chi += Indiv_Chi(cnt, nPj)
    print('j: %d Interval= [%f, %f) nPj= %f  Nj= %d ((Nj-nPj)^2)/nPj= %f' % (k, a0, a1, nPj, cnt, Indiv_Chi(cnt, nPj)))
    return chi

if __name__=='__main__':
    data=getData()
    k=15
    chi_test=Calc_Chi_Square(data,k)
    alpha05=23.685
    alpha10=21.064

    print('\nNo. of Intervals k: ',k)
    print('X2: ', chi_test)
    print('X2(15-1,1-0.05): ',alpha05)
    print('X2(15-1,1-0.10): ', alpha10)
    print('\n')

    if(chi_test>=alpha05):
        print('Reject the Hypothesis at alpha=0.05')
    else:
        print('Cannot Reject the Hypothesis at alpha=0.05')
    if (chi_test > alpha10):
        print('Reject the Hypothesis at alpha=0.10')
    else:
        print('Cannot Reject the Hypothesis at alpha=0.10')



