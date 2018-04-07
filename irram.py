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



def exodus(msg):
    print msg + '\nSee "irramsh -h|--help" for further information.'
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
    return (glob.glob(text+'*'+"/")+[None])[state]

'''
Constants storing abs paths to configuration files and package directories
'''
PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGFILE = PATH+"/config"
PKGCONFIGFILE = PATH+"/packages/pkgconfig"
TESTFILE = PATH+"/test.cc"
PKGPATH = PATH+"/packages"
TEMPLATE =  '#include "iRRAM/lib.h"\n'\
            '#include "iRRAM/core.h"\n'\
            '#include "iRRAM.h"\n'\
            'using namespace iRRAM;\n'\
            'void compute()\n'\
            '{\n'\
            '\tcout<<"halo world";\n}'

'''
Global variables storing user configurations of irramsh
(UID, release date, dir, T/F denoting official release, T/F chosen)
'''
class CONFIGURATION:
    LOADED = False
    VERSION = -1
    VERSIONS = []
    COMPILER = []
    LENGTH = 5
    LIST = []
    INSTALLED = []
    ACTIVATED = []
    def __init__(self):
        pass
    def next_id(self):
        i = 0
        for v in self.VERSIONS:
            if i > int(v[0]):
                pass
            else:
                i = int(v[0])
        return i + 1

CONF = CONFIGURATION()

'''
Template of a iRRAM source code
'''



def message(irram, inputfiles, lib, libpath, output):
    return "g++ -std=c++11 -g -O2 -I" + irram + "/include " + libpath + " -Xlinker -rpath -Xlinker "+irram+"/lib "\
           + str(inputfiles) + " " + lib + " -L" + irram+"/lib -liRRAM -lmpfr -lgmp  -lm -o " + output



def load_config():
    '''
    Load config file
    :return: None
    '''
    global CONF

    try:

        with open(CONFIGFILE, 'r') as f:
            content = f.readlines()
        configs = [x.strip().split(",") for x in content]
        for l in configs:
            if len(l) != 5:
                exodus('Configuration file is damaged. irramsh clear to reset the damaged configuration file')

        for c in configs:
            CONF.VERSIONS.append([int(c[0]), c[1], c[2], int(c[3]), int(c[4])])
            if int(c[4]) == 1:
                if CONF.VERSION != -1:
                    exodus('More than one iRRAM are chosen to be a default compiler.')

                CONF.VERSION = int(c[0])
                CONF.COMPILER = [int(c[0]), c[1], c[2], int(c[3]), int(c[4])]

        if len(CONF.VERSIONS) == 0:
            exodus('Configuration is empty. irramsh init first to use.')
        if CONF.VERSION == -1:
            exodus('Default iRRAM is not chosen.')
        CONF.LOADED = True

    except:
        raise ValueError('Configuration File Defective')


def dump_config():
    '''
    store Config into the config file
    :return: None
    '''
    l = []
    for v in CONF.VERSIONS:
        l.append(str(v[0]) + ","+str(v[1]) + ","+str(v[2]) + ","+str(v[3]) + ","+str(v[4]))
    with open(CONFIGFILE, 'w') as f:
        f.writelines("%s\n" % j for j in l)


def add_irram():
    '''
    add irram compiler
    :return: None
    '''
    global CONF
    test = open(TESTFILE, 'w')
    test.write('')
    test.write(TEMPLATE)
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
            subprocess.check_call(message(location, PATH+"/test.cc", "", "", "a.out"), shell=True)
            verif = True

        except:
            print 'Could not compile a test file with the selected version of iRRAM.'
            counter -= 1

    if not verif:
        exodus('The selected version of iRRAM does not work. '
               'Check whether the installed iRRAM is properly installed "locally"')


    official = 1
    while official not in ['Y', 'N', 'y', 'n']:
        official = raw_input("Is this the official release of iRRAM? (201401 by Norbert Mueller) [y/n]:")
    if official in ['Y', 'y']:
        official = 1
        version = '201702'
    else:
        official = 0
        version = raw_input("[optional, 000000 by default] Set version's release year-month (e.g., 201701): \n")
        if len(version) == 6:
            try:
                k = int(version)
            except:
                version = '000000'
        else:
            version = '000000'
    if len(CONF.VERSIONS) == 0:
        CONF.VERSIONS.append([CONF.next_id(), version, location, str(official), 1])
    else:
        CONF.VERSIONS.append([CONF.next_id(), version, location, str(official), 0])

    dump_config()


def select_official(v):
    '''
    assign official release for the chosen version v
    :param v: int
    :return: None
    '''
    global CONF
    exists = False
    for i in range(len(CONF.VERSIONS)):
        if int(CONF.VERSIONS[i][0]) == v:
            CONF.VERSIONS[i][3] = 1
            exists = True
    if not exists:
        exodus('Selected version ' + v + " does not exist")
    dump_config()

