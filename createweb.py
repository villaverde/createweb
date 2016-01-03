# -*- coding: utf-8 -*-

#
#Scrip para añadir webs usando ngix y python
#

import optparse
import sys
from nginx import nginx_main, nginx_check
from supervisor import supervisor_conf
from user import user


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
    #Llamamos la modulo de nginx
    nginx_main(domain, project, project_type)
    #si el projecto esta en python, llamamos a supervisor para generar la configuracion
    if project_type == "python":
        supervisor_conf(project)

if __name__ == '__main__':
    main()
