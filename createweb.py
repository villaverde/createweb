#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Scrip para añadir webs usando ngix y python
#

import optparse
import sys
from nginx import nginx_conf



def main():
    domain = raw_input("Dominio (Sin www): ")
    project = raw_input("Nombre del proyecto: ")
    project_type = raw_input("Tipo de proyecto\n"
                             "--> Python\n"
                             "--> PHP\n"
                             "Pon uno de los tipos permitidos: ")
    dns = raw_input("Quieres añadir el dominio al servidores de dns (BIND)?\n"
                    "si\n"
                    "no\n"
                    ": ")
    nginx_conf(domain, project, project_type)

if __name__ == '__main__':
