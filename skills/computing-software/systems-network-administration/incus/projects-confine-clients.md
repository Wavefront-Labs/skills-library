---
id: computing-software.systems-network-administration.incus.projects-confine-clients
name: projects-confine-clients
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, project, restricted, trust, tls, incus-group, confinement]
level: advanced
status: docs-checked
description: "Confine Incus users to projects: restricted TLS client certificates via incus config trust, and per-user projects created automatically for members of the incus group."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/projects_confine.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Confine clients to projects

TLS clients:
```
incus config trust add --projects <project> --restricted
incus config trust add-certificate <certificate_file> --projects <project> --restricted
incus config trust edit <fingerprint>
```
- The first form is for token authentication, the second adds a certificate file directly. Use them from the start so the client is confined as soon as its certificate is added.
- For an existing certificate, edit it, set `restricted` to `true` and list permitted projects under `projects`.
- `incus remote add --project` preselects a project but does not confine the client.

Local users:
1. Add them to the `incus` group, not `incus-admin`.
2. On first command, Incus creates a confined project for the user and switches to it, initialising Incus with defaults if needed.
3. To set limits or restrictions, edit the project afterwards; that needs `incus-admin` access.

## Checked

2026-11-04: confirmed against the Incus confine-projects how-to (restricted trust commands, editing an existing certificate, `remote add --project` not confining, `incus` versus `incus-admin` groups, automatic per-user project and initialisation). Nothing removed.

Method: documentation only; no commands were run.
