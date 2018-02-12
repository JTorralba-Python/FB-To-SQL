#!/usr/bin/env python

#actions:				(IDX in A)
#dispatch_history:		(IDX in V)
#comments:				(IDX in V)
#abort:					(IDX in V)

import sys
import xml.etree.ElementTree as ET

def CASE_INFO(Node):

	global CASE_INFO_SQL
	global CASE_INFO_SQL_Table
	global ADCA_SQL
	global ADCA_SQL_Table

	T = unicode(Node.tag).encode('utf-8')
	A = unicode(Node.attrib).encode('utf-8')
	V = unicode(Node.text).encode('utf-8')

	if A=='{}':
		A = ':'
	else:
		A = ':' + A + ':'

	if str(Node.tag)=='caseinfo':
		#CASE_INFO_SQL_Table = str(Node.tag).upper()
		CASE_INFO_SQL_Table = 'CASE_INFO'
		pass
	else:
		if str(Node.tag)=='case':
			CASE_INFO_SQL = CASE_INFO_SQL + CASE_INFO_SQL_Table + ' --> '
			pass
		else:
			if str(Node.tag)=='actions' or str(Node.tag)=='dispatch_history' or str(Node.tag)=='comments' or str(Node.tag)=='abort':
				ADCA(Node)
				ADCA_SQL_Table = ''
				pass
				return
			else:
				X = T.strip() + ':'+ V.strip()
				CASE_INFO_SQL = CASE_INFO_SQL + X

	for Child in Node:
		CASE_INFO(Child)

	if str(Node.tag)=='case':
		print CASE_INFO_SQL.rstrip()
		print ADCA_SQL.rstrip()
		print "----------------------------------------------------------------------------------------------------------------------------------------------------------------"
		CASE_INFO_SQL = ''
		ADCA_SQL = ''

def ADCA(Node):

	global ADCA_SQL
	global ADCA_SQL_Table

	if Node.find('rep_id')==None:
		REP_ID = 0
	else:
		REP_ID = 1

	T = unicode(Node.tag).encode('utf-8')
	A = unicode(Node.attrib).encode('utf-8')
	V = unicode(Node.text).encode('utf-8')

	if A=='{}':
		A = ':'
	else:
		A = ':' + A + ':'

	if str(Node.tag)=='actions' or str(Node.tag)=='dispatch_history' or str(Node.tag)=='comments' or str(Node.tag)=='abort':
		ADCA_SQL_Table = str(Node.tag).upper()
		pass
	else:
		if ((str(Node.tag)=='dispatch' or str(Node.tag)=='comment' or str(Node.tag)=='aborted') and REP_ID) or str(Node.tag)=='action':
			ADCA_SQL = ADCA_SQL + ADCA_SQL_Table + ' --> '
			pass
		else:
			X =  T.strip() + ':'+ V.strip()
			ADCA_SQL = ADCA_SQL + X

	for Child in Node:
		ADCA(Child)

	if ((str(Node.tag)=='dispatch' or str(Node.tag)=='comment' or str(Node.tag)=='aborted') and REP_ID) or str(Node.tag)=='action':
		ADCA_SQL = ADCA_SQL + '\n'

try:
	Input = str(sys.argv[1])
except:
	print 'No input file specified.'
	sys.exit()

with open(Input,'r') as XML_File:
    Tree = ET.parse(XML_File)

Node = Tree.getroot()

CASE_INFO_SQL = ''
CASE_INFO_SQL_Table = ''
ADCA_SQL = ''
ADCA_SQL_Table = ''

CASE_INFO(Node)
CASE_INFO_SQL_Table = ''