def deselct_official(v):
    '''
    deselct official release for the chosen version v
    :param v: int
    :return: None
    '''
    global CONF
    exists = False
    for i in range(len(CONF.VERSIONS)):
        if int(CONF.VERSIONS[i][0]) == int(v):
            CONF.VERSIONS[i][3] = 0
            exists = True
    if not exists:
        exodus('Selected version ' + v + " does not exist")
    dump_config()

def switch(v):
    '''
    Switch the current default compiler to the verion v
    :param v: int
    :return: None
    '''

    global CONF
    exists = False
    for i in range(len(CONF.VERSIONS)):
        if int(CONF.VERSIONS[i][4]) == 1:
            CONF.VERSIONS[i][4] = 0
        if int(CONF.VERSIONS[i][0]) == v:
            CONF.VERSIONS[i][4] = 1
            exists = True
    if not exists:
        exodus('Selected version ' + v + " does not exist")
    dump_config()


def clear():
    '''
    delete all content of config file
    :return: None
    '''
    config = open(CONFIGFILE, 'w')
    config.close()



'''
PACKAGE MANAGEMENT
'''


def load_package_config():
    global CONF
    with open(PKGCONFIGFILE, 'r') as f:
        pkgs = f.readlines()
    pkgs = [x.strip().split(",".strip()) for x in pkgs]
    for pkg in pkgs:
        if int(pkg[1]) == 1:
            CONF.ACTIVATED.append([pkg[0], int(pkg[1])])
        CONF.INSTALLED.append([pkg[0], int(pkg[1])])


def dump_package_config():
    global CONF
    l = []
    for c in CONF.INSTALLED:
        l.append(str(c[0])+","+str(c[1]))
    with open(PKGCONFIGFILE, 'w') as f:
        f.writelines("%s\n" % j for j in l)

def update_package_index():
    pass


def load_package_index():
    global CONF
    import urllib2
    response = urllib2.urlopen('https://complexity.kaist.ac.kr/_media/irramsh/irramsh-package-index.odt')
    html = response.readlines()
    CONF.LIST = [x.strip().split(",".strip()) for x in html]
    return [x.strip().split(",".strip()) for x in html]


def uninstall_package(pkgname):

    installed = CONF.INSTALLED
    for p in installed:
        if pkgname == p[0]:
            return
    exodus('Package name ' + pkgname + ' is not installed')


def install_package(pkgname):
    global CONF
    installed = CONF.INSTALLED
    for p in installed:
        if pkgname == p[0]:
            exodus('Pakage name ' + pkgname + ' is already installed')

    pkgs = load_package_index()
    for p in pkgs:
        if pkgname == p[0]:
            try:
                subprocess.check_call('wget -P '+ PATH + '/packages ' + p[1], shell=True)
                if not os.path.exists(PATH + '/packages/'+p[0]):
                    os.makedirs(PATH + '/packages/'+p[0])
                uz = 'unzip ' + PATH+'/packages/'+p[0]+'.zip ' + '-d ' + PATH+'/packages/'+p[0]
                subprocess.check_call(uz, shell= True)
                CONF.INSTALLED.append([p[0], 1])
                dump_package_config()
            except:
                exodus('Installing ' + pkgname + ' failed')
            return
    exodus('Package name ' + pkgname +' does not exists.')


def deactivate_package(pkgname):
    '''
    :param pkgname: string
    :return: None.
    '''
    global CONF
    exists = False
    for i in range(len(CONF.INSTALLED)):
        if CONF.INSTALLED[i][0] == pkgname.strip():
            CONF.INSTALLED[i][1] = 0
            exists = True
    if not exists:
        exodus('Package ' + pkgname + " is not installed")
    dump_package_config()


def activate_package(pkgname):
    global CONF
    exists = False
    for i in range(len(CONF.INSTALLED)):
        if CONF.INSTALLED[i][0] == pkgname.strip():
            CONF.INSTALLED[i][1] = 1
            exists = True
    if not exists:
        exodus('Package ' + pkgname + " is not installed")
    dump_package_config()


def load_package_paths():
    pkgs = CONF.ACTIVATED
    libpath = " "
    s = " "
    for p in pkgs:
        libpath += "-I "+PATH+"/packages/"+p[0]+" "
        if int(CONF.COMPILER[3]) == 1:
            pt = PATH+"/packages/"+p[0] +"/irramsh_official"
        else:
            pt = PATH+"/packages/"+p[0] +"/irramsh"

        with open(pt, 'r') as f:
            srcs = f.readlines()
            for l in srcs:
                s += PATH+"/packages/"+p[0]+"/"+(l.strip())+" "
    return s, libpath




