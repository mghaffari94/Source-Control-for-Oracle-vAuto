#!/bin/bash
source $HOME/.bash_profile
timestamp=`date "+%Y-%m-%d,%H:%M:%S"`
git_repo_local_dir="/home/ghaffari/GitDatabaseOper"
git_url="source.example.com/mahdi.gh/GitDatabaseOper"
config_file="/home/ghaffari/cfgOper/configFile.ini"
log_dir="/home/ghaffari/logOper"

/opt/syncgitdb/SyncGitDB $git_repo_local_dir @$git_url $config_file $log_dir > $log_dir/scriptLog-"$timestamp".log

exit