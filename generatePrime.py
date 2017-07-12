__author__ = 'Y'

import math
import random
import time


isPrime=range(1,10002)

prime=[]

def initPrime():
    for i in range(1,10000):
        isPrime[i]=True
    isPrime[0]=False
    isPrime[1]=False
    isPrime[2]=True


def generatePrime():
    for i in range(2,int(math.sqrt(10000) )):
        if(isPrime[i]):
            j=2*i
            while (j < 10000):
                isPrime[j]=False
                j+=i
    j=1;
    while j <10000:
        if (isPrime[j]):
            prime.append(j)
        j=j+1
    #print len(prime)
    #print prime

def getAPrime():

    a=random.randint(2**10,2**14)
    if(a%2==0):
        a=a+1
    for i in range(1, len(prime)):
        if (a%prime[i]==0):
            return getAPrime()
    #Miller -Rabin Test
    #1 2^s*d
    s=0
    d=(a-1)
    while True:
        quotient,remainder=divmod(d,2)
        if remainder==1:
            break;
        s+=1
        d=quotient
    assert (2**s*d== a-1 )

    def try_composite(b):
        if pow(b,d,a)==1:
            return False;
        for i in range(s):
            if pow(b,2**i*d,a) == a-1:
                return False
        return True

    #2 Test r in [0,s-1]
    for  i in range(3):
        b=random.randrange(2,a)
        if try_composite(b):
            return getAPrime()
    return a


def inverse(a,n):
    t=0
    r=n
    newt=1
    newr=a

    while newr!=0:
        quotient,remainder=divmod(r,newr)
        (t,newt)=(newt,t-quotient*newt)
        (r,newr)=(newr,r-quotient*newr)
    if t<0 :
        t=t+n
    return t

def gcd(a,b):
    if(a<b):
        temp=a
        a=b
        b=temp
    if(b==0):
        return a
    else:
        return gcd(b,a%b)

def fast_pow(base , pow,n):

    if(pow==0):
        return 1
    elif (pow==1):
        return base

    if(pow%2==0):
        return (fast_pow(base,pow/2,n)%n*fast_pow(base,pow/2,n)%n)%n
    elif(pow%2==1):
        return (fast_pow(base,pow/2,n)%n*fast_pow(base,pow/2,n)%n)*base%n


def encryption(plain_text,public_key,n):
    encrypted_text=[]
    nums=len(plain_text)

    for i in range(0,nums) :
        #print i
        #encrypted_text.append((plain_text[i]**public_key)%n)
        encrypted_text.append( fast_pow(plain_text[i],public_key,n)%n )


    return encrypted_text;

def decrpytion(encrypted_text,private_key,n):

    plain_text=[]
    nums=len(encrypted_text)

    for i in range(0,nums):
        #plain_text.append(encrypted_text[i]**private_key%n)
        plain_text.append( fast_pow(encrypted_text[i],private_key,n)%n )
    return plain_text



def toNumber(ch):

    return ord(ch)

def toString(plain_text):
    result=[]
    for i in range( len(plain_text) ):
         result.append( unichr(plain_text[i]) )
    return result

def test():
    e=79
    d=1019
    n=3337
    faiN=3220
    print "Test Case:"
    print "Public Key : ("+str(e)+","+str(n)+")"
    print "Private Key: ("+str(d)+","+str(n)+")"

    #print "Plain text:"
    pt=[82,83,65]
    print "Plain text:" +str(pt)
    print "In UniCode is:"+str( toString(pt) )
    c1=encryption(pt,e,n)
    print toString(pt)
    print "Cipher text:"+str(c1)
    d1=decrpytion(c1,d,n)
    print "After decryption:"+str(d1)


if __name__ == '__main__':

    initPrime()
    generatePrime()
    '''
    for i  in range(1,16384):
        if(isPrime[i]==True):
            print(str(i) + " ");
                '''
    print "Here is a simple test. If you want to know more about this test case,please check function test()"
    test()

    print "-----------------------------------------------------------------------"
    print "Following test case uses very big prime number, so it costs time."
    p1=getAPrime()
    p2=getAPrime()
    print "The first prime:"+str(p1)
    print "The second prime:"+str(p2)
    faiN=(p1-1)*(p2-1)
    print "faiN:"+str(faiN)
    #public key
    public_key_e=random.randint(2,faiN);
    while gcd(public_key_e,faiN)!=1:
        public_key_e=random.randint(2,faiN)
    #private key
    private_key_d=inverse(public_key_e,faiN)

    #print 'e:'+str(public_key_e)
    #print 'd:'+str(private_key_d)
    #print 'e*d mod fai(N)'+str( (public_key_e%faiN)*(private_key_d%faiN)%faiN  )

    print 'Public Key:('+str(public_key_e)+","+str(p1*p1)+")"
    print str(p1*p2)
    print 'Private Key:'+str(private_key_d)+","+str(p1*p2)+")"
    print str(p1*p2)

    word=raw_input("Please a word:")
    plain_text=[]
    print
    for i in range(0,len(word)):
        plain_text.append( toNumber( (word[i]) ) )
    print "Plain text:"+str(plain_text)
    time_a=time.time()
    encrypted_text=encryption(plain_text,public_key_e,p1*p2)
    time_b=time.time()
    time_diff=time_b-time_a
    print "Encryption Time use :"+str( (int(time_diff)/60))+" minute"+str((int(time_diff)%60))+" seconds"
    #print 'out'
    print "Encryption text:"+str(encrypted_text)
    time_a=time.time()
    test_dec=decrpytion(encrypted_text,private_key_d,p1*p2)
    time_b=time.time()
    time_diff=time_b-time_a
    print "Decryption Time used :"+str( int(time_diff/60) )+" minute"+str (int(time_diff%60))+" seconds"
    print "Decryption text:"+str( test_dec )


