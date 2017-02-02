!-----------------------------------------------------------
!                     find_z
!  This suborutine finds the projected distance between
!  the star and planet centers. Eq. (5), ( z = r_sky) from
!  Winn, 2010, Transit and Occultations.
!------------------------------------------------------------
subroutine find_z(t,pars,z,ts)
implicit none

!In/Out variables
  integer, intent(in) :: ts
  double precision, intent(in), dimension(0:ts-1) :: t
  double precision, intent(in), dimension(0:5) :: pars
  double precision, intent(out), dimension(0:ts-1) :: z
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

  i = acos( i / a * ( 1.d0 + e * sin(w) ) / ( 1.d0 - e*e ) )

  !Let us estimate the eclipse duration to rule out the no real recondary transits
  !For a planet with radius 0.0. This would not affect the method
  ttot = (1.d0 + 0.d0)**2 - ( a * cos(i) * (1.0d0 - e*e) / ( 1.0d0 + e * sin(w)) )**2
  ttot = asin( ttot / a / sin(i) )
  ttot = P * ttot / pi * sqrt(1.0 - e*e) / ( 1.d0 + e*sin(w) )

 !Calculate the projected distance assuming there are no TTVs
 call find_anomaly(t,t0,e,w,P,ta,ts)

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

!------------------------------------------------------------
!This subrouotine finds the time of periastron passage
!by knowing the transit time
!------------------------------------------------------------
subroutine find_tp(t0, e, w, P, tp)
implicit none
!In/Out variables
  double precision, intent(in) :: t0, e, w, P
  double precision, intent(out) :: tp
!Local variables
  double precision :: theta_p
  double precision :: ereal, eimag
  double precision :: pi = 3.1415926535897d0

  ereal = e + cos( pi / 2.d0  - w)
  eimag = sqrt( 1.d0 - e * e ) * sin( pi/ 2.d0  - w )
  theta_p = atan2(eimag, ereal )
  theta_p = theta_p - e * sin( theta_p )

  tp = t0 - theta_p * p / 2.d0 / pi

end subroutine

!------------------------------------------------------------
!This subroutine finds the true anomaly of an eccentric orbit
!by using the Newton-Raphson (NR)  algorithm
!The input parameters are:
! man -> mean anomaly, ec -> eccentricity, delta -> NR limit
! imax -> iteration limit for NR, dman -> man dimension
!The output parameters are:
! ta -> True anomaly (vector with the same dimension that man)
!------------------------------------------------------------
subroutine find_anomaly(t,t0,e,w,P,ta,dt)
implicit none
!In/Out variables
  integer, intent(in) :: dt
  double precision, intent(in) , dimension(0:dt-1) :: t
  double precision, intent(out), dimension(0:dt-1) :: ta
  double precision, intent(in) :: t0, e, w, P
!Local variables
  integer :: i,n
  double precision, dimension(0:dt-1) :: ma, f, df, eimag, ereal
  double precision :: two_pi = 2.d0*3.1415926535897932384626d0
  double precision :: uno, tp
  double precision :: fmin=1.d-8
  integer :: imax = int(1e8)
!
  uno = 1.0d0

  call find_tp(t0,e,w,P,tp)

  !Calculate the mean anomaly
  ma = two_pi * ( t - tp ) / P

  !calculate the eccentric anomaly
  !Using Newthon-Raphson algorithm
  ta(:) = ma(:)
  f(:) = fmin * 1.0d1
  n = 0

  do i = 0, dt-1
    do while ( abs(f(i)) > fmin .and. n < imax )
      f(i)   = ta(i) - e * sin(ta(i)) - ma(i)
      df(i)  = uno - e * cos(ta(i))
      ta(i)  = ta(i) - f(i) / df(i)
      n = n + 1
    end do
  end do

  if ( n > imax ) then !This should never happen!
    print *, 'I am tired, too much Newton-Raphson for me!'
    print *, e, f
    stop
  end if

  !calculate the true anomaly
  !Relation between true anomaly(ta) and eccentric anomaly(ea) is
  !tan(ta) = sqrt(1-e^2) sin (ea) / ( cos(ea) - e ) https://en.wikipedia.org/wiki/True_anomaly
  !In a complex plane, this is =  (cos(ea) - e) + i (sqrt(1-e^2) *sin(ea) )
  !with modulus = 1 - e cos(ea)
  eimag = ( sqrt(uno-e*e) * sin(ta) ) !/ (uno-e*cos(ta))
  ereal = ( cos (ta) - e ) !/ (uno-e*cos(ta))
  !Therefore, the tue anomaly is
  ta = atan2(eimag,ereal)

end subroutine
