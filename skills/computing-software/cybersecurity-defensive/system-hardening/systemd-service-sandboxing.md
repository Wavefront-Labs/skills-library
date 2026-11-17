---
id: computing-software.cybersecurity-defensive.system-hardening.systemd-service-sandboxing
name: systemd-service-sandboxing
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, systemd-sandboxing, systemd-analyze-security, protectsystem, dynamicuser, capabilityboundingset, systemcallfilter]
level: advanced
status: docs-checked
description: "Sandbox Linux services with systemd: systemd-analyze security scores, ProtectSystem, PrivateTmp, NoNewPrivileges, capabilities, syscall filters, iterative testing."
sources: ["https://github.com/systemd/systemd/blob/main/man/systemd.exec.xml", "https://github.com/systemd/systemd/blob/main/man/systemd-analyze.xml", "https://github.com/systemd/systemd/blob/main/man/systemd.resource-control.xml", "https://github.com/torvalds/linux/blob/master/Documentation/filesystems/proc.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd service sandboxing

Most daemons run with far more access than they need. systemd can confine them without containers.

## Measure
```
systemd-analyze security                 # exposure score per service (0 = locked down, 10 = unsafe)
systemd-analyze security nginx.service   # per-setting breakdown
```

## Apply via drop-in (do not edit vendor units)
`systemctl edit myapp.service`:
```ini
[Service]
User=myapp
Group=myapp
# or DynamicUser=yes for stateless services
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=/var/lib/myapp /var/log/myapp
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
MemoryDenyWriteExecute=yes          # forbids memory mappings that are writable and executable at once; omit for JIT-compiling runtimes
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_BIND_SERVICE
SystemCallFilter=@system-service
SystemCallFilter=~@privileged @resources
SystemCallArchitectures=native
UMask=0077
IPAddressDeny=any                   # filters ingress and egress; add IPAddressAllow= for every peer the service needs
```
Then `systemctl daemon-reload && systemctl restart myapp`.

## Iterate
Add a block of options, restart, run functional tests, check `journalctl -u myapp` for EPERM/EACCES errors and any seccomp audit messages, relax only the specific option that breaks.
Common needs: write paths (add to ReadWritePaths), binding to <1024 (capability), JIT (drop MemoryDenyWriteExecute),
netlink (`AF_NETLINK`).

## Notes
- `ProtectSystem=strict` mounts the entire file system hierarchy read-only except the API file systems `/dev`, `/proc` and `/sys` (protect those with `PrivateDevices=`, `ProtectKernelTunables=`, `ProtectControlGroups=`) and paths listed in `ReadWritePaths=`, `StateDirectory=` and related settings.
- `DynamicUser=yes` allocates a transient UID and implicitly enables `ProtectSystem=strict`, `NoNewPrivileges=` and `RestrictSUIDSGID=` (and `PrivateTmp=`); state goes in `StateDirectory=`.
- Options apply to the service's processes only; they do not replace patching or AppArmor/SELinux, but stack well.

## Gotchas
- Availability of an option depends on the systemd version and kernel; check each directive in systemd.exec(5) for your release.
- Distribution units may already set some options; check with `systemctl cat`.

## Verify
`systemd-analyze security myapp.service` shows a lower exposure score (0.0 to 10.0, higher is more exposed), the service passes its health
checks, and `cat /proc/<pid>/status | grep -E 'NoNewPrivs|Seccomp|CapBnd'` shows the restrictions.

## Checked
Checked 2026-10-25 against systemd.exec(5), systemd.resource-control(5) and systemd-analyze(1) sources (systemd/systemd, main branch, 2026-10) and the kernel proc documentation. Confirmed: every directive in the example (NoNewPrivileges, ProtectSystem=strict, ReadWritePaths, ProtectHome, PrivateTmp, PrivateDevices, ProtectKernelTunables/Modules/Logs, ProtectControlGroups, ProtectClock, ProtectHostname, RestrictNamespaces, RestrictRealtime, RestrictSUIDSGID, LockPersonality, MemoryDenyWriteExecute, RestrictAddressFamilies, CapabilityBoundingSet, AmbientCapabilities, SystemCallFilter with `@system-service`, `@privileged` and `@resources`, SystemCallArchitectures, UMask, IPAddressDeny/Allow), the 0.0 to 10.0 exposure range, DynamicUser implications, and the `NoNewPrivs`, `Seccomp` and `CapBnd` fields in /proc/<pid>/status. Corrected: IPAddressDeny filters ingress as well as egress. Removed unconfirmed: the score-band target, `ausearch -m SECCOMP`, the warning-on-unsupported-option note and the Arch wiki reference (not read).

Method: documentation only; no commands were run.
