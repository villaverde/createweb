#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Scrip para configurar supervisor
#




#funcion que genera archivo supervisor en función de los parámetros indicados
#parametros: project = nombre del proyecto
#devuelve un archivo de configuración de supervisor
def supervisor_conf(project):
	#parametros de configuración
	path = ''
	fFile = open("supervisor_template.conf", "r")
	fFile_new = open(path+project+".conf", "w")
	content = fFile.read()
	content = content.replace('{project}', project)
	fFile_new.write(content)


#parametros de configuración
project = 'juanillo'

supervisor_conf(project)