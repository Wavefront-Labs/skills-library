---
id: computing-software.devops-ci-cd.rundeck.start-stop-rundeckd
name: start-stop-rundeckd
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, rundeckd, java-home, init-script, service-control]
level: intro
status: docs-checked
description: "Start, stop and check the Rundeck server with the rundeckd control script for RPM, DEB and launcher installs, and choose which Java it uses."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/startup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The control script takes `rundeckd [start|stop|restart|condrestart|status]`.

RPM and DEB installs put it at `/etc/init.d/rundeckd` and start Rundeck at boot:

```bash
/etc/init.d/rundeckd start
/etc/init.d/rundeckd stop
```

Launcher (war) installs generate it under the base directory:

```bash
$RDECK_BASE/server/sbin/rundeckd start
$RDECK_BASE/server/sbin/rundeckd stop
```

You can wire the launcher script into your OS boot process yourself.

Choosing Java on RPM installs: by default Rundeck uses the `java` found in the path. Either set `JAVA_HOME` before running any command (Java is taken from `JAVA_HOME/bin`), or set `JAVA_HOME` in `/etc/rundeck/profile` as another option. Either avoids altering the global system configuration.

## Checked

2026-11-04: the rundeckd actions, the RPM/DEB init script path and boot start, the launcher script path, the start and stop commands and the JAVA_HOME options confirmed against the Rundeck Startup and Shutdown page. Removed an unsourced verify step.

Method: documentation only; no commands were run.
