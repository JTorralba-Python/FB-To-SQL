CREATE TABLE COMMENTS (
	INTERNAL_ID BIGINT NOT NULL,
	IDX INTEGER DEFAULT 0,
	VAR1 INTEGER DEFAULT 0,
	VAR2 INTEGER DEFAULT 0,
	VAR3 INTEGER DEFAULT 0,
	VAR4 INTEGER DEFAULT 0,
	VAR5 INTEGER DEFAULT 0,
	VAR6 INTEGER DEFAULT 0,
	VAR7 INTEGER DEFAULT 0,
	VAR8 INTEGER DEFAULT 0,
	VAR9 INTEGER DEFAULT 0,
	VAR10 INTEGER DEFAULT 0,
	COMMENT VARCHAR(512),
	REP_ID CHAR(38)
) ;
CREATE INDEX IDX_COMMENTS ON COMMENTS (INTERNAL_ID) ;
