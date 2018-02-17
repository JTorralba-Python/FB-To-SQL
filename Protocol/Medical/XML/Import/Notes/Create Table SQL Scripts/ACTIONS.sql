CREATE TABLE ACTIONS (
	INTERNAL_ID BIGINT NOT NULL,
	IDX INTEGER DEFAULT 0 NOT NULL,
	ACTION_CODE INTEGER DEFAULT 0,
	VAR1 VARCHAR(10),
	VAR2 VARCHAR(10),
	VAR3 VARCHAR(10),
	VAR4 VARCHAR(10),
	VAR5 VARCHAR(10),
	VAR6 VARCHAR(10),
	VAR7 VARCHAR(10),
	VAR8 VARCHAR(10),
	VAR9 VARCHAR(10),
	VAR10 VARCHAR(10),
	DATE_TIME TIMESTAMP,
	OPERATOR VARCHAR(30),
	DATA1 VARCHAR(512),
	DATA2 VARCHAR(512),
	DATA3 VARCHAR(512),
	REP_ID CHAR(38),
	DATA4 BLOB SUB_TYPE 1
) ;
CREATE INDEX IX_ACTIONS_1 ON ACTIONS (INTERNAL_ID) ;
CREATE INDEX IX_ACTIONS_2 ON ACTIONS (INTERNAL_ID,ACTION_CODE) ;
