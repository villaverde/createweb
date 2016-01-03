#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Script para añadir archivo de configuración ngix para aplicaciones python o php
#
import os
import sys
from there_application import which
pathConfNginx=os.path.dirname('/etc/nginx/') #Path a la configuracion de nginx

#Funcionar principal que se encarg de la configuracion de ngix
def nginx_main(domain,project,project_type):

    try:
        os.stat(pathConfNginx)
    except:
        print "\033[91mError el direcotrio %s no exixta\nNo se seguira creando nada\033[0m" % (pathConfNginx)
        return
    nginx_conf(domain, project, project_type)
    nginx_ln(project)

#funcion que genera archivo nginx en función de los parámetros indicados
#parametros: domain = dominio del proyecto; project = nombre del proyecto
#devuelve un archivo de configuración de nginx 
def nginx_conf(domain, project, project_type):
	#parametros de configuración
    if project_type =='python':
        fFile = open("templates/nginx/nginx_python_template.conf", "r")
    elif project_type == 'php':
        fFile = open("templates/nginx/nginx_php_template.conf", "r")
    fFile_new = open(pathConfNginx+"/sites-available/"+project+".conf", "w")
    content = fFile.read()
    content = content.replace('{project}', project)
    content = content.replace('{domain}', domain)
    fFile_new.write(content)
    print("\033[92mCreada la configuracion de nginx\033[0m")

def nginx_ln(project):
    comando = 'ln -s '+pathConfNginx+'/sites-available/'+project+'.conf '+pathConfNginx+'/sites-enabled/'+project+'.conf'
    os.system(comando)
    print("\033[92mCreado en enlace simbolico de nginx para activar el virtualhost\033[0m")

def nginx_check():
    print('\033[92m Comprobando si esta instalado NGINX\033[0m')
    if which('nginx') == None:
        print('\033[91m  *  Nginx no esta instalado. Instalalo para poder seguir\033[0m')
        sys.exit(0)
    else:
        print('\033[92m  * Nginx esta instalado\033[0m')
