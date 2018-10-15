CREATE OR REPLACE PACKAGE USSD.plsql_backup
AS
    -- The procedure is called for the compilation of objects by means of a trigger
    PROCEDURE backup (p_name      IN plsql_archive.name%TYPE,
                      p_type      IN plsql_archive.type%TYPE,
                      p_owner     IN plsql_archive.owner%TYPE,
                      p_action    IN plsql_archive.action%TYPE,
                      p_ip        IN plsql_archive.IP%TYPE,
                      p_osuser    IN plsql_archive.OSUSER%TYPE,
                      p_err       IN plsql_archive.ERR%TYPE);
END plsql_backup;
/