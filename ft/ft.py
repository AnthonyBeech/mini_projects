import numpy as np
import math as mt
import cmath as cmt
import matplotlib.pyplot as plt


#number of samples and frequency
L=8
N=2**L  
f=10         
print(N)

#create empty array
sig = np.zeros((2*N, N), dtype=np.complex) 


#define input function
for i in range(N):                                    
    sig[0,i] = mt.cos(2*mt.pi*f*i/N)
    sig[1,i] = sig[0,i]
    
    
#perform discrete hilbert transform to produce imaginary component
for k in range(N):                        
    if (k % 2) == 0:
        for n in range(N):
            if (n % 2) != 0:
                sig[1,k]=sig[1,k]+(2/mt.pi)*sig[0,n]/(k-n)*1j
    else:
        for n in range(N):
            if (n % 2) == 0:
                sig[1,k]=sig[1,k]+(2/mt.pi)*sig[0,n]/(k-n)*1j 
              
                
#perform fourier transform
for j in range(N):
    for n in range(N):
        sig[2,j]=sig[2,j]+sig[1,n]*cmt.exp(-1j*2*mt.pi*j*n/N)
        
        
#print results
plt.plot(sig[1].real, label="R")
plt.plot(sig[1].imag, label="I")
plt.legend()
plt.show()

plt.plot(sig[2].real, label="R")
plt.plot(sig[2].imag, label="I")
plt.legend()
plt.show()
