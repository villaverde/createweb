#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Script para añadir archivo de configuración ngix para aplicaciones python o php
#




#funcion que genera archivo nginx en función de los parámetros indicados
#parametros: domain = dominio del proyecto; project = nombre del proyecto
#devuelve un archivo de configuración de nginx 
def nginx_conf(domain, project, project_type):
	#parametros de configuración
	path = ''
	if project_type =='python':
		fFile = open("nginx_python_template.conf", "r")
	elif project_type == 'php':
		fFile = open("nginx_php_template.conf", "r")
	fFile_new = open(path+project+".conf", "w")
	content = fFile.read()
	content = content.replace('{project}', project)
	content = content.replace('{domain}', domain)
	fFile_new.write(content)


#parametros de configuración
project = 'juanillo'
domain = 'http://carapillo.com'
project_type = 'python'
nginx_conf(domain, project, project_type)