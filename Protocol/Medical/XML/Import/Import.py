#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET

def CASE_INFO(Node):

	global CASE_INFO_SQL
	global CASE_INFO_SQL_TABLE
	global CASE_INFO_SQL_INSERT
	global CASE_INFO_SQL_FIELDS
	global CASE_INFO_SQL_VALUES

	global CASE_INFO_INTERNAL_ID

	global ADCA_SQL
	global ADCA_SQL_TABLE
	global ADCA_SQL_INSERT
	global ADCA_SQL_FIELDS
	global ADCA_SQL_VALUES

	T = unicode(Node.tag).encode('utf-8').strip().upper()
	V = unicode(Node.text).encode('utf-8').strip().replace("'", "''")

	if T == 'INTERNAL_ID':
		CASE_INFO_INTERNAL_ID = V

	if V == 'None':
		V = ''

	if T == 'CASEINFO':
		CASE_INFO_SQL_TABLE = 'CASE_INFO'
		CASE_INFO_SQL_INSERT = 'INSERT INTO "CASE_INFO"' + '\n'
		pass
	else:
		if T == 'CASE':
			CASE_INFO_SQL = CASE_INFO_SQL + CASE_INFO_SQL_INSERT
			pass
		else:
			if T == 'ACTIONS' or T == 'DISPATCH_HISTORY' or T == 'COMMENTS' or T == 'ABORT':
				ADCA(Node)

				ADCA_SQL_TABLE = ''
				ADCA_SQL_INSERT = ''
				ADCA_SQL_FIELDS = ''
				ADCA_SQL_VALUES = ''

				pass
				return
			else:
				if InSchema(T):
					CASE_INFO_SQL_FIELDS = CASE_INFO_SQL_FIELDS + '"' + T + '", '
					CASE_INFO_SQL_VALUES = CASE_INFO_SQL_VALUES + DataType(CASE_INFO_SQL_TABLE,T,V)

	for Child in Node:
		CASE_INFO(Child)

	if T == 'CASE':

		CASE_INFO_SQL = CASE_INFO_SQL.strip() + ' ' + '(' + CASE_INFO_SQL_FIELDS.strip().rstrip(',') + ')' + ' ' + 'VALUES(' + CASE_INFO_SQL_VALUES.strip().rstrip(',') + ')'
		CASE_INFO_SQL = CASE_INFO_SQL.strip() + ';'

		print CASE_INFO_SQL
		print ADCA_SQL.strip()
		#print "----------------------------------------------------------------------------------------------------------------------------------------------------------------"

		CASE_INFO_SQL = ''
		CASE_INFO_INSERT = ''
		CASE_INFO_SQL_FIELDS = ''
		CASE_INFO_SQL_VALUES = ''

		CASE_INFO_INTERNAL_ID = 0

		ADCA_SQL = ''

def ADCA(Node):

	global ADCA_SQL
	global ADCA_SQL_TABLE
	global ADCA_SQL_INSERT
	global ADCA_SQL_FIELDS
	global ADCA_SQL_VALUES

	if Node.find('rep_id') == None:
		REP_ID = 0
	else:
		REP_ID = 1

	T = unicode(Node.tag).encode('utf-8').strip().upper()
	V = unicode(Node.text).encode('utf-8').strip().replace("'", "''")

	if V == 'None':
		V = ''

	if T == 'ACTIONS' or T == 'DISPATCH_HISTORY' or T == 'COMMENTS' or T == 'ABORT':
		ADCA_SQL_TABLE = T
		ADCA_SQL_INSERT = 'INSERT INTO "' + T + '"'
		pass
	else:
		if T == 'ACTION' or ((T == 'DISPATCH' or T == 'COMMENT' or T == 'ABORTED') and REP_ID):
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
			if InSchema(T):
				ADCA_SQL_FIELDS = ADCA_SQL_FIELDS + '"' + T + '", '
				ADCA_SQL_VALUES = ADCA_SQL_VALUES + DataType(ADCA_SQL_TABLE, T, V)

	for Child in Node:
		ADCA(Child)

	if T == 'ACTION' or ((T == 'DISPATCH' or T == 'COMMENT' or T == 'ABORTED') and REP_ID):

		ADCA_SQL = ADCA_SQL.strip() + ' ' + '(' + ADCA_SQL_FIELDS.strip().rstrip(',') + ')' + ' ' + 'VALUES(' + ADCA_SQL_VALUES.strip().rstrip(',') + ')'
		ADCA_SQL = ADCA_SQL.strip() + ';\n'

