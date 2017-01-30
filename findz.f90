!-----------------------------------------------------------
!                     find_z
!  This suborutine finds the projected distance between
!  the star and planet centers. Eq. (5), ( z = r_sky) from
!  Winn, 2010, Transit and Occultations.
!------------------------------------------------------------
subroutine find_z(t,pars,t0_vec,flag,z,ts,n_transits)
implicit none

!In/Out variables
  integer, intent(in) :: ts, n_transits
  double precision, intent(in), dimension(0:ts-1) :: t
  double precision, intent(in), dimension(0:5) :: pars
  double precision, intent(in), dimension(0:n_transits-1) :: t0_vec
  double precision, intent(out), dimension(0:ts-1) :: z
  logical, intent(in), dimension(0:3) :: flag
!Local variables
  double precision, dimension(0:ts-1) :: ta, swt
  double precision :: t0, P, e, w, i, a
  double precision :: si, new_t0, ttot
  double precision :: pi = 3.1415926535897932384626d0
  integer :: n, j
!External function
  external :: find_anomaly
!

  t0  = pars(0)
  P   = pars(1)
  e   = pars(2)
  w   = pars(3)
  i   = pars(4)
  a   = pars(5)

  if ( flag(0) ) P = 1.d0**pars(1)
  if ( flag(1) ) then
    e = pars(2) * pars(2) + pars(3) * pars(3)
    w = atan2(pars(2),pars(3))
  end if
  !Let us get the w of the planet
  w = w + pi
  if (flag(3)) a = 10.0**a
  if (flag(2)) i = acos( i / a * ( 1.d0 + e * sin(w) ) / ( 1.d0 - e*e ) )

  !Let us estimate the eclipse duration to rule out the no real recondary transits
  !For a planet with radius 0.0. This would not affect the method
  ttot = (1.d0 + 0.d0)**2 - ( a * cos(i) * (1.0d0 - e*e) / ( 1.0d0 + e * sin(w)) )**2
  ttot = asin( ttot / a / sin(i) )
  ttot = P * ttot / pi * sqrt(1.0 - e*e) / ( 1.d0 + e*sin(w) )

 !Obtain the eccentric anomaly by using find_anomaly
  if ( 1 == 1 ) then
   !Calculate the projected distance depending on the T0
   do n = 0, ts - 1
     j = int( ( t(n) - t0 ) / P )
     call find_anomaly(t(n),t0_vec(j),e,w,P,ta(n),1)
     !print *, t0_vec(j)
   end do
  else if ( 1 == 0) then
   !Calculate the projected distance assuming there are no TTVs
   call find_anomaly(t,t0,e,w,P,ta,ts)
  end if

  swt = sin(w+ta)

  si = sin(i)
  z = a * ( 1.d0 - e * e ) * sqrt( 1.d0 - swt * swt * si * si ) &
      / ( 1.d0 + e * cos(ta) )
  !z has been calculated

  !Let us remove the secondary transits
  do n = 0, ts - 1
    j = int( ( t(n) - t0 ) / P )
    new_t0 = t0 + j*P
    if ( t(n) > t0 + j*P + ttot .and. t(n) < t0 + (j+1)*P - ttot ) &
      z(n) = 1.d1
  end do

end subroutine