'''
Initializer: creates
1. config
2. packages/pkgconfig
'''
import os
def initialize():
    if not os.path.exists(PKGPATH):
        os.makedirs(PKGPATH)
    if not os.path.exists(PKGCONFIGFILE):
        f = open(PKGCONFIGFILE, 'w')
        f.close()
    if not os.path.exists(CONFIGFILE):
        config = open(CONFIGFILE, 'w')
        config.close()
    try:
        load_config()
    except:
        try:
            add_irram()
        except:
            exodus("cannot create a configuration file")



def require_additional_argument(s):
    exodus('The command ' + s+ ' require_additional_argument')

def check_number(v):
    '''
    check whether this is number
    :param v: string
    :return: int
    '''
    try:
        v = v.strip()
        v = int(v)
        return v
    except:
        raise


'''
MAIN CONTROL
'''


def main(argv):

    # if no argument is provided abort:
    if len(argv) == 0:
        exodus("arguments are expected")

    INPUT = ''
    OUTPUT = 'a.out'
    FORCE = False
    showall = False
    showversion = False

    try:
        opts, args = getopt.getopt(argv,"afhvo:",["all","version","help","output="])
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)


    if len(args) != 0:
        if args[0] == "init":
            initialize()
            sys.exit()
        if args[0] == "clear":
            clear()
            sys.exit()

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
        elif opt in ("-a", "--all"):
            showall = True
        elif opt in ("-v", "--version"):
            showversion = True
        elif opt in ("-f", "--force"):
            FORCE = True
        elif opt in ("-o", "--output"):
            OUTPUT = arg


    try:
        load_config()
        load_package_config()
    except Exception as e:
        exodus('Configuration could not be loaded. Try "irramsh clear/init" First.')


    if showall:
        for l in CONF.VERSIONS:
            if int(l[3]) == 1:
                print "version " + str(l[0]) + " @ " + l[2] + " Release date: " + l[1] + " (official release) "
            else:
                print "version " + str(l[0]) + " @ " + l[2] + " Release date: " + l[1]
        sys.exit()
    elif showversion:
        l = CONF.COMPILER
        if int(l[3]) == 1:
            print "Using version " + str(l[0]) + " @ " + l[2] + " Release date: " + l[1] + " (official release) "
        else:
            print "Using version " + str(l[0]) + " @ " + l[2] + " Release date: " + l[1]

        sys.exit()




    # Non option arguments:
    mainarg = args[0]
    numarg = len(args)


    # Version related:
    if mainarg == "helloworld":
        with open(OUTPUT, 'w') as f:
            f.write(TEMPLATE)
        sys.exit()

    elif mainarg == "clear":
        clear()
        sys.exit()

    elif mainarg == "switch":
        if numarg == 1:
            require_additional_argument('switch')
        try:
            v = check_number(args[1])
        except:
            exodus('argument has to be a number')

        switch(v)
        sys.exit()

    elif mainarg == "change":
        sys.exit()

    elif mainarg == "add":
        add_irram()
        sys.exit()

    elif mainarg == "select":
        if numarg == 1:
            require_additional_argument('select')
        try:
            v = check_number(args[1])
        except:
            exodus('argument has to be a number')

        select_official(v)
        sys.exit()

    elif mainarg == "deselect":
        if numarg == 1:
            require_additional_argument('deselect')
        try:
            v = check_number(args[1])
        except:
            exodus('argument has to be a number')

        deselct_official(v)
        sys.exit()

    # PACKAGE RELATED ARGUMENTS
    elif mainarg == "install":
        if numarg == 1:
            require_additional_argument('install')

        install_package(args[1])
        sys.exit()

    elif mainarg == "uninstall":
        if numarg == 1:
            require_additional_argument('uninstall')

        uninstall_package(args[1])
        sys.exit()

    elif mainarg == "deactivate":
        if numarg == 1:
            require_additional_argument('deactivate')

        deactivate_package(args[1])
        sys.exit()

    elif mainarg == "activate":
        if numarg == 1:
            require_additional_argument('activate')

        activate_package(args[1])
        sys.exit()

    elif mainarg == "list":
        q = CONF.INSTALLED
        for d in q:
            if d[1] == 0:
                print d[0] + " [deactivated]"
            else:
                print d[0]

        sys.exit()

    elif mainarg == "show":
        q = CONF.INSTALLED
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




    '''
    Compile is by default. 
    Check whether there already exists the output file.
    If it does, abort except it is forced.
    '''
    if os.path.exists(PATH+'/'+OUTPUT):
        if not FORCE:
            exodus('File ' + OUTPUT + ' already exists')
    for f in args:
        INPUT += f + " "
    s, l = load_package_paths()


    '''
    Compile the iRRAM file.. 
    '''
    try:
        subprocess.check_call(message(CONF.COMPILER[2], INPUT, s, l, OUTPUT), shell=True)
        print '[irramsh] compile finished'
    except subprocess.CalledProcessError as err:
        # print err.output
        exodus('\n[irramsh] compile failed')

if __name__ == "__main__":

    main(sys.argv[1:])
