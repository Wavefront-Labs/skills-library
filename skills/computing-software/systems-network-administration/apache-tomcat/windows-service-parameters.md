---
id: computing-software.systems-network-administration.apache-tomcat.windows-service-parameters
name: windows-service-parameters
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, windows-service, procrun, jvmoptions, jvmms, jvmmx, logpath, stdoutput, serviceuser, startup-mode]
level: practitioner
status: docs-checked
description: "Tune a Tomcat 10.1 Windows service: --Startup, --JvmMs/--JvmMx/--JvmSs, ++JvmOptions with # separators, --LogPath, --StdOutput/--StdError, --ServiceUser and PR_ variables."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/windows-service-howto.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows service parameters

Set with `tomcat10 //US//ServiceName --Name=value`. Prefix `++` appends to a multi-value parameter. Any parameter can also come from a `PR_<Name>` environment variable, which wins.

| Parameter | Default | Meaning |
|---|---|---|
| `--Startup` | manual | `auto` or `manual` |
| `--StartMode` / `--StopMode` | | `jvm`, `Java` or `exe` |
| `--Jvm` | auto | `auto` (find the JVM from the Windows registry) or the full path to `jvm.dll` |
| `--JavaHome` | JAVA_HOME | Override |
| `++JvmOptions` | `-Xrs` | `-D`/`-X` options separated by `#` or `;` (not in `exe` mode) |
| `++JvmOptions9` | | Only on Java 9+ |
| `--JvmMs` / `--JvmMx` | | Initial / maximum memory pool size in MiB (not used in `exe` mode) |
| `--JvmSs` | | Thread stack size in KiB (not used in `exe` mode) |
| `--LogPath` | `%SystemRoot%\System32\LogFiles\Apache` | Log dir |
| `--LogPrefix` | commons-daemon | |
| `--LogLevel` | Info | Error, Info, Warn, Debug |
| `--StdOutput` / `--StdError` | | File path, or `auto` for dated `service-stdout/stderr` files in LogPath |
| `--ServiceUser` / `--ServicePassword` | | Account the service runs as, in the form `DomainName\UserName`, `.\UserName` for the built-in domain, or `LocalSystem` |

```bat
tomcat10 //US//Tomcat10 --JvmMs=512 --JvmMx=2048 --JvmSs=1024 ^
  ++JvmOptions="-Dcatalina.home=\path\to\Tomcat#-Dfile.encoding=UTF-8"
tomcat10 //US//Tomcat10 --StdOutput=auto --StdError=auto --LogPath="\path\to\logs"
```

Other parameters on the page include `--Classpath`, `++Environment`, `--StopTimeout`, `--PidFile` and `--LogJniMessages`.

## Checked

2026-11-04. Confirmed against the Tomcat 10.1 Windows Service how-to (Command line parameters). Tightened the JVM, memory and ServiceUser rows; removed the low-privilege and restart advice and the generic verify line.

Method: documentation only; no commands were run.
