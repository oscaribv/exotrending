#Input routines
lc_file='dbf1.txt'
lsigma = 3
porder = 2
#lc_file='C8_3386_left.txt'
#lc_file='C8_3386_right.txt'
#Ephemeris planet b
planet = 'c'
file_type = 'Vanderburg'
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
