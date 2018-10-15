--
-- Create Schema Script
--   Database Version            : 11.2.0.4.0
--   Database Compatible Level   : 11.2.0.4.0
--   Script Compatible Level     : 11.2.0.4.0
--   Toad Version                : 13.0.0.80
--   DB Connect String           : 172.25.48.16:1522/USSD
--   Schema                      : USSD
--   Script Created by           : USSD
--   Script Created at           : 10/15/2018 12:47:25 PM
--   Notes                       : 
--

-- Object Counts: 
--   Triggers: 1 


CREATE OR REPLACE TRIGGER USSD.T_PLSQL_BACKUP
    --BEFORE DDL 
    BEFORE ALTER OR CREATE OR DROP
    ON SCHEMA
DECLARE
    oper       VARCHAR2 (32000);
    sql_text   ora_name_list_t;
    n          NUMBER;
    v_stmt     CLOB;
    -- ADD Thursday, September 20, 2018
    jobnumber     NUMBER;
    v_job_date    DATE;
    v_obj_name    plsql_archive.name%TYPE;
    v_obj_type    plsql_archive.TYPE%TYPE;
    v_obj_owner   plsql_archive.owner%TYPE;
    v_action      plsql_archive.action%TYPE;
    v_ip          plsql_archive.IP%TYPE;
    v_osuser      plsql_archive.OSUSER%TYPE;
--    v_new_src     plsql_archive.new_src%TYPE;
    v_old_src     plsql_archive.OLD_SRC%TYPE;
    v_err         plsql_archive.ERR%TYPE;
    v_type        VARCHAR2 (4000) := 'MAHDI';
    
BEGIN
    oper := ora_sysevent;

    IF ora_dict_obj_name IS NOT NULL
    THEN
    
    v_obj_name := ora_dict_obj_name;
            v_obj_type := ora_dict_obj_type;
            v_obj_owner := ora_dict_obj_owner;
--            v_new_src := 'test';
            v_action := oper;
            v_ip := SYS_CONTEXT ('USERENV', 'IP_ADDRESS');
            v_osuser := SYS_CONTEXT ('USERENV', 'OS_USER');
            v_err := SQLERRM();   
            
--    v_obj_name := 'test';
--    v_obj_type := 'test';
--    v_obj_owner := 'test';
--    v_new_src := 'test';
--    v_action := 'test';
--    v_ip := 'test';
--    v_osuser := 'test';
--    v_old_src := 'test';
--    v_err := 'test';
    
    END IF;
    
    
            -- This job is fired after 2 second
            v_job_date := SYSDATE + 0.2 / 7600; --2 sec
            DBMS_JOB.submit (
                job         => jobnumber,
                what        =>
                       'BEGIN 
                            plsql_backup.backup (
                            '''|| v_obj_name|| ''',
                            '''|| v_obj_type|| ''',
                            '''|| v_obj_owner|| ''',
                            '''|| v_action|| ''',
                            '''|| v_ip|| ''',
                            '''|| v_osuser|| ''',
                            '''|| v_err|| '''
                            );
                        COMMIT;
                        END;                
                ',
                next_date   => v_job_date,
                interval    => 'Null',
                no_parse    => FALSE);
            
EXCEPTION
    WHEN OTHERS
    THEN
--        NULL;
        raise_application_error('-20001',sqlerrm);
END t_plsql_backup;
/