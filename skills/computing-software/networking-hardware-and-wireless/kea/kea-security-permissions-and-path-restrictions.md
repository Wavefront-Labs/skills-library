---
id: computing-software.networking-hardware-and-wireless.kea.kea-security-permissions-and-path-restrictions
name: kea-security-permissions-and-path-restrictions
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, security, path-restrictions, non-root, logging, environment-variables]
level: advanced
status: docs-checked
description: "Harden a Kea deployment: running without root, log secret masking, and the path restrictions and environment variable overrides since Kea 2.7.9."
sources:
  - https://kea.readthedocs.io/en/latest/arm/security.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea permissions and path restrictions
Privileges: DHCPv4 and DHCPv6 use privileged UDP ports 67 and 547, normally needing root. Using Linux capabilities, Kea can run from an unprivileged account (see "Running Kea From a Non-root Account on Linux" in the docs).

Logging: Kea can log a whole configuration. Since 1.9.7 values of entries ending in password or secret are replaced with asterisks, as database logs already were. Logs go to stdout, stderr, files or syslog; system file permissions apply to stdout/stderr and files, while syslog may export logs over the network.

Since Kea 2.7.9, files are restricted to compiled-in locations, each overridable with an environment variable:

| Element | Default | Override |
|---|---|---|
| config-write output | same directory as initial config | none |
| Host cache files | var/lib/kea | KEA_DHCP_DATA_DIR |
| Lease files, DHCPv6 server id file | var/lib/kea | KEA_DHCP_DATA_DIR |
| Log files | var/log/kea | KEA_LOG_FILE_DIR |
| Forensic log files | var/log/kea | KEA_LEGAL_LOG_DIR |
| Unix sockets | var/run/kea (directory must have 0750 access rights) | KEA_CONTROL_SOCKET_DIR |
| Hook library scripts | share/kea/scripts/ | KEA_HOOK_SCRIPTS_PATH |

Hook libraries load only from the compiled hooks directory, overridable with `KEA_HOOKS_PATH`. Use bare file names in configuration; a path elsewhere makes Kea emit an error and refuse to load the library. A path outside the allowed directory for sockets, logs and lease files makes Kea refuse to start (or log an unrecoverable error if already running).

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM security chapter (sections 5.3.1-5.3.6) and the hooks chapter (KEA_HOOKS_PATH note): non-root capabilities note, 1.9.7 masking of password/secret values, the path-restriction table with its environment variables, and the 2.7.9 gate. Added the 0750 socket directory requirement and the refuse-to-start behaviour from the same notes. Compiled-in locations are relative to the Kea install directory.
