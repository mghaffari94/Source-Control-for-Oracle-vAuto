CREATE OR REPLACE PACKAGE BODY USSD.plsql_backup
AS

    FUNCTION get_code (p_name IN VARCHAR2, p_type IN VARCHAR2)
        RETURN CLOB
    IS
        v_code   CLOB := '';
    BEGIN
        FOR src IN (  SELECT text
                        FROM user_source
                       WHERE name = p_name AND type = p_type
                    ORDER BY line ASC)
        LOOP
            v_code := v_code || src.text;
        END LOOP;

        RETURN v_code;
    END get_code;

    -- Archiving
    PROCEDURE backup (p_name      IN plsql_archive.name%TYPE,
                      p_type      IN plsql_archive.type%TYPE,
                      p_owner     IN plsql_archive.owner%TYPE,
                      p_action    IN plsql_archive.action%TYPE,
                      p_ip        IN plsql_archive.IP%TYPE,
                      p_osuser    IN plsql_archive.OSUSER%TYPE,
                      p_err       IN plsql_archive.ERR%TYPE)
    IS
        r_rev   plsql_archive%ROWTYPE;
        v_type  plsql_archive.type%TYPE;
        p_new_src     plsql_archive.new_src%TYPE;
        oper       VARCHAR2 (32000);
        sql_text   ora_name_list_t;
        n          NUMBER;
        v_stmt     CLOB;
    BEGIN
        r_rev.name := p_name;
        r_rev.type := p_type;
        r_rev.owner := p_owner;
        r_rev.created := SYSDATE;
        r_rev.err := p_err;
        r_rev.ip := p_ip;
        r_rev.osuser := p_osuser;
        r_rev.id := seq_plsql_archive.nextval;     
        r_rev.action := p_action;
        
        v_type := r_rev.type;
        IF v_type = 'PACKAGE' THEN 
            v_type := 'PACKAGE_SPEC';
        END IF;
                
        BEGIN
            r_rev.old_src := DBMS_METADATA.get_ddl (REPLACE (v_type, ' ', '_'), r_rev.name, r_rev.owner);
        EXCEPTION
            WHEN OTHERS THEN
                r_rev.old_src := get_code (r_rev.name, r_rev.type);
                r_rev.err := SQLERRM ();
        END;
        
        -- ADD Thursday, September 20, 2018
        -- ToDo: Detect How to get new sql 
        -- DBMS_LOB.createtemporary (p_new_src, TRUE, DBMS_LOB.call);
        --                             oper := ora_sysevent;
        --                             n := ora_sql_txt (sql_text);
        --
        -- FOR i IN 1 .. n
        -- LOOP
        --     DBMS_LOB.writeappend (p_new_src, LENGTH (sql_text (i)), sql_text (i));
        -- END LOOP;
        --        
        -- r_rev.new_src := p_new_src;
        r_rev.new_src := r_rev.old_src;
        

        BEGIN
            SELECT status
              INTO r_rev.status
              FROM all_objects
             WHERE object_name = r_rev.name AND object_type = r_rev.type AND owner = r_rev.owner;
        EXCEPTION
            WHEN OTHERS THEN
                r_rev.err := r_rev.err || SQLERRM ();
        END;
        
        -- ToDo: To reduce the number of inserts, we can only keep the differences between the old and new sources.
        FOR i IN (  SELECT *
                      FROM plsql_archive
                     WHERE name = r_rev.name AND type = r_rev.type AND owner = r_rev.owner
                  ORDER BY created DESC)
        LOOP
            IF DBMS_LOB.compare (i.old_src, r_rev.old_src) = 0 THEN
                RETURN;
            END IF;

            EXIT;
        END LOOP;

        INSERT INTO plsql_archive VALUES r_rev;
    END backup;
END plsql_backup;
/