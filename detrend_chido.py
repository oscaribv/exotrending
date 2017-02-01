#!/usr/bin/python

#Load libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
import orbits as pti
from scipy.optimize import curve_fit
sns.set_color_codes()
sns.set(style='ticks')

#Read the input file
execfile("./input.py")

#Load the functions file
execfile("./functions.py")

#Which kind of file?
#Vanderburg-like
if ( file_type[0] == 'V' ):
  time, flux = np.loadtxt(lc_file, comments='#',unpack=True, usecols=[0,1])
#Everest-like
elif( file_type[0] == 'E' ):
  time, flux = np.loadtxt(lc_file,delimiter=',',comments='#',unpack=True, usecols=[0,1])

#Let us obtain the limits of the first transit,
#Transit duration + out of the transit data (this comes from the input file)
ftl = T0 - td / 2.0
ftr = T0 + td / 2.0

#Plot a nice light curve, to change plot options in functions.py
plot_light_curve()

#---------------Time to find the transits-----------------------

#The maximum value of the time
maxt = max(time)

#Since we know the period, we can calcualte the expect number
# of transits -> n_transits
n_transits = ( maxt - T0 ) / P
n_transits = int(n_transits + 1)

#Vectors to save the limits of each transit
#left transit limits
ltl = [None]*n_transits
#rigth transit limits
rtl = [None]*n_transits
#Fill the transit limit vectors
for i in range(0,n_transits):
  ltl[i] = ftl + P*i
  rtl[i] = ftr + P*i

#now the extract_transits functions, get the transits and the
#out-of-the-transit data
xt, ft, xt_ot, ft_ot = extract_transits(T0,P,time,flux,ltl,rtl,n_transits,2)

#If there are gaps in the data, the number of transit can be smaller than the
#expected number of transits. The real number of transits is:
total_n_transits = len(xt_ot)

#Plot the individual transits
plot_individual_tr1()

#---------------  Transits found  -----------------------

#---------------   Correct data   -----------------------

#Time to detrend the data
#this will save the polinomio coefs
coefs = [None]*total_n_transits
#this will save the polinomio funcions
polin = [None]*total_n_transits

#Find the best fit for each out-of-transit points
for i in range(0,total_n_transits):
  coefs[i] = np.polyfit(xt_ot[i],ft_ot[i],porder) #2nd order polynomial
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

#Now all the detrending data is stored in a single vector
#dtime and dflux

#---------------   Data corrected   -----------------------

#Find the transits in the corrected data
new_xt, new_ft, new_xt_ot, new_ft_ot = extract_transits(T0,P,dtime,dflux,ltl,rtl,n_transits,1)

#Plot the corrected transits
plot_individual_tr2()

#phase_xt vector would have the folded-time data
phase_xt = list(new_xt)

#Let us fold all the transits and plot the final result
plt.figure(1,figsize=(10,10/1.618))
for i in range(0,total_n_transits):
  plt.title('Folded transits')
  pfactor = new_xt[i][len(new_xt[i])-1] - new_xt[0][0]
  pfactor = np.float64(int(pfactor / P))
  phase_xt[i] = new_xt[i] - pfactor*P
  plt.plot(phase_xt[i],new_ft[i],'.')
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()

#Make the sigma clipping here
#--------------------------------------------

#Create the vectos which will be used during the fit
#The vector with the time stamps
vec_xt = np.concatenate(new_xt)
#The vector with the time-folded data
vec_phase = np.concatenate(phase_xt)
#The vector with the flux data
vec_flux  = np.concatenate(new_ft)

#Setting priors
p0 = [a,u1,u2,k]

#params limits
param_bounds=([min_a,min_u1,min_u1,min_k], \
              [max_a,max_u1,max_u2,max_k])

#Find the best fit values by fitting a Mandel & Agol (2010) model
popt, psigma = curve_fit(transito,vec_phase,vec_flux,p0=p0,bounds=param_bounds)
#popt[0] = a, popt[1] = u1, popt[2] = u2, popt[3] = k = Rp/R*

#Let us create the data to plot the model
fitted_flux = transito(new_xt[0], popt[0], popt[1], popt[2], popt[3])

#Plot fitted light curve
plt.plot(new_xt[0],fitted_flux,vec_phase,vec_flux,'o')
plt.show()

#Start to do the sigma clipping

#Extract the best model from the data
zero_flux = transito(vec_phase, popt[0], popt[1], popt[2], popt[3])

zero_flux = vec_flux - zero_flux

c,d = sigma_clip(vec_phase,vec_flux,zero_flux,lsigma)
a,b = sigma_clip(vec_xt,vec_flux,zero_flux,lsigma)

#Extract the best model from the data
#zero_flux = transito(dtime, popt[0], popt[1], popt[2], popt[3])

#zero_flux = dflux - zero_flux

#c,d = sigma_clip(vec_phase,vec_flux,zero_flux,lsigma)
#a,b = sigma_clip(dtime,dflux,zero_flux,lsigma)

#new_xt, new_ft, new_xt_ot, new_ft_ot = extract_transits(T0,P,a,b,ltl,rtl,n_transits,1)
err_flux = np.std(np.concatenate(new_ft_ot)) #calculated from the out of the transit points

#Let us create or detrended file
out_f = lc_file[:-4] + '_detrended' + lc_file[-4:]
of = open(out_f,'w')
#of.write('#This detrended light curve was created with pyaneti/lunas\n')
for i in range(0,len(a)):
  of.write(' %8.8f   %8.8f  %8.8f \n'%(a[i],b[i],err_flux))

of.close()
