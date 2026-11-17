---
id: computing-software.devops-ci-cd.rundeck.install-executable-war
name: install-executable-war
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, executable-war, rdeck-base, installonly, launcher]
level: practitioner
status: docs-checked
description: "Install Rundeck from the executable war: set RDECK_BASE, launch with java -jar, use launcher options, and update with --installonly while keeping custom jars."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/install/jar.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install:

```bash
export RDECK_BASE=$HOME/rundeck
mkdir -p $RDECK_BASE
cp rundeck-<version>.war $RDECK_BASE
cd $RDECK_BASE
java -Xmx4g -jar rundeck-<version>.war
```

Wait for `Grails application running at http://<host>:4440 in environment: production`, then log in as `admin` / `admin`. Add the CLI tools to your shell:

```bash
PATH=$PATH:$RDECK_BASE/tools/bin
MANPATH=$MANPATH:$RDECK_BASE/docs/man
```

Launcher options (see `-h`): `-b` basedir, `-c` configdir, `-p` projectdir, `-s` sbindir, `-x` bindir, `-d` debug, `--skipinstall` skip extraction, `--installonly` install without starting. By default directories sit in the working directory of the war.

Update:
1. Stop Rundeck and download the new war.
2. Optionally set `RDECK_BASE`, then run `java -jar rundeck-<version>.war --installonly`.
3. Copy over your customisations, including extra jars such as a SQL Server driver in `server/lib`.
4. Start Rundeck.

Gotcha: `UnsupportedClassVersionError: Bad version number in .class file` usually means an unsupported Java version.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Installing as an executable war: RDECK_BASE setup, java -Xmx4g -jar launch, Grails ready line, admin/admin login, PATH and MANPATH additions, the UnsupportedClassVersionError tip, launcher option list (-b -c -p -s -x -d -h, --skipinstall, --installonly), default directory layout, and the update steps including extra jars in server/lib. Nothing removed.

Method: documentation only; no commands were run.
