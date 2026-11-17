---
id: computing-software.systems-network-administration.apache-tomcat.catalina-home-base-setenv
name: catalina-home-base-setenv
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, running, catalina-home, catalina-base, setenv, catalina-opts, java-opts, catalina-pid, startup-shutdown]
level: intro
status: docs-checked
description: "Start and stop Tomcat 10.1 with the standard scripts and set environment through setenv.sh: JRE 11+, CATALINA_HOME and BASE, CATALINA_OPTS vs JAVA_OPTS, CATALINA_PID."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/RUNNING.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Tomcat 10.1

Needs a Java SE runtime 11 or later (a JDK also works).

| Variable | Rule |
|---|---|
| `CATALINA_HOME` | Required; the binary distribution root (scripts may detect it) |
| `CATALINA_BASE` | Optional; active config root, defaults to HOME; cannot be set in setenv |
| `JRE_HOME` / `JAVA_HOME` | One needed; JRE_HOME wins if both; JDK gives extra startup options |
| `CATALINA_OPTS` | Options for the Tomcat start java command; put memory limits here |
| `JAVA_OPTS` | Used by start, stop and other commands; keep memory limits out |
| `CATALINA_PID` | Unix PID file; blocks duplicate starts and enables forced kill |

Others are documented in comments at the top of `catalina.sh`/`catalina.bat`.

Commands:
```
$CATALINA_HOME/bin/startup.sh      # or catalina.sh start
$CATALINA_HOME/bin/shutdown.sh     # or catalina.sh stop
```
Windows: `startup.bat`, `shutdown.bat`, `catalina.bat start|stop`. Default apps appear at `http://localhost:8080/`.

`setenv` (not present by default) lives in `CATALINA_BASE/bin` or `CATALINA_HOME/bin`; BASE wins. It may set everything except HOME and BASE:
```
# $CATALINA_BASE/bin/setenv.sh
CATALINA_OPTS="-Xms512m -Xmx2g"
CATALINA_PID="/path/to/run/tomcat.pid"
```
It applies only when you use the standard scripts; a Windows service ignores it.

Verify: the default web applications answer at `http://localhost:8080/`, and `ps` shows the Java process with your `-Xmx`.

## Checked

2026-11-04. Read the Tomcat 10.1 RUNNING.txt: confirmed Java SE 11 or later, CATALINA_HOME and CATALINA_BASE semantics, JRE_HOME over JAVA_HOME, CATALINA_OPTS versus JAVA_OPTS (no memory limits in JAVA_OPTS), CATALINA_PID benefits, setenv location and precedence, the HOME and BASE exclusion, the Windows service note, and the start and stop commands. Softened the verify step.

Method: documentation only; no commands were run.
