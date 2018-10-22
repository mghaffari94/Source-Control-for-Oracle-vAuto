#!/bin/bash                                                                                                                             
source $HOME/.bash_profile                                                                                                              
                                                                                                                                        
PATH_SCRIPT_LOG=/home/ghaffari/logOper/                                                                                                 
PATHERN_LOG="scriptLog-*"                                                                                                               
PATH_PY_LOG=/home/ghaffari/logOper/                                                                                                     
PATHERN_PY_LOG="20*"                                                                                                                    
PATH_ORCL_LOG=/home/ghaffari/logOper/ORA/                                                                                               
PATHERN_ORCL_LOG="20*"                                                                                                                  
/usr/bin/find $PATH_SCRIPT_LOG -name $PATHERN_LOG -mtime +2 -exec /usr/bin/rm -f {} \;                                                  
/usr/bin/find $PATH_PY_LOG -name $PATHERN_PY_LOG -mtime +2 -exec /usr/bin/rm -rf {} \;                                                  
/usr/bin/find $PATH_ORCL_LOG -name $PATHERN_ORCL_LOG -mtime +2 -exec /usr/bin/rm -rf {} \;