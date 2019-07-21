## Source Control for Oracle ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Connect Oracle Database to your existing Git source control system

## Installation

### Requirements
* GNU/ Linux
* Oracle Client For [cx_Oracle 7](https://oracle.github.io/python-cx_Oracle/) From [Documentation](https://cx-oracle.readthedocs.io/en/latest/installation.html#install-oracle-client)
* Git Version 2.9.5


## Install RPM In Operating environment
```
$ cd ~
$ sudo mkdir ~/cfgOper
$ sudo mkdir ~/logOper
$ sudo mkdir /var/log/logOper/
$ sudo ln -s /var/log/logOper/ ~/logOper
$ sudo mkdir _rpmOper
$ sudo mkdir scripts
-- Upload rpm file to _rpmOper directory
$ cd _rpmOper
$ sudo rpm -ivh [rpm package name]
```


## Uninstall RPM
```
$ rpm -e SyncGitDB-2.0-1.el6.noarch
```

## BUILD RPM
```
$ cd /root/PyGitSyncOrcl/
$ rm -rf build/
$ rm -rf dist/
$ pyinstaller SyncGitDB.py
$ mv dist/SyncGitDB/ dist/SyncGitDB-2.0
$ cd dist
$ tar czvf SyncGitDB-2.0.tar.gz SyncGitDB-2.0/
$ rm -rf /root/rpmbuild/SOURCES/SyncGitDB-2.0.tar.gz
$ rm -rf /root/bob/rpmbuild/SOURCES/SyncGitDB-2.0.tar.gz
$ cp SyncGitDB-2.0.tar.gz /root/rpmbuild/SOURCES/
$ cp SyncGitDB-2.0.tar.gz /root/bob/rpmbuild/SOURCES/
$ rm -rf /root/rpmbuild/BUILD/*
$ rm -rf /root/rpmbuild/BUILDROOT/*
$ rm -rf /root/rpmbuild/RPMS/*
$ rm -rf /root/bob/rpmbuild/BUILD/*
$ rm -rf /root/bob/rpmbuild/BUILDROOT/*
$ rm -rf /root/bob/rpmbuild/RPMS/*
$ rpmbuild -bb /root/bob/rpmbuild/SPECS/SyncGitDB.spec
$ cd /root/rpmbuild/RPMS/noarch

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPL Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html/)
