---
id: computing-software.systems-network-administration.linux.score-service-exposure-with-systemd-analyze-security
name: score-service-exposure-with-systemd-analyze-security
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd-analyze-security, systemd-hardening, protectsystem, no-new-privileges, sandboxing, exposure-level]
level: practitioner
status: docs-checked
description: "Score and reduce a service's attack surface with systemd-analyze security: read the exposure table, apply sandboxing directives in a drop-in, and test the service still works."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Score service exposure with systemd-analyze security

## Measure
```bash
systemd-analyze security                 # all services, exposure 0.0 (best) - 10.0 (worst)
systemd-analyze security nginx.service   # per-directive table with the score impact
systemd-analyze security --threshold=5 --offline=yes ./myapp.service   # CI gate on a unit file (v250+)
```
The overall exposure level is an estimate from 0.0 (tightly sandboxed) to 10.0 (little sandboxing). It only analyses the sandboxing features systemd itself implements, not the program.

## Harden with a drop-in
```bash
systemctl edit myapp.service
```
```ini
[Service]
DynamicUser=yes                 # or User=myapp
NoNewPrivileges=yes
ProtectSystem=strict            # / read-only except listed paths
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictNamespaces=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes      # denies writable-and-executable mappings; omit for programs that need them (JIT compilers)
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM
SystemCallArchitectures=native
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
StateDirectory=myapp            # writable /var/lib/myapp owned by the service user
LogsDirectory=myapp
ReadWritePaths=/srv/myapp/uploads
UMask=0077
```
Add directives a few at a time; after each step `systemctl daemon-reload && systemctl restart myapp` and run the functional test.

## Debug what broke
- `status=226/NAMESPACE`: a path in `ReadWritePaths`/`ReadOnlyPaths` doesn't exist (prefix with `-` to ignore missing).
- Killed by `SIGSYS`: `SystemCallFilter=` denied a call (the default action; `SystemCallErrorNumber=` changes it). `SystemCallLog=~@system-service` (v247 and later) logs calls outside that group so you can widen the filter.
- `Permission denied` writing files: `ProtectSystem=strict` + missing `ReadWritePaths`/`StateDirectory`.
- `systemd-run -p ProtectSystem=strict -p PrivateTmp=yes --pty --wait /usr/bin/myapp` lets you try settings ad hoc.

## Verify
- [ ] The exposure level drops and the service passes its health check after a restart and reboot.
- [ ] The drop-in is in config management, not only on the box.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `systemd-analyze security [UNIT]` exposure range 0.0-10.0; `--offline=` and `--threshold=` exist (v250 NEWS); every sandboxing directive in the drop-in exists in `systemd.exec`; `ProtectSystem=strict` semantics; `@system-service` as the recommended allow-list start; `SIGSYS` default for `SystemCallFilter=`; `SystemCallLog=` (v247); exit status 226/NAMESPACE and the `-` prefix for optional paths; `systemd-run -p ... --pty --wait`. Removed the third-party source, the UNSAFE/EXPOSED and score-number examples and the audit-log search command.

Method: documentation only; no commands were run.
