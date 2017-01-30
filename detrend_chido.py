#Load libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
sns.set(style='ticks')

lc_file='dbf1.txt'
#lc_file='C8_3386_left.txt'
#lc_file='C8_3386_right.txt'
#Ephemeris planet b
planet = 'b'
if ( planet == 'b' ):
  lc_file='dbf1-b.txt'
  P = 0.959628
  T0 = 7394.37450 - 4833.0
  #T0 = 2589.203712
  ttran = 1.7/24.0
  td = ttran + 4.1/24.0
if ( planet == 'c' ):
  lc_file='dbf1-c.txt'
  P = 29.8454
  T0 = 7394.9788 - 4833.0
  ttran = 4.81/24.0
  td = ttran + 8./24.0

#Load functions' file
execfile("./functions.py")

#time, flux = np.loadtxt(lc_file,delimiter=',', \
time, flux = np.loadtxt(lc_file, \
            comments='#',unpack=True, usecols=[0,1])


#limits first transit
ftl = T0 - td / 2.0
ftr = T0 + td / 2.0

#This can be part of a function to create the light curve plot
#-----------------------------------------------------------

#max time
maxt = max(time)

#We expect to have n_transits
n_transits = ( maxt - T0 ) / P
n_transits = int(n_transits + 1)

T0_vec = [0.0]*n_transits
for n in range(0,n_transits):
  T0_vec[n] = T0 + n*P

plt.figure(1,figsize=(25/2.56,6.5/2.56))
plt.xlim(min(time)-5,max(time)+5)
for n in range(0,n_transits):
  plt.axvline(x=T0_vec[n],c='r',ls='--',lw=1,alpha=0.3)
plt.plot(time,flux,'.',markersize=5)
plt.minorticks_on()
plt.xlabel('BJD - 2454833')
plt.ylabel('Relative flux')
plt.savefig('light_curve.pdf',bbox_inches='tight')
plt.show()

#-----------------------------------------------------------

#limits first transit
ftl = T0 - td / 2.0
ftr = T0 + td / 2.0

#max time
maxt = max(time)

#We expect to have n_transits
n_transits = ( maxt - T0 ) / P
n_transits = int(n_transits + 1)

#left transit limits
ltl = [None]*n_transits
#rigth transit limits
rtl = [None]*n_transits

#Fill the transit limit vectors
for i in range(0,n_transits):
  ltl[i] = ftl + P*i
  rtl[i] = ftr + P*i

xt, ft, xt_ot, ft_ot = extract_transits(T0,P,time,flux,ltl,rtl,n_transits)

#If there are gaps in the data,
#   it can be a smaller number of transits than expected
total_n_transits = len(xt_ot)

plt.figure(1,figsize=(7,1.708*total_n_transits/2))
gs = gridspec.GridSpec(nrows=(total_n_transits+1)/2,ncols=2)
for i in range(0,total_n_transits):
  plt.subplot(gs[i])
  plt.xlabel('time (days)')
  plt.ylabel('Relative flux')
  plt.plot(xt[i],ft[i],'k')
  plt.plot(xt_ot[i],ft_ot[i],'ro')
  plt.minorticks_on()
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()



#Time to fit the data to a quadratic law
#this will save the polinomio coefs
coefs = [None]*total_n_transits
#this will save the polinomi funcions
polin = [None]*total_n_transits
for i in range(0,total_n_transits):
  coefs[i] = np.polyfit(xt_ot[i],ft_ot[i],2) #2nd order polynomial
  polin[i] = np.poly1d((coefs[i]))

#Now, let us correct the transit data
#dtime, dflux -> detrended time and flux data
#A one dimensional array with all the data
dtime = []
dflux = [] 
for i in range(0,total_n_transits):
  for j in range(0,len(xt[i])):
    dtime.append(xt[i][j])
    dflux.append(ft[i][j] / polin[i](xt[i][j]) )

new_xt, new_ft, new_xt_ot, new_ft_ot = extract_transits(T0,P,dtime,dflux,ltl,rtl,n_transits)

plt.figure(1,figsize=(12,3.708*total_n_transits/2))
gs = gridspec.GridSpec(nrows=(total_n_transits+1)/2,ncols=2)
for i in range(0,total_n_transits):
  plt.subplot(gs[i])
  plt.xlabel('time (days)')
  plt.ylabel('Relative flux')
  plt.plot(new_xt[i],new_ft[i],'k')
  plt.plot(new_xt_ot[i],new_ft_ot[i],'ro')
  plt.minorticks_on()
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()




#Create a vector with all the out of transit data
total_ft_ot = np.concatenate(new_ft_ot)

#plt.hist(total_ft_ot,bins=50)
#plt.ticklabel_format(useOffset=False, axis='x')
#plt.show()

fsigma = [None]*len(new_ft_ot)

for i in range(0,len(fsigma)):
  fsigma[i] = np.std(new_ft_ot[i])

total_fsigma = [None]*len(dtime)
n = 0
for i in range(0,len(new_xt)):
  for j in range(0,len(xt[i])):
    total_fsigma[n] = fsigma[i]
    n = n + 1

#Let us folded all the transits
plt.figure(1,figsize=(10,10/1.618))
for i in range(0,total_n_transits):
  plt.title('Folded transits')
  pfactor = new_xt[i][len(new_xt[i])-1] - new_xt[0][0]
  pfactor = np.float64(int(pfactor / P))
  #plt.plot(new_xt[i]-pfactor*P,new_ft[i],'.')
  plt.errorbar(new_xt[i]-pfactor*P,new_ft[i],fsigma[i],fmt='.')
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()


#Let us create or detrended file
out_f = lc_file[:-4] + '_detrended' + lc_file[-4:]
of = open(out_f,'w')
#of.write('#This detrended light curve was created with pyaneti/lunas\n')
for i in range(0,len(dtime)):
  #of.write(' %8.8f   %8.8f  %8.8f \n'%(dtime[i],dflux[i],total_ft_ot))
  of.write(' %8.8f   %8.8f  %8.8f \n'%(dtime[i],dflux[i],total_fsigma[i]))

of.close()
