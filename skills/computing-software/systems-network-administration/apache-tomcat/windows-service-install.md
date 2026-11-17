---
id: computing-software.systems-network-administration.apache-tomcat.windows-service-install
name: windows-service-install
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, windows-service, service-bat, tomcat10w, commons-daemon, procrun, install-service, uninstall-service]
level: practitioner
status: docs-checked
description: "Install, update, start, stop and remove Tomcat 10.1 as a Windows service with service.bat and tomcat10.exe //IS// //US// //DS// //ES// //SS// //TS//, plus the tomcat10w monitor."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/windows-service-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows service

Run from an elevated prompt.
```bat
service.bat install            REM service name Tomcat10
service.bat install MyService
service.bat install MyService --rename
```
With a non-default name, `tomcat10.exe` and `tomcat10w.exe` may be renamed to match; use `--rename`. Administrator privileges are required (UAC prompts when `Tomcat10.exe` is launched). `PR_*` variables for the installer must be set globally in the OS or from an elevated launch.

Direct procrun directives (`tomcat10.exe`):

| Directive | Action |
|---|---|
| `//IS//Name` | Install |
| `//US//Name` | Update parameters |
| `//DS//Name` | Delete (stops the service first if running) |
| `//ES//Name` | Start the service (with `tomcat10w`: open the config GUI, the default) |
| `//SS//Name` | Stop |
| `//TS//Name` | Run in console mode (Ctrl+C or Ctrl+Break stops) |

```bat
tomcat10 //IS//Tomcat10 --DisplayName="Apache Tomcat 10" ^
  --Install="\path\to\Tomcat\bin\tomcat10.exe" --Jvm=auto ^
  --StartMode=jvm --StopMode=jvm ^
  --StartClass=org.apache.catalina.startup.Bootstrap --StartParams=start ^
  --StopClass=org.apache.catalina.startup.Bootstrap --StopParams=stop
tomcat10 //US//Tomcat10 --Startup=auto
```

Notes:
- Service parameters are listed in `computing-software.systems-network-administration.apache-tomcat.windows-service-parameters`.
- Multiple instances: set `CATALINA_HOME` to the installation and `CATALINA_BASE` to the instance folder, then run `service.bat install <service name>` (see `computing-software.systems-network-administration.apache-tomcat.catalina-base-multiple-instances`).

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Windows Service how-to (directives, installing, updating, removing, debugging, multiple instances). Reworded rename, //DS, //ES and //TS; removed the tools.jar and setenv.bat claims and the generic verify line.

Method: documentation only; no commands were run.
