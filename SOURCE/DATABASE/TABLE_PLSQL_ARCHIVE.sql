CREATE TABLE PLSQL_ARCHIVE
(
  ID       NUMBER,
  NAME     VARCHAR2(128 BYTE),
  TYPE     VARCHAR2(20 BYTE),
  OWNER    VARCHAR2(100 BYTE),
  CREATED  DATE,
  STATUS   VARCHAR2(10 BYTE),
  OLD_SRC  CLOB                                 DEFAULT EMPTY_CLOB(),
  NEW_SRC  CLOB                                 DEFAULT EMPTY_CLOB(),
  ERR      VARCHAR2(4000 BYTE),
  OSUSER   VARCHAR2(254 BYTE),
  IP       VARCHAR2(20 BYTE),
  ACTION   VARCHAR2(32 BYTE)
);

alter table plsql_archive add constraint pk_plsql_archive primary key(id);

create index idx_plsql_archive on plsql_archive(name, type, owner);