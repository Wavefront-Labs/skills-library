---
id: computing-software.cloud-infrastructure-engineering.podman.quadlet-container-security-options
name: quadlet-container-security-options
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [quadlet, security, capabilities, seccomp, apparmor, selinux, nonewprivileges, secret]
level: advanced
status: docs-checked
description: "Harden Quadlet containers: AddCapability, DropCapability, NoNewPrivileges, ReadOnly, SeccompProfile, AppArmor, SecurityLabel keys, Mask, Unmask and Secret."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict a Quadlet container with the available keys.

Capabilities: `AddCapability=` adds to the default Podman set; it is a space separated list that can repeat, e.g. `AddCapability=CAP_DAC_OVERRIDE CAP_IPC_OWNER`. `DropCapability=` maps to `--cap-drop`.

`NoNewPrivileges=` (default false) stops processes gaining privileges via setuid and file capabilities. `ReadOnly=` (default false) makes the image read-only; `ReadOnlyTmpfs=true` maps to `--read-only-tmpfs`.

`SeccompProfile=` is a JSON file path or `unconfined`; unset uses the default Podman profile. `AppArmor=` sets the profile and `unconfined` turns confinement off.

SELinux labels: `SecurityLabelDisable` turns off label separation, `SecurityLabelFileType` sets the file label type, `SecurityLabelLevel` and `SecurityLabelType` set the process level and type, and `SecurityLabelNested` lets labels work inside the container so nested containers are separated.

`Mask=` and `Unmask=` map to `--security-opt mask=` and `unmask=`.

`Secret=` uses a Podman secret as a file or environment variable, form `secret[,opt=opt ...]`.

`Rootfs=` conflicts with `Image` and, on SELinux, needs label `unconfined_u:object_r:container_file_t:s0` by default.


Examples from the table: `SeccompProfile=/tmp/s.json`, `AppArmor=alternate-profile`, `SecurityLabelType=spc_t`, `SecurityLabelLevel=s0:c1,c2`, `SecurityLabelFileType=usr_t`, `Unmask=ALL`.

## Checked

2026-11-03. Read against the official page text (podman-systemd.unit.5); every key, value, default, path and example left in this skill was confirmed there. Nothing removed.
Method: documentation only; no commands were run.
