#!/usr/bin/env python

#actions:				(IDX in A)
#dispatch_history:		(IDX in V)
#comments:				(IDX in V)
#abort:					(IDX in V)

import sys
import xml.etree.ElementTree as ET

def CASE_INFO(Node):

	global CASE_INFO_SQL
	global CASE_INFO_SQL_INSERT
	global CASE_INFO_SQL_FIELDS
	global CASE_INFO_SQL_VALUES

	global CASE_INFO_INTERNAL_ID

	global ADCA_SQL
	global ADCA_SQL_INSERT
	global ADCA_SQL_FIELDS
	global ADCA_SQL_VALUES

	T = unicode(Node.tag).encode('utf-8').strip().upper()
	A = unicode(Node.attrib).encode('utf-8').strip().upper()
	V = unicode(Node.text).encode('utf-8').strip()

	if T == 'INTERNAL_ID':
		CASE_INFO_INTERNAL_ID = V

	if A =='{}':
		A = ''
	else:
		# print T, A
		pass

	if V == 'None':
		V = ''

	if T == 'CASEINFO':
		CASE_INFO_SQL_INSERT = 'INSERT INTO "CASE_INFO"' + '\n'
		pass
	else:
		if T == 'CASE':
			CASE_INFO_SQL = CASE_INFO_SQL + CASE_INFO_SQL_INSERT
			pass
		else:
			if T == 'ACTIONS' or T == 'DISPATCH_HISTORY' or T == 'COMMENTS' or T == 'ABORT':
				ADCA(Node)
				ADCA_SQL_Table = ''
				ADCA_SQL_INSERT = ''
				pass
				return
			else:
				CASE_INFO_SQL_FIELDS = CASE_INFO_SQL_FIELDS + '"' + T + '", '
				CASE_INFO_SQL_VALUES = CASE_INFO_SQL_VALUES + "'" + V + "', "

	for Child in Node:
		CASE_INFO(Child)

	if T == 'CASE':

		CASE_INFO_SQL = CASE_INFO_SQL.strip() + ' ' + '(' + CASE_INFO_SQL_FIELDS.strip().rstrip(',') + ')' + ' ' + 'VALUES(' + CASE_INFO_SQL_VALUES.strip().rstrip(',') + ')'

		print CASE_INFO_SQL
		print ADCA_SQL.strip()
		print "----------------------------------------------------------------------------------------------------------------------------------------------------------------"

		CASE_INFO_TABLE = ''
		CASE_INFO_SQL = ''
		CASE_INFO_SQL_FIELDS = ''
		CASE_INFO_SQL_VALUES = ''

		CASE_INFO_INTERNAL_ID = 0

		ADCA_SQL = ''

def ADCA(Node):

	global ADCA_SQL
	global ADCA_SQL_INSERT
	global ADCA_SQL_FIELDS
	global ADCA_SQL_VALUES

	if Node.find('rep_id') == None:
		REP_ID = 0
	else:
		REP_ID = 1

	T = unicode(Node.tag).encode('utf-8').strip().upper()
	A = unicode(Node.attrib).encode('utf-8').strip().upper()
	V = unicode(Node.text).encode('utf-8').strip()

	if A =='{}':
		A = ''
	else:
		# print T, A
		pass

	if V == 'None':
		V = ''

	if T == 'ACTIONS' or T == 'DISPATCH_HISTORY' or T == 'COMMENTS' or T == 'ABORT':
		ADCA_SQL_INSERT = 'INSERT INTO "' + T + '"'
		pass
	else:
		if ((T == 'DISPATCH' or T == 'COMMENT' or T == 'ABORTED') and REP_ID) or T == 'ACTION':
			ADCA_SQL = ADCA_SQL + ADCA_SQL_INSERT
			if T == 'ACTION':
				ACTION_IDX = Node.get('idx','').strip()
				ADCA_SQL_FIELDS = '"INTERNAL_ID", "IDX", '
				ADCA_SQL_VALUES = CASE_INFO_INTERNAL_ID + ', ' + ACTION_IDX + ', '
			else:
				ADCA_SQL_FIELDS = '"INTERNAL_ID", '
				ADCA_SQL_VALUES = CASE_INFO_INTERNAL_ID + ', '
			pass
		else:
			ADCA_SQL_FIELDS = ADCA_SQL_FIELDS + '"' + T + '", '
			ADCA_SQL_VALUES = ADCA_SQL_VALUES + "'" + V + "', "

	for Child in Node:
		ADCA(Child)

	if ((T == 'DISPATCH' or T == 'COMMENT' or T == 'ABORTED') and REP_ID) or T == 'ACTION':

		ADCA_SQL = ADCA_SQL.strip() + ' ' + '(' + ADCA_SQL_FIELDS.strip().rstrip(',') + ')' + ' ' + 'VALUES(' + ADCA_SQL_VALUES.strip().rstrip(',') + ')'
		ADCA_SQL = ADCA_SQL.strip() + '\n'

		ADCA_SQL_FIELDS = ''
		ADCA_SQL_VALUES = ''
		ACTION_IDX = ''

try:
	Input = str(sys.argv[1])
except:
	print 'No input file specified.'
	sys.exit()

with open(Input,'r') as XML_File:
    Tree = ET.parse(XML_File)

Node = Tree.getroot()

CASE_INFO_SQL = ''
CASE_INFO_SQL_INSERT = ''
CASE_INFO_SQL_FIELDS = ''
CASE_INFO_SQL_VALUES = ''

CASE_INFO_INTERNAL_ID = 0

ADCA_SQL = ''
ADCA_SQL_INSERT = ''
ADCA_SQL_FIELDS = ''
ADCA_SQL_VALUES = ''


CASE_INFO(Node)
