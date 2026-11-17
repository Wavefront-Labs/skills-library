---
id: computing-software.database-administration.mysql.upgrading-via-package-repositories-and-docker
name: upgrading-via-package-repositories-and-docker
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-apt-repository, mysql-yum-repository, package-upgrade, docker-mysql, mysql-upgrade, release-series]
level: practitioner
status: draft
description: "Upgrade MySQL with the official APT/Yum repositories (choosing LTS vs Innovation tracks) or Docker image tags, with pinning, backups and post-upgrade checks."
sources:
  - https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/
  - https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/
  - https://dev.mysql.com/doc/refman/8.4/en/upgrading.html
  - https://hub.docker.com/_/mysql
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Upgrading via APT / Yum repositories and Docker images

## Pick the series first
MySQL 8.4 is an LTS series; Innovation releases (9.x) get quarterly feature changes. Repositories have a separate channel per series: you upgrade *within* a series by `apt upgrade`; you change series by reconfiguring the repo. Read the series' upgrade path rules (LTS -> next LTS, skip limits) before switching.

## APT (Debian/Ubuntu)
```bash
# install the mysql-apt-config package from dev.mysql.com, then choose the series:
sudo dpkg-reconfigure mysql-apt-config        # select mysql-8.4-lts
sudo apt-get update
apt-cache policy mysql-server mysql-community-server   # confirm candidate comes from repo.mysql.com
sudo apt-get install --only-upgrade mysql-server
```
Pin to avoid accidental series jumps or distro packages taking over:
```
# /etc/apt/preferences.d/mysql
Package: mysql-*
Pin: origin repo.mysql.com
Pin-Priority: 1001
```

## Yum/DNF (RHEL family)
```bash
sudo dnf install https://dev.mysql.com/get/mysql84-community-release-el9-1.noarch.rpm   # check current file name on the downloads page
sudo dnf module disable mysql            # RHEL 8/9: disable the AppStream module so it does not shadow community packages
sudo dnf config-manager --disable mysql-innovation-community; sudo dnf config-manager --enable mysql-8.4-lts-community
sudo dnf upgrade mysql-community-server
```
`dnf repolist enabled | grep mysql` should show exactly one server series.

## Procedure (either)
1. Full backup and, for majors, `util.checkForServerUpgrade()` from MySQL Shell.
2. Upgrade replicas first, then switch over and upgrade the old source.
3. The package restarts mysqld; the server upgrades the data dictionary and system tables itself at startup (no `mysql_upgrade` since 8.0.16). Watch the error log until `ready for connections`.
4. Check: `SELECT VERSION();`, error log warnings, application smoke tests.

## Docker
```bash
docker pull mysql:8.4.6             # pin a full version tag, not 'latest' or just '8'
docker stop mysql && docker rm mysql
docker run -d --name mysql -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/root ... mysql:8.4.6
docker logs -f mysql                 # in-place upgrade runs on start against the existing volume
```
`latest` and floating tags can jump series on the next pull and an in-place downgrade is not supported: back up the volume first.

## Gotchas
- Downgrades within LTS are supported only in specific cases; across series they need logical dump/restore. Treat every upgrade as one-way and keep the backup.
- Mixing distro packages (`default-mysql-server`, MariaDB) with repo packages causes file conflicts; remove one cleanly.
- Unattended-upgrades/dnf-automatic can upgrade MySQL and restart it in business hours; exclude it from automatic updates.
