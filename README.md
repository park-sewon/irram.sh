# irram.sh
irramsh is a version and package manager + compiling helper for [iRRAM](http://irram.uni-trier.de), which
is an open source C++ library for real number computation (Exact Real Arithmetic). 
It will make iRRAM developer's life easier. 

### (1) Compile helper
Suppose you have an iRRAM source code to compile:


***pi.cc***
```C
#include iRRAM.h
void compute()
{
    REAL x = pi(); 
    cout << setRwidth(100);
    cout << x
}
```

Then, this can be compiled simply by 

```console
$ irramsh -o compute_pi pi.cc

```

### (2) Version Controller
Suppose you need to use different versions of iRRAM for some reason.
Let us suppose that you need (i) 2011_02 version of iRRAM and 
also (ii) 2017_01 version of iRRAM. Once you install both of them
locally, (when you run Quickinstall of iRRAM it asks whether 
you want ot install locally), you can add the different version of iRRAM
by simply doing

```console
$ irramsh -v

Using version 1 installed in /path/installed
$ irramsh add
Locate iRRAM installation directory:
write/path/to/new/installed

$ irramsh --all
Version 1 @ /path/to/old/irram/installed
Version 2 @ /path/to/new/irram/installed

$ irramsh switch 2
$ irramsh -v
Using version 2 installed in /new/path/installed
```


Of course, you can switch it back by simply typing
```console
$ irramsh switch 1
$ irramsh -v
Using version 1 installed in /path/installed
```

### (3) Package Manager

You can see current status of irramsh package

1. [irram-random](https://github.com/park-sewon/iRRAM-Random) by sewon park

1. _irram-poly_ by Charlse (to be uploaded)

You can see what packages are available by

```console
$ irramsh show
irram-random
irram-poly (tba)
irram-linear-algebra (tba)

$ irramsh install irram-random
...
installation complete
$ irram list
irram-random
```

Installed packages can be used easily. For the packages' 
functionality, visit their websites. However, using and compiling
the packages can be done by follow. 
Assume that you have a iRRAM source code using the installed package:

random.cc
```C
#include iRRAM.h
#include "irram-random.h"
void compute()
{
    REALMATRIX M = gaussian_matrix(10);
    cout << M(0,0);
}
```

It can be done simply by

```console
$ irramsh -o randmatrix random.cc
```

You can also remove or deactivate the installed packages. 

## How to use?
1) You need (1) python2.7 and (2) locally installed iRRAM.
To install iRRAM, visit http://irram.uni-trier.de

1) clone or download the repository.

1) add the downloaded directory to the PATH.

1) Have fun with irramsh!
