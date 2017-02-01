#-------------------------------------------------------
#Now let us save only the data around the transit
#xt, ft -> time and flux between the limits ltl and rtl
#xt_ot, ft_ot -> time and flux between the limits ltl and rtl
#                but outside the transit
def extract_transits(T0,P,time_local,flux_local,ltl_local,rtl_local,n_transits_local,toler):
  xt = []
  ft = []
  xt_ot = [] #out of transit time
  ft_ot = [] #out of transit flux
  xt_dummy = []
  ft_dummy = []
  xt_ot_dummy = []
  ft_ot_dummy = []
  j = 0
  if ( max(time_local) < rtl_local[n_transits_local-1] ):
    rtl_local[n_transits_local-1] = time_local[len(time_local)-2]
  for i in range(0,len(time_local)):
    if ( time_local[i] > ltl[j] and time_local[i] < rtl[j]):
      xt_dummy.append(time_local[i])
      ft_dummy.append(flux_local[i])
      t0_dummy = T0 + P*j
      if ( time_local[i] < ( t0_dummy - ttran/2. ) or \
           time_local[i] > ( t0_dummy + ttran/2. ) ):
        xt_ot_dummy.append(time_local[i])
        ft_ot_dummy.append(flux_local[i])
    elif(time_local[i] > rtl[j] and len(xt_ot_dummy) > toler ): #to skip gaps in data
      xt.append(list(xt_dummy))
      ft.append(list(ft_dummy))
      xt_dummy = []
      ft_dummy = []
      xt_ot.append(list(xt_ot_dummy))
      ft_ot.append(list(ft_ot_dummy))
      xt_ot_dummy = []
      ft_ot_dummy = []
      j = j + 1
      if ( j  == n_transits ):
       break
    elif(time_local[i] > rtl[j] and len(xt_ot_dummy) <= toler ): #to skip gaps in data
      j = j + 1
      xt_dummy = []
      ft_dummy = []
      xt_ot_dummy = []
      ft_ot_dummy = []

  print 'I found', len(xt), 'transits'

  return xt, ft, xt_ot, ft_ot
#-------------------------------------------------------
#Plot light curve
#-------------------------------------------------------
def plot_light_curve():

  #m  ax time
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

def plot_individual_tr1():
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


def plot_individual_tr2():
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

#
#x and y are the original arrays, z is the vector with the residuals
def sigma_clip(x,y,z,limit_sigma=3):
  control = True
  new_y = list(y)
  new_x = list(x)
  new_z = list(z)
  dummy_x = []
  dummy_y = []
  dummy_z = []
  n = 1
  while ( control ):
    sigma = np.std(new_z)
    for i in range(0,len(new_z)):
      if ( np.abs(new_z[i]) < limit_sigma*sigma ):
        dummy_x.append(new_x[i])
        dummy_y.append(new_y[i])
        dummy_z.append(new_z[i])
    if ( len(dummy_x) == len(new_x) ): #We did not cut, so the sigma clipping is done
      control = False
    new_y = list(dummy_y)
    new_x = list(dummy_x)
    new_z = list(dummy_z)
    dummy_x = []
    dummy_y = []
    dummy_z = []
    n = n + 1

  plt.plot(x,y,'or',new_x,new_y,'ob')
  plt.show()

  return new_x, new_y

#z has to be calculated from the t
def transito(t,a,u1,u2,k):
  global T0, P

  pars = [T0,P,0.0,np.pi/2,0.0,a]

  z = pti.find_z(t,pars)
  flujo, dummy_var = pti.occultquad(z,u1,u2,k)

  return flujo