def DataType(SQL_TABLE, T, V):

	global CASE_INFO_SCHEMA_NUMERIC
	global ACTIONS_SCHEMA_NUMERIC
	global DISPATCH_HISTORY_SCHEMA_NUMERIC
	global COMMENTS_SCHEMA_NUMERIC
	global ABORT_SCHEMA_NUMERIC

	if (T == 'INTERNAL_ID') or (T == 'IDX') or (SQL_TABLE == 'CASE_INFO' and T in CASE_INFO_SCHEMA_NUMERIC) or (SQL_TABLE == 'ACTIONS' and T in ACTIONS_SCHEMA_NUMERIC) or (SQL_TABLE == 'DISPATCH_HISTORY' and T in DISPATCH_HISTORY_SCHEMA_NUMERIC) or (SQL_TABLE == 'COMMENTS' and T in COMMENTS_SCHEMA_NUMERIC) or (SQL_TABLE == 'ABORT' and T in ABORT_SCHEMA_NUMERIC):
		if V == '':
			Value = "0, "
		else:
			Value = V + ", "
	else:
		Value = "'" + V + "', "

	return Value

def InSchema(T):

	global NOT_IN_SCHEMA

	if T in NOT_IN_SCHEMA:
		return False
	else:
		return True

try:
	Input = str(sys.argv[1])
except:
	print 'No input file specified.'
	sys.exit()

with open(Input,'r') as XML_File:
    Tree = ET.parse(XML_File)

Node = Tree.getroot()

CASE_INFO_SCHEMA_NUMERIC = ['INTERNAL_ID', 'PARTY', 'PATIENTS', 'AGE', 'AGEUNIT', 'GENDER', 'CONSCIOUS', 'BREATHING', 'CC', 'RON_TOTAL', 'OVERRIDE', 'STATUS', 'SHUNTED', 'SHUNTEDTO', 'RECONFIGURED', 'RECONFIGURE_OC', 'RE_EVAL', 'LANGUAGE_NO', 'PENDING', 'PROGFORM', 'PROGFIELD', 'TESTCASE', 'SHIFTED', 'SHIFTED_CC', 'SHIFTED_SUBLVL', 'CALLER_LANGUAGE_NO', 'CALL_PHONE_TYPE', 'DELETED', 'ARCH', 'AMOD']

ACTIONS_SCHEMA_NUMERIC = ['INTERNAL_ID', 'IDX', 'ACTION_CODE']

DISPATCH_HISTORY_SCHEMA_NUMERIC = ['INTERNAL_ID', 'IDX', 'CC', 'SUBLVL', 'DISPTYPE']

COMMENTS_SCHEMA_NUMERIC = ['INTERNAL_ID', 'IDX', 'VAR1', 'VAR2', 'VAR3', 'VAR4', 'VAR5', 'VAR6', 'VAR7', 'VAR8', 'VAR9', 'VAR10']

ABORT_SCHEMA_NUMERIC = ['INTERNAL_ID', 'IDX']

NOT_IN_SCHEMA = ['LON_1', 'LAT_1', 'INFO_DE', 'INFO_CBRN', 'TRANSFER']

CASE_INFO_SQL = ''
CASE_INFO_SQL_TABLE = ''
CASE_INFO_SQL_INSERT = ''
CASE_INFO_SQL_FIELDS = ''
CASE_INFO_SQL_VALUES = ''

CASE_INFO_INTERNAL_ID = 0

ADCA_SQL = ''
ADCA_SQL_TABLE = ''
ADCA_SQL_INSERT = ''
ADCA_SQL_FIELDS = ''
ADCA_SQL_VALUES = ''

CASE_INFO(Node)
