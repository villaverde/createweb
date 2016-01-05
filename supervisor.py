#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Scrip para configurar supervisor
#

import os
import sys
from there_application import which

#funcion que genera archivo supervisor en función de los parámetros indicados
#parametros: project = nombre del proyecto
#devuelve un archivo de configuración de supervisor



def supervisor_conf(project):
	#parametros de configuración
    path = os.path.dirname('/etc/supervisor/conf.d/')
    try:
        os.stat(path)
    except:
        print("\033[91mError el direcotrio "+path+" no exixta\nNo se seguira creando nada\033[0m")
        return
    fFile = open("templates/supervisor/supervisor_template.conf", "r")
    fFile_new = open(path+'/'+project+".conf", "w")
    content = fFile.read()
    content = content.replace('{project}', project)
    fFile_new.write(content)
    print("\033[92mCreada la configuracion de supervisor\n\033[0m")

def supervisor_check():
    print('\033[92m Comprobando si esta instalado SUPERVISOR\033[0m')
    if which('supervisorctl') == None:
        print('\033[91m  * Supervisor no esta instalado. Instalalo para poder seguir\033[0m')
        sys.exit(0)
    else:
        print('\033[92m  * Supervisor esta instalado\033[0m')
