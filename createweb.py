#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#Scrip para añadir webs usando ngix y python
#

import optparse
import common

def create_web(options):
	if not options.domain:
		print('No se especifico ningun dominio')
		return

def main():
	parser = optparse.OptionParser()
	parser.add_option('-d', '--domain', help='Nombre del dominio')
	parser.add_option('-p', '--project', help='Nombre del proyecto')
	parser.add_option('-t', '--type', help='Tipo de alojamiento. Por ahora solo doy soporte a django')
	options = common.parser(parser)

	create_web(options)

if __name__ == '__main__':
	main()
