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
        a0=a1


    #last interval
    a0=a1
    a1=max(data)+0.1
    cnt = 0
    for d in data:
        if a0 <= d < a1:
            cnt += 1
    chi += Indiv_Chi(cnt, nPj)
    return chi



