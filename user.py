#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pwd
import subprocess
import shutil
import sys
import grp

CHROOT_BASE = '/home/chroot'
APPS        = ['/bin/sh',
               '/bin/bash',
               '/usr/bin/id',
               '/bin/hostname',
               '/bin/ls',
               '/bin/cat',
               '/bin/grep',
               '/usr/bin/cut',
               '/usr/bin/find',
               ]

def shlibs(f):
    if not os.path.exists(f):
        raise IOError, '%s does not exists' % f

    try:
        ldd_output = subprocess.check_output(['/usr/bin/ldd', f]).split('\n')
    except subprocess.CalledProcessError:
        return []

    shlibs = []
    for eachLib in ldd_output:
        if not eachLib:
            continue

        libInfo = eachLib.split()
        if os.path.splitext(libInfo[0])[0] == 'linux-vdso.so':
            continue

        if libInfo[1] == '=>':
            shlibs.append(libInfo[2])
        else:
            shlibs.append(libInfo[0])

    return shlibs

def chroot_create_base_dirs(user_chroot):
    print('\033[92mCreando/Actulizado los directorio de la base chroot\033[0m')
    if not os.path.exists(CHROOT_BASE):
        print('\033[92m     * Creando la base CHROOT => '+CHROOT_BASE+'\033[0m')
        os.makedirs(CHROOT_BASE)

    if not os.path.exists(user_chroot):
        print('\033[92m     * Creando el direcotrio de chroot => '+user_chroot+'\033[0m')
        os.makedirs(user_chroot)

    if not os.path.exists(os.path.join(user_chroot, 'root')):
        print('\033[92m     * Creando direcotrio chroot => /root\033[0m')
        os.makedirs(os.path.join(user_chroot, 'root'))
        os.chmod(os.path.join(user_chroot, 'root'), 0700)

def chroot_create_user(user, user_chroot):
    try:
        user_home = pwd.getpwnam(user)[5]
        print('\033[93mActualizando el usuario a chroot => \033[0m'+user)
    except KeyError as e:
        print('\033[92mEl usuario no existe, se creara\033[0m')
        subprocess.call(['/usr/sbin/adduser', user])
        user_home = pwd.getpwnam(user)[5]

    if not os.path.exists(os.path.join(user_chroot, user_home[1:])):
        print('\033[93m     * Instalando los archivos chroot => Archivos de skel para \033[0m'+user)
        shutil.copytree('/etc/skel', os.path.join(user_chroot, user_home[1:]))
    else:
        print('\033[92m     * Reinstalando lso archivos chroot => Archivos del skel para \033[0m'+user)
        shutil.rmtree(os.path.join(user_chroot, user_home[1:]))
        shutil.copytree('/etc/skel', os.path.join(user_chroot, user_home[1:]))

def chroot_create_dev(user_chroot):
    print('\033[92mCreando /dev para el chroot\033[0m')
    if not os.path.exists(os.path.join(user_chroot, 'dev')):
        print('\033[92m     * Creando el directorio dev para el chroot\033[0m')
        os.makedirs(os.path.join(user_chroot, 'dev'))

    if not os.path.exists(os.path.join(user_chroot, 'dev/null')):
        print('\033[92m     * Creando las entradas para dev => /dev/null\033[0m')
        subprocess.call(['/bin/mknod', '-m', '666', os.path.join(user_chroot, 'dev/null'), 'c', '1', '3'])

    if not os.path.exists(os.path.join(user_chroot, 'dev/zero')):
        print('\033[92m     *  Creando las entradas para dev => /dev/zero\033[0m')
        subprocess.call(['/bin/mknod', '-m', '666', os.path.join(user_chroot, 'dev/zero'), 'c', '1', '5'])

    if not os.path.exists(os.path.join(user_chroot, 'dev/random')):
        print('\033[92m     *  Creando las entradas para dev => /dev/random\033[0m')
        subprocess.call(['/bin/mknod', '-m', '666', os.path.join(user_chroot, 'dev/random'), 'c', '1', '8'])

    if not os.path.exists(os.path.join(user_chroot, 'dev/urandom')):
        print('\033[92m     *  Creando las entradas para dev => /dev/urandom\033[0m')
        subprocess.call(['/bin/mknod', '-m', '666', os.path.join(user_chroot, 'dev/urandom'), 'c', '1', '9'])

