#!/usr/bin/env python
# -*- coding: windows-1256 -*-
import argparse
import traceback
import cx_Oracle
import logging
import os
import re
import shlex
import subprocess
import sys
from configparser import ConfigParser
import dbHelper
from Logger import Logger

prs = argparse.ArgumentParser(description='usage')
prs.add_argument('-b', action='store_true', help='git init --bare')
prs.add_argument('git_dir', action='store', help='To make and git init directory')
prs.add_argument('rmt_repo', action='store', help='URL Remote Repository')
prs.add_argument('cfg_file', action='store', help='configFile.ini Path')
prs.add_argument('log_dir', action='store', help='Log Directory Path')
args = prs.parse_args()

__level__ = logging.INFO
__confiFileName__ = os.path.abspath(args.cfg_file)
__LOGDIR__ = os.path.abspath(args.log_dir)

logMain = Logger(filename="main_init", level=__level__,
                 dirname="File-" + os.path.basename(__file__), rootdir=__LOGDIR__)


def NewMaxID():
    logNewMaxID = Logger(filename="__init__", level=__level__,
                         dirname="File-" + os.path.basename(
                             __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)
    try:
        # No commit as you don-t need to commit DDL.
        res = cursor.execFetchOne("SELECT MAX(ID)"
                                  "FROM USSD.PLSQL_ARCHIVE", __LOGDIR__ + '/ORA')

        regex = r"([(])"
        regex2 = r"([,)])"
        matches = re.sub(regex, '\n', str(res))
        matches2 = re.sub(regex2, '\n', matches)
        V_REC = matches2.replace("\n", "")

        config = ConfigParser()
        config.read(__confiFileName__)
        config['MAX_ID']['VALUE'] = str(V_REC)

        try:
            with open(__confiFileName__, 'w', encoding='windows-1256') as configfile:  # save
                config.write(configfile)
        except EnvironmentError as ex:  # parent of IOError, OSError *and* WindowsError where available
            logNewMaxID.warning("Error in create" + __confiFileName__ + " -> NewMaxID()")
            logNewMaxID.error("Error Massage: " + str(ex))
        except:
            logNewMaxID.error("Unexpected error:", sys.exc_info()[0])

    # Ensure that we always disconnect from the database to avoid
    # ORA-00018: Maximum number of sessions exceeded.
    except cx_Oracle.DatabaseError as ex:
        logNewMaxID.warning("General Error Database in -> NewMaxID()")
        logNewMaxID.error("Error Massage: " + str(ex))

    except:
        logNewMaxID.error("Unexpected error:", sys.exc_info()[0])


def loadNonClob():
    logloadNonClob = Logger(filename="__init__", level=__level__,
                            dirname="File-" + os.path.basename(
                                __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

    configINI = ConfigParser()
    configINI.read(__confiFileName__)
    V_MAX_ID = configINI.get('MAX_ID', 'VALUE')

    sql = "SELECT NAME, TYPE, OWNER, CREATED, STATUS, ERR, " \
          "OSUSER, IP, ACTION, OLD_SRC, NEW_SRC, ID " \
          "FROM USSD.PLSQL_ARCHIVE " \
          "WHERE NAME NOT LIKE '%SYS_%'" \
          "AND ID > :TEST"

    try:
        # No commit as you don-t need to commit DDL.
        cursor.execArgs(sql, V_MAX_ID, __LOGDIR__ + '/ORA')
        #
        records = cursor.fetchall()

        global Vn_NAME
        Vn_NAME = [record[0] for record in records] or ''

        global Vn_TYPE
        Vn_TYPE = [record[1] for record in records] or ''

        global Vn_OWNER
        Vn_OWNER = [record[2] for record in records] or ''

        global Vn_CREATED
        Vn_CREATED = [record[3] for record in records] or ''

        global Vn_STATUS
        Vn_STATUS = [record[4] for record in records] or ''

        global Vn_ERR
        Vn_ERR = [record[5] for record in records] or ''

        global Vn_OSUSER
        Vn_OSUSER = [record[6] for record in records] or ''

        global Vn_IP
        Vn_IP = [record[7] for record in records] or ''

        global Vn_ACTION
        Vn_ACTION = [record[8] for record in records] or ''

        global Vn_OLD_SRC
        Vn_OLD_SRC = [record[9] for record in records] or ''

        global Vn_NEW_SRC
        Vn_NEW_SRC = [record[10] for record in records] or ''

        global Vn_ID
        Vn_ID = [record[11] for record in records] or ''

    # Ensure that we always disconnect from the database to avoid
    # ORA-00018: Maximum number of sessions exceeded.
    except cx_Oracle.DatabaseError as ex:
        logloadNonClob.warning("General Error Database in -> NewMaxID()")
        logloadNonClob.error("Error Massage: " + str(ex))
    except:
        logloadNonClob.error("Unexpected error:", sys.exc_info()[0])


def loadCLOB():
    global Vx_OLD_SRC
    Vx_OLD_SRC = []
    # Check if LOB data is empty using cx_Oracle in Python.
    for i in Vn_OLD_SRC:
        if str(type(i)) == "<class 'cx_Oracle.LOB'>":
            Vx_OLD_SRC.append(i)
        else:
            Vx_OLD_SRC.append('')

    # Check if LOB data is empty using cx_Oracle in Python.
    global Vy_NEW_SRC
    Vy_NEW_SRC = []
    for j in Vn_NEW_SRC:
        if str(type(j)) == "<class 'cx_Oracle.LOB'>":
            Vy_NEW_SRC.append(j)
        else:
            Vy_NEW_SRC.append('')


def diffNewOld():
    logdiffNewOld = Logger(filename="__init__", level=__level__,
                           dirname="File-" + os.path.basename(
                               __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

    listfor = zip(
        Vx_OLD_SRC,
        Vy_NEW_SRC, Vn_NAME, Vn_TYPE, Vn_ID, Vn_OSUSER,
        Vn_IP, Vn_STATUS, Vn_ACTION, Vn_CREATED, Vn_OWNER)

    for Vi_OLD_SRC, Vi_NEW_SRC, Vi_NAME, Vj_TYPE, Vi_ID, Vi_OSUSER, Vj_IP, \
        Vi_STATUS, Vj_ACTION, Vi_CREATED, Vj_OWNER in listfor:

        if (str(type(Vi_OLD_SRC)) == "<class 'cx_Oracle.LOB'>" and
            str(type(Vi_NEW_SRC)) == "<class 'cx_Oracle.LOB'>") \
                or \
                (str(type(Vi_OLD_SRC)) == "<class 'str'>" and
                 str(type(Vi_NEW_SRC)) == "<class 'cx_Oracle.LOB'>") and Vj_ACTION != "DROP":

            regex = r"\\n"
            regex2 = r"(^[b][\"])"
            regex3 = r"[\"]$"
            regex4 = r"(^[b][\'])"
            regex5 = r"[\']$"

            # To write to a file:
            Vi_NEW_SRC = Vi_NEW_SRC.read()
            V_NEW_SRC_utf8 = Vi_NEW_SRC.rstrip('\t\r\n\0').encode('utf-8').decode('cp1256')
            #
            matches = re.sub(regex, '\n', str(V_NEW_SRC_utf8))
            matches2 = re.sub(regex2, '', str(matches))
            matches3 = re.sub(regex3, '', str(matches2))
            matches4 = re.sub(regex4, '', str(matches3))
            matches5 = re.sub(regex5, '', str(matches4))

            # In Production Mode
            try:
                with open(dirpath + Vi_NAME + "-" + Vj_TYPE + ".txt", "w", encoding='windows-1256') as f:
                    f.write(str(matches5))
            except EnvironmentError as ex:
                # parent of IOError, OSError *and* WindowsError where available
                logdiffNewOld.warning("Error in create" + __confiFileName__ + " -> NewMaxID()")
                logdiffNewOld.error("Error Massage: " + str(ex))
            except:
                logdiffNewOld.error("Unexpected error:", sys.exc_info()[0])

            NewMaxID()

            fileN = Vi_NAME + "-" + Vj_TYPE + ".txt"
            gitAdd(fileN, dirpath)

            comment = 'This commit by: ' + str(Vi_OSUSER) + ' from IP: ' + str(Vj_IP) + ' with status: ' \
                      + str(Vi_STATUS) + ' in Database' + ' and user action is: ' + str(Vj_ACTION) \
                      + ' in Time: ' + str(Vi_CREATED) + ' and owner object is: ' + str(Vj_OWNER)

            gitConfigUser(str(Vi_OSUSER), str(Vi_OSUSER) + "@780.ir", dirpath)
            # Date Format Option in Git => {relative,local,default,iso,rfc}
            gitConfigDateFormat("local", dirpath)
            gitCommit(fileN, dirpath, comment)

        else:
            # In Production Mode
            try:
                with open(dirpath + Vi_NAME + "-" + Vj_TYPE + ".txt", "w", encoding='windows-1256') as f:
                    f.write("DROP " + Vj_TYPE + " " + Vi_NAME)
            except EnvironmentError as ex:
                # parent of IOError, OSError *and* WindowsError where available
                logdiffNewOld.warning("Error in create" + __confiFileName__ + " -> NewMaxID()")
                logdiffNewOld.error("Error Massage: " + str(ex))
            except:
                logdiffNewOld.error("Unexpected error:", sys.exc_info()[0])

            NewMaxID()

            fileN = Vi_NAME + "-" + Vj_TYPE + ".txt"
            gitAdd(fileN, dirpath)

            comment = 'This commit by: ' + str(Vi_OSUSER) + ' from IP: ' + str(Vj_IP) + ' with status: ' \
                      + 'VALID' + ' in Database' + ' and user action is: ' + str(Vj_ACTION) \
                      + ' in Time: ' + str(Vi_CREATED) + ' and owner object is: ' + str(Vj_OWNER)

            gitConfigUser(str(Vi_OSUSER), str(Vi_OSUSER) + "@780.ir", dirpath)
            # Date Format Option in Git => {relative,local,default,iso,rfc}
            gitConfigDateFormat("local", dirpath)
            gitCommit(fileN, dirpath, comment)

    gitPush(url_remote_repo, dirpath)


def gitClone(url, repoDir):
    logGitClone = Logger(filename="__init__", level=__level__,
                         dirname="File-" + os.path.basename(
                             __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

    try:
        if not os.path.isdir(repoDir + ".git"):
            cmdGitClone = ['git', 'clone', url, repoDir]
            p = subprocess.Popen(cmdGitClone, cwd=os.getcwd())
            p.wait()
    except:
        logGitClone.error("General Error in -> gitClone()" + sys.exc_info()[0])


def gitInit(repoDir):
    logGitInit = Logger(filename="__init__", level=__level__,
                        dirname="File-" + os.path.basename(
                            __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

    if args.__dict__.get('b'):
        # bare repos store git revision history of your repo in the root folder
        cmdGitClone = ['git', 'init', '--bare']
        p = subprocess.Popen(cmdGitClone, cwd=repoDir)
        p.wait()
    else:
        # local repository
        cmd = ['git', 'init']
        p = subprocess.Popen(cmd, cwd=repoDir)
        p.wait()
        # Make .gitignore
        if not os.path.isfile(dirpath + '.gitignore'):
            try:
                f = open(dirpath + '.gitignore', 'w')
                f.write('')
                f.close()
            except EnvironmentError as ex:  # parent of IOError, OSError *and* WindowsError where available
                logGitInit.warning("Error in create" + __confiFileName__ + " -> NewMaxID()")
                logGitInit.error("Error Massage: " + str(ex))
            except:
                logGitInit.error("Unexpected error:", sys.exc_info()[0])


def gitAdd(fileName, repoDir):
    cmd = ['git', 'add', fileName]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()


# ToDo: Use this Function.
def runCommand(command):
    logRunCommand = Logger(filename="__init__", level=__level__,
                           dirname="File-" + os.path.basename(
                               __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            logRunCommand.info(output.strip())
    rc = process.poll()
    return rc


def gitConfigUser(userName, email, repoDir):
    cmd = ['git', 'config', '--global', 'user.name', userName]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()

    cmd = ['git', 'config', '--global', 'user.email', email]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()


def gitConfigDateFormat(dateFormat, repoDir):
    cmd = ['git', 'config', '--global', 'log.date', dateFormat]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()


def gitCommit(fileName, repoDir, message):
    cmd = ['git', 'commit', fileName,
           '-m', message]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()


def gitPush(url, repoDir):
    cmd = ['git', 'push', url]
    p = subprocess.Popen(cmd, cwd=repoDir)
    p.wait()


def gitCashExit():
    cmd = ['git', 'credential-cache', 'exit']
    p = subprocess.Popen(cmd)
    p.wait()


def loadConfigFile():
    logLoadConfigFile = Logger(filename="__init__", level=__level__,
                               dirname="File-" + os.path.basename(
                                   __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)
    try:
        configINI = ConfigParser()
        configINI.read(__confiFileName__)

        global V_DB_USERNAME
        global V_DB_PASSWORD
        global V_DB_HOST
        global V_DB_PORT
        global V_DB_SN
        global V_GIT_USERNAME
        global V_GIT_PASSWORD
        global V_DB_DSN

        V_DB_USERNAME = configINI.get('ORACLE_CONNECTION', 'dbUsername')
        V_DB_PASSWORD = configINI.get('ORACLE_CONNECTION', 'dbPassword')
        V_DB_DSN = configINI.get('ORACLE_CONNECTION', 'dbDSN')

        V_GIT_USERNAME = configINI.get('GIT_CONF', 'gitUsername')
        V_GIT_PASSWORD = configINI.get('GIT_CONF', 'gitPassword')
    except:
        logLoadConfigFile.error("Unexpected error:", sys.exc_info()[0])


try:

    loadConfigFile()
    os.environ["PYTHONIOENCODING"] = "windows-1256"
    connection = None
    if __name__ == "__main__":

        logMain = Logger(filename="__init__", level=__level__,
                         dirname="File-" + os.path.basename(
                             __file__) + "-Func-" + sys._getframe().f_code.co_name, rootdir=__LOGDIR__)

        try:
            # create instances of the dbHelper connection and cursor
            connection = dbHelper.Connection(V_DB_USERNAME, V_DB_PASSWORD, V_DB_DSN, __LOGDIR__ + '/ORA')
            cursor = connection.cursor()

            # demonstrate that the dbHelper connection and cursor are being used
            try:
                # No commit as you don-t need to commit DDL.
                V_NLS_LANGUAGE, = cursor.execFetchOne("SELECT VALUE AS NLS_LANGUAGE "
                                                      "FROM V$NLS_PARAMETERS "
                                                      "WHERE PARAMETER = ('NLS_LANGUAGE')"
                                                      ,
                                                      __LOGDIR__ + '/ORA')

                V_NLS_TERRITORY, = cursor.execFetchOne("SELECT VALUE AS NLS_TERRITORY "
                                                       "FROM V$NLS_PARAMETERS "
                                                       "WHERE PARAMETER = ('NLS_TERRITORY')"
                                                       ,
                                                       __LOGDIR__ + '/ORA')

                V_NLS_CHARACTERSET, = cursor.execFetchOne("SELECT VALUE AS NLS_CHARACTERSET "
                                                          "FROM V$NLS_PARAMETERS WHERE "
                                                          "PARAMETER = ('NLS_CHARACTERSET')"
                                                          ,
                                                          __LOGDIR__ + '/ORA')

                if V_NLS_LANGUAGE and V_NLS_TERRITORY and V_NLS_CHARACTERSET is not None:
                    # export NLS_LANG=<language>_<territory>.<character set>
                    os.environ["NLS_LANG"] = V_NLS_LANGUAGE + "." + V_NLS_TERRITORY + "." + V_NLS_CHARACTERSET

                    dirpath = os.path.abspath(args.git_dir) + "/"
                    url_remote_repo = "https://" + V_GIT_USERNAME + ":" + V_GIT_PASSWORD + args.rmt_repo + ".git"

                    gitCashExit()
                    gitClone(url_remote_repo, dirpath)
                    gitInit(dirpath)
                    loadNonClob()
                    loadCLOB()
                    diffNewOld()

            except Exception as e:
                logMain.error(traceback.format_exc())
            except:
                logMain.error("Unexpected error:", sys.exc_info()[0])

            # Ensure that we always disconnect from the database to avoid
            # ORA-00018: Maximum number of sessions exceeded.

        except cx_Oracle.DatabaseError as ex:
            logMain.warning("General Error Database in -> NewMaxID()")
            logMain.error("Error Massage: " + str(ex))
        except:
            logMain.error("Unexpected error:", sys.exc_info()[0])

except RuntimeError as e:
    logMain.error(sys.stderr.write("ERROR: %s\n" % e))

except:
    logMain.error("Unexpected error:", sys.exc_info()[0])
