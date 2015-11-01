#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Scrip para añadir webs usando ngix y python
#

import optparse
import sys
from nginx import nginx_conf



def main():
    domain = ""
    project = ""
    project_type = ''
    estrue = True
    while(domain==""):
        domain = raw_input("Dominio (Sin www): ")
    while(project==""):
        project = raw_input("Nombre del proyecto: ")
    while estrue:
        print project_type
        project_type = raw_input("Tipo de proyecto\n"
                                 "--> python\n"
                                 "--> php\n"
                                 "Pon uno de los tipos permitidos: ")
        if project_type == "php":
            estrue = False
        if project_type =="python":
            estrue = False
    dns = raw_input("Quieres añadir el dominio al servidores de dns (BIND)?\n"
                    "si\n"
                    "no\n"
                    ": ")
    nginx_conf(domain, project, project_type)

if __name__ == '__main__':
    main()
