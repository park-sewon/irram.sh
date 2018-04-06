#!/usr/bin/python

"""
Main file for irramsh.
irramsh is a version and package manager for iRRAM.
Maintainer or person who modify the file to adjust the file to their environment
should be aware of that the program has access to a file system.
This version is a work in progress-prototype version; the project is created mainly to make
the author's life of programming on iRRAM easier; and distributed in hope of making others' easier as well;
there is no warranty of any result of this program; If any problem occurs during using this program,
it is the user's fault not inspecting the file thoroughly.
"""

import sys, getopt, subprocess, os, readline, glob

__author__ = "sewon park"
__copyright__ = "Copyright 2018, sewon park"
__license__ = "MIT License"
__status__ = "Prototype, work in progress"

path = os.path.dirname(os.path.abspath(__file__))


def exodus(msg):
    print msg + '  See "irramsh -h|--help" for further information.'
    sys.exit(1)


def usage():
    s = 'iRRAM version and package manager.\n' \
        '(1) You can control many versions of iRRAM; e.g., when you need to use' \
        'a formal released version and indevelopment version at once.\n' \
        '(2) You can easily compile an iRRAM source code; e.g., if you have hello.cc,' \
        'all you need to do is  "irramsh -o myirram hello.cc\n' \
        '(3) You can download and use various iRRAM packages easily; e.g., if you want to use' \
        'a random number generator, all you need to do is "irramsh install irram-random" and add'\
        '#include "irram-random.h" to your source code!\n\n'\
        'irramsh has following options::\n' \
        '-h|--help shows this message\n' \
        '-v|--version shows which version of iRRAM is being used to compile\n' \
        '-a|--all shows all versions of iRRAM that is registered to this irramsh\n'\
        '-o|--output selects the output file name. it is a.out in default\n' \
        '-f|--force forces compile when there already exists the output file.\n\n'\
        'and following usages:\n'\
        '"init" initializes the irramsh.\n' \
        '"-o <filename.cc> helloworld" creates an irram template <filename.cc>\n'\
        '"add" adds another iRRAM version to the irramsh\n'\
        '"switch <n>" switchs the iRRAM compiler to the version <n>. Try "irramsh -a" to see what versions you have\n'\
        '"select <n>" names the registered version <n> to be the 201401 official release of iRRAM\n'\
        '"deselect" de-select the selected official release version of iRRAM\n'\
        '"clear" clears the saved configuration. Use it when the irramsh got too messy\n\n' \
        'package managing:\n'\
        '"show" shows available packages in irramsh package repo\n'\
        '"list" shows installed packages in irramsh\n'\
        '"install <package>" downloads and installs the package <package>\n' \
        '"uninstall <package>" removes the installed package <package>\n' \
        '"activate <package>" activates a decativated package\n' \
        '"deactivate <package>" deactivates the installed package named <package>\n'

    print(s)
    sys.exit(0)


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


hw = '#include "iRRAM/lib.h"\n#include "iRRAM/core.h"\n#include "iRRAM.h"\nusing namespace iRRAM;\nvoid compute()\n{\ncout<<"halo world";\n}'
CONFIGFILE = path+"/config"
PKGCONFIGFILE = path+"/packages/pkgconfig"
TESTFILE = path+"/test.cc"
PKGPATH = path+"/packages"

def message(iRRAMPath, INPUT, LIB, LIBPATH, OUTPUT):

    return "g++ -std=c++11 -g -O2 -I" + iRRAMPath + "/include " + LIBPATH + " -Xlinker -rpath -Xlinker "+iRRAMPath+"/lib "\
           + str(INPUT)  +" " +LIB+ " -L" + iRRAMPath+"/lib -liRRAM -lmpfr -lgmp  -lm -o " + OUTPUT


'''
CONFIGURATION OF IRRAMSH
'''
def load_config():
    try:
        version = 0
        locationlst = []
        location = ""
        with open(CONFIGFILE, 'r') as f:
            content = f.readlines()
        configs = [x.strip() for x in content]
        for c in configs:
            if "VERSION=" in c:
                version = int(c.split("=")[1])
            elif "V=" in c:
                locationlst.append(c.split("V="))
                if int(c.split("V=")[0]) == version:
                    location = c.split("V=")[1]

        if location == []:
            raise ValueError('Configuration File Defective')

        return locationlst, location, version


    except:
        raise ValueError('Configuration File Defective')


