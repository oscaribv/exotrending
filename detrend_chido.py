#Load libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
import pyaneti as pti
from scipy.optimize import curve_fit
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

plot_light_curve()

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

plot_individual_tr1()

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

phase_xt = list(new_xt)

plot_individual_tr1()

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
  phase_xt[i] = new_xt[i] - pfactor*P
  #plt.errorbar(new_xt[i]-pfactor*P,new_ft[i],fsigma[i],fmt='.')
  plt.errorbar(phase_xt[i],new_ft[i],fsigma[i],fmt='.')
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()

#Make the sigma clipping here
#--------------------------------------------

#--------------------------------------------
#z has to be calculated from the t
def transito(t,a,u1,u2,k):
  global T0, P

  flag = [False,False,True,False]
  pars = [T0,P,0.0,np.pi/2,0.0,a]

  t0_vec = [T0]
  z = pti.find_z(t,pars,t0_vec,flag)
  flujo, dummy_var = pti.occultquad(z,u1,u2,k)

  return flujo

vec_xt = np.concatenate(new_xt)
vec_phase = np.concatenate(phase_xt)
vec_flux  = np.concatenate(new_ft)

p0 = [10.0,0.5,0.5,0.1]

#bounds = [[2.0,10.0],[0.0,1.0],[0.0,1.0],[0.0,0.2]]
param_bounds=([2.0,0.0,0.0,0.0],[100.,1.0,1.0,0.2])

popt, psigma = curve_fit(transito,vec_phase,vec_flux,p0=p0,bounds=param_bounds)


#Let us create the data to plot the model
fitted_flux = transito(new_xt[0], popt[0], popt[1], popt[2], popt[3])

#Plot fitted light curve
plt.plot(new_xt[0],fitted_flux,vec_phase,vec_flux,'o')
plt.show()

#Start to do the sigma clipping

#Extract the best model from the data
zero_flux = transito(vec_phase, popt[0], popt[1], popt[2], popt[3])

zero_flux = vec_flux - zero_flux

#Start the sigma-clipping

plt.plot(vec_phase,zero_flux,'o')

sys.exit()

#Let us create or detrended file
out_f = lc_file[:-4] + '_detrended' + lc_file[-4:]
of = open(out_f,'w')
#of.write('#This detrended light curve was created with pyaneti/lunas\n')
for i in range(0,len(dtime)):
  of.write(' %8.8f   %8.8f  %8.8f \n'%(dtime[i],dflux[i],total_ft_ot))
  #of.write(' %8.8f   %8.8f  %8.8f \n'%(dtime[i],dflux[i],total_fsigma[i]))

of.close()
