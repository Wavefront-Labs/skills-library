---
id: computing-software.database-administration.sql-server.sql-server-on-linux-and-containers
name: sql-server-on-linux-and-containers
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, mssql-conf, sql-server-linux, docker, containers, kubernetes, sqlcmd]
level: practitioner
status: docs-checked
description: "Install and configure SQL Server on Linux with mssql-conf, run it in Docker with persistent volumes, and handle the differences from Windows."
sources:
  - https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-configure-mssql-conf
  - https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker
  - https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-performance-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server on Linux and containers

## Install (RHEL / Ubuntu)
Add the Microsoft repository for your distro, install `mssql-server`, then:
```bash
sudo /opt/mssql/bin/mssql-conf setup          # edition, SA password, EULA
systemctl status mssql-server
```

## mssql-conf replaces Configuration Manager
```bash
sudo /opt/mssql/bin/mssql-conf set memory.memorylimitmb 28672   # default is 80% of RAM
sudo /opt/mssql/bin/mssql-conf set network.tcpport 1433
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultdatadir /var/opt/mssql/data
sudo /opt/mssql/bin/mssql-conf set filelocation.defaultbackupdir /var/opt/mssql/backup
sudo /opt/mssql/bin/mssql-conf set sqlagent.enabled true
sudo /opt/mssql/bin/mssql-conf set hadr.hadrenabled 1
sudo /opt/mssql/bin/mssql-conf traceflag 3226 on
sudo systemctl restart mssql-server
```
`mssql-conf` writes its settings to the `mssql.conf` file; the error log is `/var/opt/mssql/log/errorlog`.
`memory.memorylimitmb` caps the whole process; `max server memory` still applies inside it.

## Host tuning
`tuned-adm profile mssql`, XFS or ext4 (both supported) mounted `noatime`, and `vm.swappiness`
set as the performance best-practices page describes.

## Docker
```bash
docker run -d --name sql1 -h sql1 \
  -e ACCEPT_EULA=Y -e MSSQL_SA_PASSWORD='<SECRET>' -e MSSQL_PID=Developer \

  -p 1433:1433 -v sqldata:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2022-latest
docker exec -it sql1 /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<SECRET>' -C
```
- Always mount `/var/opt/mssql` on a volume, or the data dies with the container.
- Pin a specific version tag in production, not `latest`.

## Differences from Windows
- Windows authentication uses Active Directory with a keytab (see `adutil` and `mssql-conf setup-ad-keytab`).

## Verify
`SELECT @@VERSION;`

## Checked
2026-10-28. Confirmed against the mssql-conf, Docker quickstart and Linux performance best-practices pages: mssql-conf setup, memory.memorylimitmb (default 80% of physical memory; max server memory cannot exceed it), network.tcpport, filelocation.defaultdatadir and defaultbackupdir, sqlagent.enabled, hadr.hadrenabled, traceflag, the error log under /var/opt/mssql/log, mssql-tools18 in the container images, MSSQL_PID, tuned-adm profile mssql, noatime, vm.swappiness, XFS and ext4 supported, Windows authentication via adutil and a keytab.
Removed unconfirmed claims: MSSQL_MEMORY_LIMIT_MB and MSSQL_AGENT_ENABLED container variables, mssql uid 10001, the example CU tag, the Kubernetes operator note, FILESTREAM and Pacemaker lines, forward-slash note, data directory ownership and THP/NUMA wording, the sys.dm_os_host_info query.
Method: documentation only; no commands were run.
