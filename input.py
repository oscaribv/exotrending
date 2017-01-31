#Input routines
lc_file='dbf1.txt'
lsigma = 3
porder = 2
lc_file='C8_3386_left.txt'
lc_file='C8_3386_right.txt'
#Ephemeris planet b
planet = 'b'
file_type = 'E'
if ( planet == 'b' ):
  #lc_file='dbf1-b.txt'
  lc_file='C8.txt'
  P = 0.959628
  T0 = 7394.37450 - 4833.0
  #T0 = 2589.203712
  ttran = 1.7/24.0
  td = ttran + 4.1/24.0
if ( planet == 'c' ):
  lc_file='C8.txt'
  #lc_file='dbf1-c.txt'
  P = 29.8454
  T0 = 7394.9788 - 4833.0
  ttran = 4.81/24.0
  td = ttran + 5./24.0

#priors
a = 10.0
u1 = 0.5
u2 = 0.5
k  = 0.1

min_a = 2.0
max_a = 100.0
min_u1 = 0.0
max_u1 = 1.0
min_u2 = -1.0
max_u2 = 1.0
min_k = 0.0
max_k = 1.0
