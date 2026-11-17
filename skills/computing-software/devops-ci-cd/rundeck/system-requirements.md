---
id: computing-software.devops-ci-cd.rundeck.system-requirements
name: system-requirements
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, system-requirements, java-17, h2-database, network-ports]
level: intro
status: docs-checked
description: "Check Rundeck server prerequisites: OS, memory and CPU sizing, Java 17, supported databases, network ports, and why H2 is not for production."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/install/system-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From the requirements page:

- OS: Red Hat Enterprise 8+, Oracle Linux 8+, Amazon Linux 2023; Ubuntu 22.04.3+, Debian 12+; Windows Server 2019+.
- Sizing: Runbook Automation Self-Hosted recommended 32GB RAM (24GB JVM heap), 8 CPUs; minimum 16GB (12GB heap), 4 CPUs. Open source minimum 8GB (4GB heap), 2 CPUs.
- Java: Rundeck 6.0.0 needs Java 17 as the minimum runtime, supported through Java 25. Azul Zulu OpenJDK is what it is built and tested with. Check with `java -version` and set `JAVA_HOME` if needed.
- Databases: MariaDB 10.11.6+, MySQL 8.0.35+ or 8.4+, PostgreSQL 15.5+, SQL Server 2022, Oracle 19c+.
- Ports: 4440 (http), 4443 (https), 22 for SSH to Linux nodes, 5985 (Windows machines over http) and 5986 (Windows machines over https). Check free ports with `netstat -an | egrep '4440|4443'`.
- Run as a dedicated user such as `rundeck`; root is not required or recommended (use sudo if needed).
- Browser: current Firefox or Chrome.

Gotcha: the default embedded H2 database is not safe for production. An unclean shutdown can truncate or corrupt data. Use MariaDB/MySQL or PostgreSQL, on a host with enough capacity.

Clients must allow the Rundeck user to SSH with public-key authentication and no password prompt.

## Checked

2026-11-04: operating systems, sizing, Java versions and distribution, databases, ports, the netstat check, dedicated user, browsers, the H2 warning and the SSH key requirement confirmed against the Rundeck Instance System Requirements page. Renamed the Enterprise column to Runbook Automation Self-Hosted and described the Windows ports as the page does.

Method: documentation only; no commands were run.
