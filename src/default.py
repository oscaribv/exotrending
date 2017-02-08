#Default commands for chidetrending

lc_file='warm_jupiter.dat'
is_seaborn = False
method = 'substraction'
file_type = 'V'
toler = 2
lsigma = 3.0
porder = 2
fixed_error = 1.0
fix_error = False
is_fix_parameters = False
file_separator = ' '
P = 28.38229
T0 = 7325.81705 - 4833.0
ttran = 5.0/24.0
td = ttran + 10./24.

#priors
a =  4.56
u1 = 0.5
u2 = 0.41
k  = 0.0172

#prior ranges
min_a = 2.0
max_a = 100.0
min_u1 = 0.0
max_u1 = 1.0
min_u2 = -1.0
max_u2 = 1.0
min_k = 0.0
max_k = 1.0
