#-------------------------------------------------------
#Now let us save only the data around the transit
#xt, ft -> time and flux between the limits ltl and rtl
#xt_ot, ft_ot -> time and flux between the limits ltl and rtl
#                but outside the transit
def extract_transits(T0,P,time_local,flux_local,ltl_local,rtl_local,n_transits_local):
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
    elif(time_local[i] > rtl[j] and len(xt_ot_dummy) > 2 ): #to skip gaps in data
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
    elif(time_local[i] > rtl[j] and len(xt_ot_dummy) < 2 ): #to skip gaps in data
      j = j + 1
      xt_dummy = []
      ft_dummy = []
      xt_ot_dummy = []
      ft_ot_dummy = []
      if ( j  == n_transits ):
       break

  print 'I found', len(xt), 'transits'

  return xt, ft, xt_ot, ft_ot
#-------------------------------------------------------
