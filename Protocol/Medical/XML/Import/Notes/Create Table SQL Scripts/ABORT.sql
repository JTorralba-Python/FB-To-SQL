CREATE TABLE ABORT (
	INTERNAL_ID BIGINT NOT NULL,
	IDX INTEGER DEFAULT 0,
	REASON VARCHAR(250),
	REP_ID CHAR(38)
) ;
CREATE INDEX IDX_ABORT ON ABORT (INTERNAL_ID) ;
