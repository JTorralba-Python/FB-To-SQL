CREATE TABLE DISPATCH_HISTORY (
	INTERNAL_ID BIGINT NOT NULL,
	IDX INTEGER DEFAULT 0 NOT NULL,
	CC INTEGER DEFAULT 0,
	LVL VARCHAR(10),
	SUBLVL INTEGER DEFAULT 0,
	SUFFIX VARCHAR(10),
	DISPTYPE INTEGER DEFAULT 0,
	LOCAL_SUFFIX VARCHAR(10),
	REP_ID CHAR(38)
) ;
CREATE INDEX IX_DISPATCH_HISTORY_1 ON DISPATCH_HISTORY (INTERNAL_ID) ;
CREATE INDEX IX_DISPATCH_HISTORY_2 ON DISPATCH_HISTORY (CC,LVL,SUBLVL,SUFFIX) ;
