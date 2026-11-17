---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-debugging-and-dryrun
name: quadlet-debugging-and-dryrun
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, debugging, dryrun, systemd-analyze, quadlet-unit-dirs, generator, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug Quadlet files with the generator --dryrun, systemd-analyze verify, QUADLET_UNIT_DIRS to limit scope, and the not-found error that signals a syntax or version problem."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find out why a Quadlet did not become a service.

Symptom: `systemctl start {--user} example.service` fails with "Failed to start example.service: Unit example.service not found." Either the syntax is wrong, or the file uses an option from a newer Podman Quadlet than the installed generator, so the generator created no service.

View generated files and errors:

```
/usr/lib/systemd/system-generators/podman-system-generator {--user} --dryrun
```

Show only errors, plus extra checks on the generated unit:

```
systemd-analyze {--user} --generators=true verify example.service
```

To debug a few units, copy them to a separate directory and set `QUADLET_UNIT_DIRS`, which makes Quadlet look there instead of the usual search paths and so limits output to those units:

```
QUADLET_UNIT_DIRS=<Directory> /usr/lib/systemd/system-generators/podman-system-generator {--user} --dryrun
```

Also see the startup timeout skill for image-pull failures, which the page says can exceed systemd's default 90-second service start limit.


The `{--user}` placeholder in the commands means: include `--user` for rootless units and omit it for rootful ones. The dry-run output shows the contents of the generated service files, so it also helps check that mapped keys such as `PublishPort` ended up in the `ExecStart` line.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed. Wording tightened where the page is softer than the draft.
Method: documentation only; no commands were run.
