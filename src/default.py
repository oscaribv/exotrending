#-----------------------------------------------#
#                  default.py                   #
#        Default commands for exodetrending     #
#       Written by Oscar Barragan, Feb 2017     #
#-----------------------------------------------#

#You can change these variables here, but I recommend you
#to do it in the input.py file

#input light curve file
lc_file='warm_jupiter.dat'

#File separator, default is ' ', it could be ',', '.', etc.
file_separator = ' '

#Default ephemeris
P = 28.38229               #Period (days)
T0 = 7325.81705 - 4833.0   #T0 (days)
ttran = 5.0/24.0           #transit duration (days)
ttout = 10./24.            #out of transit data duration (days)

#Turn it on/off to activate seaborn plots (True or False)
is_seaborn = False

#Method for the detrending (substraction or division)
method = 'substraction'

#Number minimum of data to take into account a transit 
#for the extract_transit function (integer)
toler = 2

#How many sigma do we want for the sigma-clipping?
lsigma = 3.0

#Order of polinomial to fit
porder = 2

#If we want to fix the out put error for the light curve, set it True
fix_error = False
#Set the value that you want to for the error bars
#It works only if fix_error = True
fixed_error = 1.0

#If you have a good solution for your data, you prefer to fix the parameters
#istead of finding the best solution, set it True if the case
is_fix_parameters = False
#priors
#If is_fix_parameters = True, these are the parameters used to perform the sigma-clipping
#If is_fix_parameters = False, these are the priors for the curve_fit routine
a  =  4.56    #scaled semi-major axis
u1 = 0.5      #u1 limb darkening coefficient, Mandel & Agol, 2002
u2 = 0.41     #u2 limb darkening coefficient, Mandel & Agol, 2002
k  = 0.0172   #Scaled planet radius Rp/R*

#if is_fix_parameters = False, these are the ranges for the parameters for curve_fit
min_a = 2.0
max_a = 100.0
min_u1 = 0.0
max_u1 = 1.0
min_u2 = -1.0
max_u2 = 1.0
min_k = 0.0
max_k = 1.0
