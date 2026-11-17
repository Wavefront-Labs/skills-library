---
id: computing-software.networking-hardware-and-wireless.unbound.chroot-and-username-privileges
name: chroot-and-username-privileges
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, chroot, username, privileges, permissions, pidfile]
level: practitioner
status: docs-checked
description: "Control Unbound chroot, privilege drop and working directory, and fix the permission errors they cause at startup."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# chroot and username privileges
Chroot is on by default and adds a layer of defence against remote exploits. If permission errors stop startup, use absolute file paths, or disable it with `chroot: ""`.

Unbound expects a user named `unbound` by default and drops to it after startup. Disable with `username: ""` (no change of user). If the user is enabled, files Unbound needs, such as the trust anchor, must be accessible to that user.

Defaults: `username` is `unbound` unless built otherwise; the default `chroot`, `directory` and `pidfile` locations are fixed at build or install time, so check your build.

With chroot enabled, pass the config file on the command line as a full path from the original root. Other paths (working directory, logfile, root hints, key files) can be absolute relative to the new root, relative to the working directory, or absolute relative to the original root. Unbound may also need `/dev/urandom` inside the chroot.

The pidfile is written just before chroot and the privilege drop, so it can live outside the chroot; Unbound cannot remove it at termination in that case.

With `username` set, privileges are dropped after the port is bound. Reloads keep the opened ports, but if you change to a port that needs privileges, a reload fails and a restart is needed.

`tls-cert-bundle` is read at startup before permission drop and chroot. A file Unbound updates, such as the auto-trust-anchor-file, needs write access for the Unbound user to the file and its directory.

## Checked

2026-11-08. Read the getting-started configuration page in full and the chroot, username, directory, pidfile and tls-cert-bundle entries of unbound.conf (not the whole page). Removed wrong fixed default paths, which are install-time values, and added the chroot path, pidfile and reload-port rules.

Method: documentation only; no commands were run.