def chroot_create_etc(user_chroot):
    print('\033[92mCreando las entradas /dev para el entrono chroot\033[0m')
    chroot_etc_dir = os.path.join(user_chroot, 'etc')
    if not os.path.exists(chroot_etc_dir):
        print('\033[92m      * Creando el directorio chroot => /etc\033[0m')
        os.makedirs(chroot_etc_dir)

    print('\033[92m      * Instalando los ficheros chroot => /etc/profile\033[0m')
    shutil.copy2('/etc/profile', os.path.join(chroot_etc_dir, 'profile'))


    print('\033[92m      * Instalando los ficheros chroot => /etc/hosts\033[0m')
    shutil.copy2('/etc/hosts', os.path.join(chroot_etc_dir, 'hosts'))

    print('\033[92m      * Instalando los ficheros chroot => /etc/services\033[0m')
    shutil.copy2('/etc/services', os.path.join(chroot_etc_dir, 'services'))

    if not os.path.exists(os.path.join(chroot_etc_dir, 'profile.d')):
        print('\033[92m      * Instalando los ficheros chroot => /etc/profile.d\033[0m')
        shutil.copytree('/etc/profile.d', os.path.join(chroot_etc_dir, 'profile.d'))
    else:
        print('\033[92m      * Reinstalando los ficheros chroot => /etc/profile.d\033[0m')
        shutil.rmtree(os.path.join(chroot_etc_dir, 'profile.d'))
        shutil.copytree('/etc/profile.d', os.path.join(chroot_etc_dir, 'profile.d'))

    if not os.path.exists(os.path.join(chroot_etc_dir, 'skel')):
        print('\033[92m      * Instalando los ficheros chroot => /etc/skel\033[0m')
        shutil.copytree('/etc/skel', os.path.join(chroot_etc_dir, 'skel'))
    else:
        print('\033[92m      * Reinstalando los ficheros chroot => /etc/skel\033[0m')
        shutil.rmtree(os.path.join(chroot_etc_dir, 'skel'))
        shutil.copytree('/etc/skel', os.path.join(chroot_etc_dir, 'skel'))

    print('\033[92m      * Reinstalando los ficheros chroot => /etc/locale.alias\033[0m')
    shutil.copy2('/etc/locale.alias', os.path.join(chroot_etc_dir, 'locale.alias'))

    print('\033[92m      * Reinstalando los ficheros chroot => /etc/locale.gen\033[0m')
    shutil.copy2('/etc/locale.gen', os.path.join(chroot_etc_dir, 'locale.gen'))

def chroot_install_apps(user_chroot, force_overwrite=False):
    print('\033[92m (Re)Instalando las aplicaiones del entorno chroot\033[0m')

    for eachApp in APPS:
        app_dir  = os.path.dirname(eachApp)
        app_name = os.path.basename(eachApp)

        if app_dir.startswith('/'):
            app_chroot_dir = os.path.join(user_chroot, app_dir[1:])
        else:
            app_chroot_dir = os.path.join(user_chroot, app_dir)

        app_chroot_location = os.path.join(app_chroot_dir, app_name)
        if not os.path.exists(app_chroot_dir):
            print('\033[92m      * Creando directorio chroot => '+app_chroot_dir+'\033[0m')
            os.makedirs(app_chroot_dir)

        if not os.path.exists(app_chroot_location) or (os.path.exists(app_chroot_location) and force_overwrite):
            print('\033[92m      * Instalando app chroot => '+app_chroot_location+'\033[0m')
            shutil.copy2(eachApp, app_chroot_location)

def chroot_install_shlibs(user_chroot, force_overwrite=False):
    print('\033[92m Instalando las librerias compartidas en el entrono chroot\033[0m')

    for eachApp in APPS:
        for eachLib in shlibs(eachApp):
            shlib_dir  = os.path.dirname(eachLib)
            shlib_name = os.path.basename(eachLib)
            if shlib_dir.startswith('/'):
                shlib_chroot_dir = os.path.join(user_chroot, shlib_dir[1:])
            else:
                shlib_chroot_dir = os.path.join(user_chroot, shlib_dir)

            shlib_chroot_location = os.path.join(shlib_chroot_dir, shlib_name)

            if not os.path.exists(shlib_chroot_dir):
                print('\033[92m      * Creando el directorio chroot => '+shlib_chroot_dir+'\033[0m')
                os.makedirs(shlib_chroot_dir)

            if not os.path.exists(shlib_chroot_location) or (os.path.exists(shlib_chroot_location) and force_overwrite):
                print('\033[92m      * Instalando el chroot shlib => '+shlib_chroot_location+'\033[0m')
                shutil.copy2(eachLib, shlib_chroot_location)

    print('\033[92m      * (Re)Instalando /lib/terminfo\033[0m')

    if not os.path.exists(os.path.join(user_chroot, 'lib/terminfo')):
        shutil.copytree('/lib/terminfo', os.path.join(user_chroot, 'lib/terminfo'))
    else:
        shutil.rmtree(os.path.join(user_chroot, 'lib/terminfo'))
        shutil.copytree('/lib/terminfo', os.path.join(user_chroot, 'lib/terminfo'))

    print('\033[92m      * (Re)Instalando /usr/lib/locale\033[0m')
    if not os.path.exists(os.path.join(user_chroot, 'usr/lib/locale')):
        shutil.copytree('/usr/lib/locale', os.path.join(user_chroot, 'usr/lib/locale'))
    else:
        shutil.rmtree(os.path.join(user_chroot, 'usr/lib/locale'))
        shutil.copytree('/usr/lib/locale', os.path.join(user_chroot, 'usr/lib/locale'))

def chroot_install_usr_share(user_chroot):
    print('\033[92m Instalando documentos en el entorno chroot\033[0m')

    if not os.path.exists(os.path.join(user_chroot, 'usr/share/locale')):
        print('\033[92m      * Instalando locales chroot => /usr/share/locale\033[0m')
        shutil.copytree('/usr/share/locale', os.path.join(user_chroot, 'usr/share/locale'))
    else:
        print('\033[92m      * Reinstalando locales chroot => /usr/share/locale\033[0m')
        shutil.rmtree(os.path.join(user_chroot, 'usr/share/locale'))
        shutil.copytree('/usr/share/locale', os.path.join(user_chroot, 'usr/share/locale'))

def user(project):
    user_chroot = os.path.join(CHROOT_BASE, project)
    chroot_create_base_dirs(user_chroot)
    chroot_create_user(project, user_chroot)
    chroot_create_dev(user_chroot)
    chroot_create_etc(user_chroot)
    chroot_install_apps(user_chroot)
    chroot_install_shlibs(user_chroot)
    chroot_install_usr_share(user_chroot)

    print('\033[92m Entorno chroot listo\033[0m')