def add_irram():

    test = open(TESTFILE, 'w')
    test.write('')
    test.write(hw)
    test.close()

    verif = False
    counter = 3
    while (not verif) and counter >= 0:

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)

        location = raw_input("Locate iRRAM installation directory: /path/to/iRRAM/installed \n")
        while location[-1] == '/':
            location = location[:-1]

        try:
            subprocess.check_call(message(location, path+"/test.cc", "", "", "a.out"), shell=True)
            verif = True

        except:
            print 'Could not compile a test file with the selected version of iRRAM.'
            counter -= 1

    if not verif:
        exodus('The selected version of iRRAM does not work. Check whether the installed iRRAM is properly installed "locally"')

    num = -1
    with open(CONFIGFILE, 'r') as f:
        config = f.readlines()

    newconf = ""
    for l in config:
        if "NUM=" in l:
            num = int(l.split("=")[1])
            l = ("NUM="+str(num+1)+"\n")
        newconf += (l)
    newconf += (str(num+1)+"V="+location+"\n")
    print newconf
    with open(CONFIGFILE, 'w') as f:
        f.write(newconf)




def select_official(v):
    '''
    select among registered versions of iRRAM, the official release
    '''
    v = v.strip()
    try:
        exists = False
        with open(CONFIGFILE, 'r') as f:
            config = f.readlines()
        q = []
        for l in config:
            if "VERSION=" in l:
                if int(l.split("=")[1]) == int(v):
                    q.append("VERSION=0")
                else:
                    q.append(l)
            elif "0V=" in l:
                exodus('Official release is already selected. "deselect" the official release first')
            elif v+"V"+"=" in l:
                q.append("0V="+l.split("=")[1])
                exists = True
            else:
                q.append(l)
        if not exists:
            exodus('Selected version ' + v + " does not exist")
        with open(CONFIGFILE, 'w') as f:
            f.writelines(q)
    except Exception as err:
        exodus('Could not change version')

def deselct_official():
    try:
        with open(CONFIGFILE, 'r') as f:
            config = f.readlines()
        q = []
        num = 0
        for l in config:
            if "NUM=" in l:
                num = int(l.split("=")[1])
            elif "V0=" in l:
                l = "v"+str(num+1)+"="+l.split("=")[1]

            q.append(l)

        with open(CONFIGFILE, 'r') as f:
            f.writelines(q)
    except:
        exodus('Could not change version')


def switch(v):
    with open(CONFIGFILE, 'r') as f:
        config = f.readlines()
    newconf = ""
    ex = True
    for l in config:
        if "VERSION=" in l:
            l = ("VERSION="+str(v)+"\n")
        newconf+= (l)
        if "V=" in l:
            if v == int(l.split("V=")[0]):
                ex = False
    if ex:
        raise ValueError('Selected Switching Version Does not Exist')

    with open(CONFIGFILE, 'w') as f:
        f.write(newconf)


def clear():
    config = open(CONFIGFILE, 'w')
    config.close()


'''
PACKAGE MANAGEMENT
'''


def load_package_index():
    import urllib2
    response = urllib2.urlopen('https://complexity.kaist.ac.kr/_media/irramsh/irramsh-package-index.odt')
    html = response.readlines()
    return [x.strip().split(",".strip()) for x in html]


def uninstall_package(pkgname):

    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            return
    exodus('Package name ' + pkgname + ' is not installed')


def install_package(pkgname):

    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            exodus('Pakage name ' + pkgname + ' is already installed')


    pkgs = load_package_index()
    for p in pkgs:
        if pkgname == p[0]:
            try:
                subprocess.check_call('wget -P '+ path + '/packages ' + p[1], shell=True)
                if not os.path.exists(path + '/packages/'+p[0]):
                    os.makedirs(path + '/packages/'+p[0])
                uz = 'unzip ' + path+'/packages/'+p[0]+'.zip ' + '-d ' + path+'/packages/'+p[0]
                subprocess.check_call(uz, shell= True)

                with open(PKGCONFIGFILE, 'a') as f:
                    f.write(p[0] + ", 1\n")

            except:
                exodus('Installing ' + pkgname + ' failed')
            return
    exodus('Package name ' + pkgname +' does not exists.')


def deactivate_package(pkgname):
    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            if int(p[1]) == 0:
                p[1] = 1
    with open(PKGCONFIGFILE, 'w') as f:
        for p in installed:
            f.writelines(p)

def activate_package(pkgname):
    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            if int(p[1]) == 0:
                p[1] = 1
    with open(PKGCONFIGFILE, 'w') as f:
        for p in installed:
            f.writelines(p)


def load_package_config():
    with open(PKGCONFIGFILE, 'r') as f:
        pkgs = f.readlines()
    pkgs = [x.strip().split(",".strip()) for x in pkgs]
    return pkgs


