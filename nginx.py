#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Script para añadir archivo de configuración ngix para aplicaciones python o php
#
import os
pathConfNginx=os.path.dirname('/etc/nginx/') #Path a la configuracion de nginx

#Funcionar principal que se encarg de la configuracion de ngix
def nginx_main(domain,project,project_type):

    try:
        os.stat(pathConfNginx)
    except:
        print "Error el direcotrio %s no exixta\nNo se seguira creando nada" % (pathConfNginx)
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
    print("Creada la configuracion de nginx")

def nginx_ln(project):
    comando = 'ln -s '+pathConfNginx+'/sites-available/'+project+' '+pathConfNginx+'/sites-enabled/'+project
    os.system(comando)
    print("Creado en enlace simbolico de nginx para activar el virtualhost")