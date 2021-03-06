#!/usr/bin/python

#Load libraries
from __future__ import print_function, division, absolute_import
import sys
sys.path.append('./src')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import exomodule as exo
from scipy.optimize import curve_fit

#Read the input file
exec(open('src/default.py').read())
exec(open('input.py').read())
#Load the functions file
exec(open('src/functions.py').read())

if ( is_seaborn ):
  import seaborn as sns
  sns.set_color_codes()
  sns.set(style='ticks')

#Total time to take into account
td = ttran + toutt

if ( file_separator == None ):
  time, flux = np.loadtxt(lc_file\
             ,comments='#',unpack=True, usecols=[0,1])
else:
  time, flux = np.loadtxt(lc_file,delimiter=file_separator,\
             comments='#',unpack=True, usecols=[0,1])


mean_flux = np.mean(flux)

flux = flux / mean_flux

#Let us obtain the limits of the first transit,
#Transit duration + out of the transit data (this comes from the input file)
ftl = T0 - td / 2.0
ftr = T0 + td / 2.0

print('This is the whole light curve')
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
xt, ft, xt_ot, ft_ot = extract_transits(T0,P,time,flux,ltl,rtl,n_transits,toler)

#If there are gaps in the data, the number of transit can be smaller than the
#expected number of transits. The real number of transits is:
total_n_transits = len(xt_ot)

print('Individual transits')
#Plot the individual transits
plot_individual_tr1()

#---------------  Transits found  -----------------------

#---------------   Correct data   -----------------------

#Time to detrend the data
#this will save the polinomio coefs
coefs = [None]*total_n_transits
#this will save the polinomio funcions
polin = [None]*total_n_transits

print('FITTING POLINOMIAL ORDER = ', porder)
if ( method[0] == 's' ):
  print ('METHOD = SUBSTRACTION ')
if ( method[0] == 'd' ):
  print ('METHOD = DIVISION ')

#Find the best fit for each out-of-transit points
for i in range(0,total_n_transits):
  coefs[i] = np.polyfit(xt_ot[i],ft_ot[i],porder)
  polin[i] = np.poly1d((coefs[i]))

#Now, let us correct the transit data
#new_* variables -> detrended time and flux data
new_xt = list(xt)        #time for each transit
new_ft = list(ft)        #flux for each transit
new_xt_ot = list(xt_ot)  #time for each out-of-transit data
new_ft_ot = list(ft_ot)  #flux for each out-of-transit data
for i in range(0,len(ft)):
  for j in range(0,len(ft[i])):
     if ( method[0] == 'd' ):
       new_ft[i][j] = ft[i][j] / polin[i](xt[i][j])
     elif( method[0] == 's' ):
       new_ft[i][j] = ft[i][j] - polin[i](xt[i][j]) + 1.0
for i in range(0,len(ft_ot)):
  for j in range(0,len(ft_ot[i])):
     if ( method[0] == 'd' ):
       new_ft_ot[i][j] = ft_ot[i][j] / polin[i](xt_ot[i][j])
     elif( method[0] == 's' ):
       new_ft_ot[i][j] = ft_ot[i][j] - polin[i](xt_ot[i][j]) + 1.0

#Now all the detrending data is stored

#---------------   Data corrected   -----------------------

#Plot the corrected transits
print('detrended transits')
plot_individual_tr2()

#phase_xt vector would have the folded-time data
phase_xt = list(new_xt)

print('Folded transits')
#Let us fold all the transits and plot the final result
plt.figure(1,figsize=(10,10/1.618))
for i in range(0,total_n_transits):
  plt.title('Folded transits')
  pfactor = new_xt[i][len(new_xt[i])-1] - new_xt[0][0]
  pfactor = np.float64(int(pfactor / P))
  phase_xt[i] = new_xt[i] - pfactor*P
  plt.plot(phase_xt[i],new_ft[i],'o')
  plt.ticklabel_format(useOffset=False, axis='y')
plt.show()

#Make the sigma clipping here
#--------------------------------------------

print('STARTING SIGMA-CLIPPING')
print('with = ',lsigma,'-sigma')

#Create the vectos which will be used during the fit
#The vector with the time stamps
vec_xt = np.concatenate(new_xt)
#The vector with the time-folded data
vec_phase = np.concatenate(phase_xt)
#The vector with the flux data
vec_flux  = np.concatenate(new_ft)

#Setting priors
p0 = [a,u1,u2,k,b]

#params limits
param_bounds=([min_a,min_u1,min_u1,min_k,min_b], \
              [max_a,max_u1,max_u2,max_k,max_b])


mixmin = min(new_xt[0])
mixmax = max(new_xt[0])
mivec = np.arange(mixmin,mixmax,(mixmax-mixmin)/100.)

#Let us create the data to plot the model
if ( is_fix_parameters ):
  print('I AM USSING THE INPUT PARAMETERS')
  fitted_flux = transito(mivec,a,u1,u2,k,b)
  zero_flux = transito(vec_phase,a,u1,u2,k,b)
else:
  print('I AM FITTING THE DATA')
  #Find the best fit values by fitting a Mandel & Agol (2010) model
  popt, psigma = curve_fit(transito,vec_phase,vec_flux,p0=p0,bounds=param_bounds)
  fitted_flux = transito(mivec, popt[0], popt[1], popt[2], popt[3],popt[4])
  #Extract the best model from the data
  zero_flux = transito(vec_phase, popt[0], popt[1], popt[2], popt[3],popt[4])

#print 'DOES THE CURVE LOOKS LIKE YOUR DATA?'
#Plot fitted light curve
plt.plot(mivec,fitted_flux,vec_phase,vec_flux,'o')
plt.show()

#Start to do the sigma clipping
zero_flux = vec_flux - zero_flux

ot_fvector = np.concatenate(new_ft_ot)
ot_xvector = np.concatenate(new_xt_ot)
zero_flux_ot = [1.0]*len(ot_fvector)
zero_flux_ot = zero_flux_ot - ot_fvector

print('SIGMA-CLIPPING ENDED')
print('BLUE POINTS -> good data')
print('RED POINTS  -> rejected data')
c,d = sigma_clip(vec_phase,vec_flux,zero_flux,lsigma,True)
a,b = sigma_clip(vec_xt,vec_flux,zero_flux,lsigma,False)

#Let us do the sigma clipping for the out of the transit data
c,d = sigma_clip(ot_xvector,ot_fvector,zero_flux_ot,lsigma,False)

err_flux = np.std(d) #calculated from the out of the transit points
if ( fix_error ):
  err_flux = fixed_error

#Let us create the detrended file
out_f = lc_file[:-4] + '_detrended' + lc_file[-4:]
print("CREATING OUTPUT FILE = ", out_f)
of = open(out_f,'w')
for i in range(0,len(a)):
  of.write(' %8.8f   %8.8f  %8.8f \n'%(a[i],b[i],err_flux))

of.close()
