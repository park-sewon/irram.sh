#!/usr/bin/python

import sys, getopt, subprocess, errno, os
import readline, glob
path = os.path.dirname(os.path.abspath(__file__))


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


hw = '#include "iRRAM/lib.h"\n#include "iRRAM/core.h"\n#include "iRRAM.h"\nusing namespace iRRAM;\nvoid compute()\n{\ncout<<"halo world";\n}'
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
        with open(path+'/config', 'r') as f:
            content = f.readlines()
        configs = [x.strip() for x in content]
        for c in configs:
            if "VERSION=" in c:
                version = int(c.split("=")[1])
            elif "V=" in c:
                locationlst.append(c.split("V="))
                if int(c.split("V=")[0]) == version:
                    location = c.split("V=")[1]
            elif "cleared" in c:
                version = 0
                locationlst = []

        if version == 0 or location == []:
            raise ValueError('Configuration File Defective')

        return locationlst, location, version


    except:
        raise ValueError('Configuration File Defective')


def add_irram():

    test = open(path+'/test.cc', 'w')
    test.write('')
    test.write(hw)
    test.close()

    verif = True
    while verif:

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)

        location = raw_input("Locate iRRAM installation directory:\n")

        try:
            subprocess.check_call(message(location, path+"/test.cc", "", "", "a.out"), shell=True)
            verif = False

        except:
            print "Couldn't compile a test file. Try again!"
            sys.exit()


    num = -1
    with open(path+'/config', 'r') as f:
        config = f.readlines()

    newconf = ""
    for l in config:
        if "NUM=" in l:
            num = int(l.split("=")[1])
            l = ("NUM="+str(num+1)+"\n")
        newconf += (l)
    newconf += (str(num+1)+"V="+location+"\n")
    print newconf
    with open(path+'/config', 'w') as f:
        f.write(newconf)


def switch(v):
    with open(path+'/config', 'r') as f:
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

    with open(path+'/config', 'w') as f:
        f.write(newconf)


def clear():
    config = open(path+'/config', 'w')
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

    pass

def install_package(pkgname):

    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            raise ValueError('Pakage name ' + pkgname + ' is already installed')


    pkgs = load_package_index()
    for p in pkgs:
        if pkgname == p[0]:
            try:
                subprocess.check_call('wget -P '+ path + '/packages ' + p[1], shell=True)
                if not os.path.exists(path + '/packages/'+p[0]):
                    os.makedirs(path + '/packages/'+p[0])
                uz = 'unzip ' + path+'/packages/'+p[0]+'.zip ' + '-d ' + path+'/packages/'+p[0]
                subprocess.check_call(uz, shell= True)
                with open(path + '/packages/pkgconfig', 'a') as f:
                    f.write(p[0] + ", 1\n")
            except:
                raise
            return
    raise ValueError('Package name ' + pkgname +' does not exists.')


def deactivate_package(pkgname):
    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            if int(p[1]) == 0:
                p[1] = 1
    with open(path+'/packages/pkgconfig', 'w') as f:
        for p in installed:
            f.writelines(p)

def activate_package(pkgname):
    installed = load_package_config()
    for p in installed:
        if pkgname == p[0]:
            if int(p[1]) == 0:
                p[1] = 1
    with open(path+'/packages/pkgconfig', 'w') as f:
        for p in installed:
            f.writelines(p)


def load_package_config():
    with open(path+'/packages/pkgconfig', 'r') as f:
        pkgs = f.readlines()
    pkgs = [x.strip().split(",".strip()) for x in pkgs]
    return pkgs


def load_package_paths():
    pkgs = load_package_config()
    libpath = " "
    s = " "
    for p in pkgs:
        libpath += "-I "+path+"/packages/"+p[0]+" "
        with open(path+"/packages/"+p[0] +"/irramsh", 'r') as f:
            srcs = f.readlines()
            for l in srcs:
                s+=path+"/packages/"+p[0]+"/"+(l.strip())+" "
    return s, libpath



import os
def initialize():
    newconfig = False
    if not os.path.exists(path+'/packages'):
        os.makedirs(path+'/packages')
    if not os.path.exists(path+'/packages/pkgconfig'):
        f = open(path+'/packages/pkgconfig', 'w')
        f.close()
    if not os.path.exists(path+'/config'):
        config = open(path+'/config', 'w')
        config.write('NUM=0\nVERSION=0\n')
        config.close()
        newconfig = True
    if newconfig == True:
        try:
            add_irram()
            switch(1)
        except:
            print "cannot create a configuration file"
            sys.exit()



'''
MAIN CONTROL
'''
def main(argv):

    if len(argv) == 1:
        print "arguments are expected"
        sys.exit()
    loaded = False
    while not loaded:
        try:
            locationlst, location, version = load_config()
            loaded = True

        except ValueError as err:
            print(err)
            if 'Configuration File Not Found' in err or 'Configuration File Defective' in err:
                initialize()

        except Exception as e:
            print(e)
            sys.exit()

    INPUT = ''
    OUTPUT = 'a.out'
    FORCE = False

    # Parsing option arguments
    try:
        opts, args = getopt.getopt(argv,"afhvo:",["all","version","help","output="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    for opt, arg in opts:
        print arg
        if opt in ('-h', "--help"):
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()

        elif opt in ("-a", "--all"):
            for l in locationlst:
                print "version " + l[0] + " @ " + l[1]
            sys.exit()

        elif opt in ("-v", "--version"):
            print "Using version "+ str(version) +" installed in " + location
            sys.exit()

        elif opt in ("-f", "--force"):
            Force = True

        elif opt in ("-o", "--output"):
            OUTPUT = arg


    # Parsing non-option arguments
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
            raise
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
        for p in  load_package_index():
            print p[0]
        sys.exit()

    if os.path.exists(path+'/'+OUTPUT):
        if not FORCE:
            raise ValueError('File ' + OUTPUT + ' already exists')
    # Compiling irram in default
    for f in args:
        INPUT += f + " "
    s, l = load_package_paths()

    subprocess.check_call(message(location, INPUT, s, l, OUTPUT), shell=True)

if __name__ == "__main__":

    main(sys.argv[1:])
