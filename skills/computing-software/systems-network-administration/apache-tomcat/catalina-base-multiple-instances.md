---
id: computing-software.systems-network-administration.apache-tomcat.catalina-base-multiple-instances
name: catalina-base-multiple-instances
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, catalina-base, multiple-instances, instance-layout, shared-install, lib-directory, windows-service]
level: practitioner
status: docs-checked
description: "Run several Tomcat 10.1 instances from one install with separate CATALINA_BASE directories: subdirectories, CATALINA_HOME contents, lib search order, a Windows service each."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/RUNNING.txt
  - https://tomcat.apache.org/tomcat-10.1-doc/windows-service-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple instances with CATALINA_BASE

Share one binary install (`CATALINA_HOME`), give each instance its own `CATALINA_BASE`:

| In CATALINA_BASE | Contents |
|---|---|
| `bin` | only `setenv.sh/.bat` and optionally `tomcat-juli.jar` |
| `conf` | all config incl. `server.xml`, `web.xml` (copy from HOME) |
| `lib` | per-instance libraries, e.g. JDBC drivers |
| `logs`, `work`, `temp` | runtime output, JSP work dirs, java.io.tmpdir |
| `webapps` | auto-deployed apps |

CATALINA_HOME keeps `bin` (scripts) and `lib`. `setenv` and `tomcat-juli.jar` are used from HOME only if absent in BASE. Both `lib` directories join the common classpath, BASE first; keep standard libs in HOME and extras in BASE.

Steps:
1. `mkdir -p /path/to/instance1/{conf,logs,temp,webapps,work,lib,bin}` and copy `conf/*` from HOME.
2. Edit `conf/server.xml`: give each instance unique shutdown port and connector ports (or use `portOffset` on `<Server>`).
3. Start: `CATALINA_BASE=/path/to/instance1 $CATALINA_HOME/bin/catalina.sh start`.

Windows services, one per instance:
```bat
set CATALINA_HOME=\path\to\tomcat_10
set CATALINA_BASE=\path\to\tomcat_10\instances\instance1
service.bat install instance1
set CATALINA_BASE=\path\to\tomcat_10\instances\instance2
service.bat install instance2
```
Configure with `tomcat10w //ES//instance1`.

Config files can use `${catalina.home}` and `${catalina.base}`.

Verify: each instance answers on its own port and writes to its own `logs/`.

## Checked

2026-11-04. Read the Tomcat 10.1 RUNNING.txt (multiple instances section) and Windows Service How-To: confirmed the CATALINA_BASE and CATALINA_HOME directory split, setenv and tomcat-juli.jar fallback, BASE-first library order, ${catalina.home} and ${catalina.base} in XML, the per-instance service.bat install sequence and tomcat10w //ES//instance1, and portOffset on the Server page. Nothing removed.

Method: documentation only; no commands were run.
