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

### (4) irramsh_make
Suppose you have a project _myproject_ where you need to compile many iRRAM files:
_src1/a.cc_ _src1/b.cc_ _src2/c.cc_ _src3/d.cc_ with _*irramsh version 4*_ using irramsh
packages _irram-pkg1_ and _irram-pkg2_ into an output file _out.out_.
So, this is a big project which has its one compilation configuration. 

When you have other projects working on simultaneously,
in such case, you do not want to switch the irram configuration
everytime to compile this; you do not want to activate/deactivate packages and
switch version all the time. 
Moreover, typing all the source files every time is clerical. 

Using irramsh_make, you can store the project's own configuration
and compile it without changing any configuration of irramsh!

In the case, write the project's configuration into

_*irramsh_make*_:
```text
- makefile for the project myproject
- The project uses irram version 3
- comment out with leading symbol '-'
* version
    + 4
* packages
    + irram-pkg1
    - irram-random
    + irram-pkg2
* sources
    + src1/a.cc
    + src1/b.cc
    - src1/a_tmp.cc
    + src2/c.cc
    + src3/d.cc
* output
    + out.out
    - test.out
* force
    - force forces overwrite when 'out.out' already exists.
    - is turned off by default
```

```console
$ irramsh make
[irramsh] compile finished
```

## Using tips

iRRAM projects that are based on in-development version 
may have some compatibility issues. Unless there is some
inevitable reason for using only 
the in-development version, packages distributed through irramsh 
should offer to be compatible with the official version of iRRAM.
However, this can be done only if the irramsh knows whether your
iRRAM version is official or not. 

When you first download the irramsh, you need to initialize it first 
(It asks for the initialization anyway). When you try to initialize 
or to add another version of 
iRRAM, after you locate the iRRAM installed directory, it asks you whether
the located version is the official release version of iRRAM:

```console
$ irramsh init
Locate iRRAM installation directory: /path/to/iRRAM/installed:
> /path/to/irram/installed
Is this the official release of iRRAM? (201401 by Norbert Mueller) [y/n]:
> Y
$ irramsh -a
version 1 @ /path2/installed Release date: 201701
version 2 @ /path1/installed Release date: 201402 (official release)
```
Even if you did not specified when you added, you can later specify 
the official release version among the registered versions:
```console
$ irramsh -a
version 1 @ /path2/installed Release date: 201701
version 2 @ /path1/installed Release date: 201402
$ irramsh select 2
$ irramsh -a
version 1 @ /path2/installed Release date: 201701
version 2 @ /path1/installed Release date: 201402 (official release)
```

## Installation
1) You need (1) python2.7 and (2) locally installed iRRAM.
To install iRRAM, visit http://irram.uni-trier.de

1) clone or download the repository.

1) add the downloaded directory to the PATH.

1) Have fun with irramsh!
