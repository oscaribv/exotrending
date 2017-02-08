# CHI-DETENDRING #
#### Written by Oscar Barragán
##### email: oscaribv@gmail.com
##### Updated Feb 07, 2017

## __Introduction__

## ** Dependencies **

You need to install in your computer:
* gfortran
* numpy
* matplotlib
* scipy
* seaborn (optional)

## Use it now!

You do not need install anything, just clone or download pyaneti.

```
git clone https://github.com/oscaribv/chidetrending
```

The advantage about cloning the repository is the possibility to follow the changes to this package easily with git pull (learn more about git
in [https://git-scm.com/](https://git-scm.com/)).
Or if you want

```
wget https://github.com/oscaribv/chidetrending/archive/master.zip
unzip master.zip
mv chidetrending_master chidetrending
```

if you choose this option, you should repeat it every time the code is updated.

Now we have to compile the file with the transit routines (we need to do this
 only one time!)

```
cd chidetrending/src
make
```
If there were no errors, then you are ready to run the test case!

First return to the parent directory
```
cd ..
```
The test case comes from [Barragán et al. (2017)](https://arxiv.org/abs/1702.00691).
A warm Jupiter with 3 transits. We downladed the light curve and we called it
"warm_jupiter.dat". From a transit detection algorith me have the ephemeris
P = 28.38229 and epoch of first transit T0 = 2492.81705. We estimated
roughly that the transit duration is 5 hours and we want 10 hours of out-of-transit
data to do the detrending.

We put this information in the input.py file (already in)

```python2.7
#Input file

#the name of the file with the light curve data
lc_file='warm_jupiter.dat'

#Flag to indicate if we want a plot with the seaborn library
#is_seaborn = True

#Ephemeris
#Period
P = 28.38229
#Epoch of first transit
T0 = 2492.81705
#Transit duration in days
ttran = 5.0/24.0
#out of transit duration in days
toutt = 10./24.0
```

We are ready to run the program

```
python detrending_chido.py
```
You will see

![Whole light curve](images/f1.png)

which is the whole light-curve, where the transit positions
 are marked with vertical dashed lines. Then

![Detected transits](images/f2.png)

Which are the found transits (3 in this case). The next image is

![Detrended transits](images/f3.png)

Which are all the DETRENDEND transits. The next image is the
phase-folded data to the first transit.

![Folded transits](images/f4.png)

The next step is to fit a Mandel & Agol (2002) light curve_fit

![Fit to data](images/f5.png)

And perform the sigma clipping

![removed data points](images/f6.png)

Where the red points are the removed ones. The output of the code are
the pdf file of the light_curve.pdf and the warm_jupiter_detrended.dat file,
which contains the detrendend light curve, where the first column is the time,
the second the flux and the third one the error bars.