def load_package_paths(version):
    pkgs = load_package_config()
    libpath = " "
    s = " "
    for p in pkgs:
        libpath += "-I "+path+"/packages/"+p[0]+" "
        if int(version) == 0:
            pt = path+"/packages/"+p[0] +"/irramsh_official"
        else:
            pt = path+"/packages/"+p[0] +"/irramsh"

        with open(pt, 'r') as f:
            srcs = f.readlines()
            for l in srcs:
                s+=path+"/packages/"+p[0]+"/"+(l.strip())+" "
    return s, libpath




'''
Initializer: creates
1. config
2. packages/pkgconfig
'''
import os
def initialize():
    newconfig = False
    if not os.path.exists(PKGPATH):
        os.makedirs(PKGPATH)
    if not os.path.exists(PKGCONFIGFILE):
        f = open(PKGCONFIGFILE, 'w')
        f.close()
    if not os.path.exists(CONFIGFILE):
        config = open(CONFIGFILE, 'w')
        config.write('NUM=0\nVERSION=0\n')
        config.close()
        newconfig = True
    if newconfig == True:
        try:
            add_irram()
            switch(1)
        except:
            exodus("cannot create a configuration file")



'''
MAIN CONTROL
'''


def main(argv):
    if len(argv) == 0:
        exodus("arguments are expected")
    try:
        locationlst, location, version = load_config()
    except:
        exodus('Configuration could not be loaded. Try "irramsh init" before running this.')

    INPUT = ''
    OUTPUT = 'a.out'
    FORCE = False

    '''
    Parsing option arguments
    '''
    try:
        opts, args = getopt.getopt(argv,"afhvo:",["all","version","help","output="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    for opt, arg in opts:
        print arg
        if opt in ('-h', "--help"):
            usage()

        elif opt in ("-a", "--all"):
            for l in locationlst:
                if int(l[0]) == 0:
                    print "version " + l[0] + " @ " + l[1] +" (official release) "
                else:
                    print "version " + l[0] + " @ " + l[1]
            sys.exit()

        elif opt in ("-v", "--version"):
            if version == 0:
                print "Using (official release) version "+ str(version) +" installed in " + location
            else:
                print "Using version "+ str(version) +" installed in " + location

            sys.exit()

        elif opt in ("-f", "--force"):
            FORCE = True

        elif opt in ("-o", "--output"):
            OUTPUT = arg


    '''
    parsing non-option arguments
    '''
    mainarg = args[0]

    if mainarg == "init":
        initialize()
        sys.exit()

    if mainarg == "helloworld":
        with open(OUTPUT, 'w') as f:
            f.write(hw)
        sys.exit()

    elif mainarg == "clear":
        clear()
        sys.exit()

    elif mainarg == "switch":
        try:
            v = int(args[1])
            switch(v)
        except:
            exodus('Could not change the version')
        sys.exit()

    elif mainarg == "change":
        sys.exit()

    elif mainarg == "add":
        add_irram()
        sys.exit()

    elif mainarg == "install":
        install_package(args[1])
        sys.exit()

    elif mainarg == "uninstall":
        uninstall_package(args[1])
        sys.exit()

    elif mainarg == "deactivate":
        deactivate_package(args[1])
        sys.exit()

    elif mainarg == "activate":
        activate_package(args[1])
        sys.exit()

    elif mainarg == "list":
        q = load_package_config()
        for d in q:
            print d[0]

        sys.exit()

    elif mainarg == "show":
        q = load_package_config()
        for p in load_package_index():
            exists = False
            for d in q:
                if p[0] == d[0]:
                    print p[0] + " [installed]"
                    exists = True
                    continue
            if not exists:
                print p[0]
        sys.exit()

    elif mainarg == "select":
        select_official(args[1])
        sys.exit()

    elif mainarg == "deselect":
        deselct_official()
        sys.exit()


    '''
    Compile is by default. 
    Check whether there already exists the output file.
    If it does, abort except it is forced.
    '''
    if os.path.exists(path+'/'+OUTPUT):
        if not FORCE:
            exodus('File ' + OUTPUT + ' already exists')
    for f in args:
        INPUT += f + " "
    s, l = load_package_paths(version)


    '''
    Compile the iRRAM file.. 
    '''
    try:
        subprocess.check_call(message(location, INPUT, s, l, OUTPUT), shell=True)
    except subprocess.CalledProcessError as err:
        # print err.output
        exodus('\n[irramsh] compile failed')

if __name__ == "__main__":

    main(sys.argv[1:])
