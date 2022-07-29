import numpy as np
import math as mt
import cmath as cmt
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)


#Define size and frequency of input
L=3
N=2**L
f=10
print(N)


#create empty array for storing real and analytical function
sig_r = np.zeros((2*N, N), dtype=np.complex)   
sig = np.zeros((2*N, N), dtype=np.complex) 
V = np.zeros(N, dtype=np.complex)


#define input function
for i in range(N):                                    
    sig_r[0,i] = mt.cos(2*mt.pi*f*i/N)
    sig[0,i]= sig_r[0,i]
    
    
#perform discrete hilbert transform to produce imaginary component
for k in range(N):                        
    if (k % 2) == 0:
        for n in range(N):
            if (n % 2) != 0:
                sig[0,k]=sig[0,k]+(2/mt.pi)*sig_r[0,n]/(k-n)*1j
    else:
        for n in range(N):
            if (n % 2) == 0:
                sig[0,k]=sig[0,k]+(2/mt.pi)*sig_r[0,n]/(k-n)*1j 

#duplicate input function to perforom transform         
for j in range(N):
    sig[1,j]=sig[0,j]                
         
        
#split input into odd and even parts 2N times
for j in range(N-1):   
    sig[2*j+2][0:(len(sig[j+1])//2):1] = sig[j+1][0::2]
    sig[2*j+3][0:(len(sig[j+1])//2):1] = sig[j+1][1::2]


#zero out the mid calculation values incase they interfere with result
for j in range(1,N,1):
    for n in range(N):      
        sig[j,n]=0
        
        
#Calculate Fourier coefficients
for n in range(N//2):
    V[n]=cmt.exp(-1j*2*mt.pi*n/N)
        
        
#Perform transform by resumming from N=1 arrays
for j in range(N-2,-1,-1): 
    for n in range(np.count_nonzero(sig[2*j+2])):
        sig[j+1,n]=sig[2*j+2,n]+V[n]*sig[2*j+3,n]
        sig[j+1,n+np.count_nonzero(sig[2*j+2])]=sig[2*j+2,n]-V[n]*sig[2*j+3,n]

            
#compare with actual FFT to test result       
sig[2]=np.fft.fft(sig[0])
sig[3]=sig[1]-sig[2]
print(sig[3])


#plot values
plt.plot(sig[1].real, label="R")
plt.plot(sig[2], label="F")
plt.legend()
plt.show()




#L=3

#split input into odd and even parts 2N times
# |a|b|c|d|e|f|g|h|         
# |a|b|c|d|e|f|g|h|
# |a|c|e|g| | | | |
# |b|d|f|h| | | | |
# |a|e| | | | | | |
# |c|g| | | | | | |
# |b|f| | | | | | |
# |d|h| | | | | | |
# |a| | | | | | | |
# |e| | | | | | | |
# |c| | | | | | | |
# |g| | | | | | | |
# |b| | | | | | | |
# |f| | | | | | | |
# |d| | | | | | | |
# |h| | | | | | | |




#Perform transform by re-summing from N=1 arrays
# |a+V0e|a-V0e|
# |c+V0g|c-V0g|  <---------------------
# |b+V0f|b-V0f|                       |
# |d+V0h|d-V0h|                       |
# |a| | | | | | | |                   |
# |e| | | | | | | |                   |
# |c| | | | | | | |                   |
# |g| | | | | | | |                   |
# |b| | | | | | | |                   |
# |f| | | | | | | |                   |
# |d| | | | | | | |                   |
# |h| | | | | | | |                   |
#                                     |
#                                     |
# |a+V0c|b+V1d|a-V0c|b-V1d|    <-----------------------------------------
# |e+V0g|f+V1h|e-V0g|f-V1h|           |                                 |
# |a|b|                               |                                 |
# |c|d|        <-----------------------                                 |
# |e|f|                                                                 |
# |g|h|                                                                 |
#                                                                       |
#                                                                       |
# |a+V0e|b+V1f|c+V2g|d+V3h|a-V0e|b-V1f|c-V2g|d-V3h|                     |
# |a|b|c|d|                                                             |
# |e|f|g|h|     <--------------------------------------------------------






#L=2

#split input into odd and even parts 2N times
# |a|b|c|d|        
# |a|c| | |
# |b|d| | |
# |a| | | |
# |c| | | |
# |b| | | |
# |d| | | |


#Perform transform by re-summing from N=1 arrays
# |a+V0c|a-V0c|
# |b+V0d|b-V0d|  <---------------------
# |a| | | |                           |
# |c| | | |                           |
# |b| | | |                           |
# |d| | | |                           |
#                                     |
#                                     |
# |a+V0c|b+V1d|a-V0c|b-V1d|           |
# |a|b|                               |                                 
# |c|d|        <-----------------------  
