#EXOTRENDRING
#### Written by Barragán O. and Gandolfi D.
##### email: oscar.barraganvil@edu.unito.it
##### Updated Feb 14, 2017

## Introduction

* This software suite is a small compilation to detrended exoplanet transit light curves.

* It is very simple and it can be used straightforward.

* If you have a light curve (time and flux) and some good epeheris, this code can help you!

* I have only tested it with Kepler light curves, but it should work for any file with a time and flux column.


## Dependencies

You need to have installed:
* gfortran
* numpy
* matplotlib
* scipy
* seaborn (optional)

## Use it now!

You do not need install anything, just clone or download the repository.

```
git clone https://github.com/oscaribv/exotrending
```

The advantage about cloning the repository is the possibility to follow the changes to this package easily with git pull (learn more about git
in [https://git-scm.com/](https://git-scm.com/)).
Or if you want

```
wget https://github.com/oscaribv/exotrending/archive/master.zip
unzip master.zip
mv exotrending_master exotrending
```

if you choose this option, you should repeat it every time the code is updated.

Now we have to compile the file with the transit routines (we need to do this
 only one time!)

```
cd exotrending/src
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
P = 28.38229 days and epoch of first transit T0 = 2492.81705 (BJD - 2454833.0) days. We estimated
roughly that the transit duration is 5 hours and we want 10 hours of out-of-transit
data to do the detrending.

We put this information in the input.py file (already in)

```Python
#Input file

#the name of the file with the light curve data
lc_file='warm_jupiter.dat'

#Flag to indicate if we want a plot with the seaborn library
#Uncoment next line to have similar plots to the ones in this tutorial
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
python exotrending.py
```
You will see

` This is the whole light curve `

![Whole light curve](images/f1.png)

which is the whole light-curve, where the transit positions
 are marked with vertical dashed lines. Then

` Individual detected transits `

![Detected transits](images/f2.png)

`I found 3 transits`

Which are the found transits (3 in this case). The next image is

```
Individual detected transits
FITTING POLINOMIAL ORDER =  2
METHOD = SUBSTRACTION
detrended transits
```

![Detrended transits](images/f3.png)

Which are all the DETRENDEND transits. The next image is the
phase-folded data to the first transit.

` folded transits `

![Folded transits](images/f4.png)

The next step is to fit a Mandel & Agol (2002) light curve_fit

```
STARTING SIGMA-CLIPPING
with =  3.0 -sigma
I AM FITTING THE PARAMETERS
```

![Fit to data](images/f5.png)

And perform the sigma clipping

```
SIGMA-CLIPPING ENDED
BLUE POINTS -> remaining data
RED POINTS  -> removed data
```

![removed data points](images/f6.png)

```
CREATING OUTPUT FILE =  warm_jupiter_detrended.dat
```

Where the red points are the removed ones (I know, this is not a good
example to show that the sigma-clipping works, but I will
put some good example soon).

 The output of the code are
the pdf file of the light_curve.pdf and the warm_jupiter_detrended.dat file,
which contains the detrendend light curve, where the first column is the time,
the second the flux and the third one the error bars.

## Documentation

This last example is a simple case. There are more option in the code
that can be modified in the input.py file. A manual is not
available now, but a description of the parameters that you can
change are inside the `src/default.py` file.

## Software in development

This software is in contruction, it may contain bugs.

** If you have doubts or suggestions do not hesitate to contact me.
email: oscar.barraganvil@edu.unito.it **

## Acknowledgements
* I thank to Lauren Flor Torres, Sebastian Morales, Fernando Romero and Mabel Valerdi
for help me as test users.
