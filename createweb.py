# -*- coding: utf-8 -*-

#
#Scrip para añadir webs usando ngix y python
#

import optparse
import sys
import os
from nginx import nginx_main, nginx_check
from supervisor import supervisor_conf, supervisor_check
from user import user
from virtualenv import virtualenv_check, virtualenv

def dirweb(project):
    print('\033[92 Creamos el directorio web\033[0m')
    os.mkdir('/home/'+project+'/web')
    os.system('chown '+project+' /home/'+project+'/web')
    os.system('chgrp '+project+' /home/'+project+'/web')

def main():
    domain = ""
    project = ""
    project_type = ''
    estrue = True
    while(domain==""):
        domain = raw_input("\033[92mDominio (Sin www):\033[0m ")
    while(project==""):
        project = raw_input("\033[92mNombre del proyecto:\033[0m ")
    while estrue:
        project_type = raw_input("\033[92mTipo de proyecto\n"
                                 "--> python\n"
                                 "--> php\n"
                                 "Pon uno de los tipos permitidos:\033[0m ")
        if project_type == "php":
            estrue = False
        if project_type =="python":
            estrue = False
    #Comprobamos si nginx esta instalado
    nginx_check()
    #Llamamos al modulo de usuario
    user(project)
    dirweb(project)
    if project_type == "python":
        #Comprobamos si esta instalado supervisor
        supervisor_check()
        #Comprobamos si esta instalado virtualenv o virtualenvwrapper
        virtualenv_check()
        #Al ser python creamos una virtualenv para el proyecto
        virtualenv(project)


    #Llamamos la modulo de nginx
    nginx_main(domain, project, project_type)
    #si el projecto esta en python, llamamos a supervisor para generar la configuracion
    if project_type == "python":
        supervisor_conf(project)

if __name__ == '__main__':
    main()
