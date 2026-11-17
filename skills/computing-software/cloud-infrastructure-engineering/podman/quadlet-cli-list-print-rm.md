---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-cli-list-print-rm
name: quadlet-cli-list-print-rm
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet-list, quadlet-print, quadlet-rm, filter, format, recursive, template-quadlet]
level: practitioner
status: docs-checked
description: "Inspect and remove installed Quadlets with podman quadlet list, print and rm: columns, name/pod/status filters, Go templates, template removal and application removal."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-list.1.html
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-rm.1.html
  - https://docs.podman.io/en/latest/markdown/podman-quadlet-print.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: audit and clean up Quadlets managed through podman.

`podman quadlet list` (alias `ls`) lists Quadlets for the current user with name, systemd unit name, file path, status, application and pod. `--filter`/`-f` can repeat: `name`, `pod` (the `Pod=` value, shown for .container units) and `status`, with valid statuses `Not loaded`, `loaded template`, `active/running`, `inactive/dead`, `failed/failed`, `activating/start`, `deactivating/stop`. `--format` takes JSON or a Go template with `.App`, `.Name`, `.Path`, `.Pod`, `.Status`, `.UnitName`; for example `--format '{{ .UnitName }}'`. `Not loaded` and `loaded template` statuses come from podman, the others from systemd.

`podman quadlet print` (alias `cat`) shows the file including comments: `podman quadlet print myquadlet.container`.

`podman quadlet rm [options] quadlet|application...` removes Quadlets. Options: `--all`/`-a`; `--force`/`-f` removes running Quadlets (for uninstantiated templates it stops instances); `--ignore`/`-i` ignores missing ones; `--recursive` is required to remove applications. Removing a template such as `templateName@.container` also removes the generated `templateName@.service`; if instances run, it fails without `--force`. Removing one Quadlet in an application removes the whole application.

## Checked
2026-11-09: read the podman-quadlet-list, podman-quadlet-print and podman-quadlet-rm man pages in full and confirmed the default columns, filters and valid statuses, format placeholders, the print alias and example, and the rm options, template and application behaviour. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
