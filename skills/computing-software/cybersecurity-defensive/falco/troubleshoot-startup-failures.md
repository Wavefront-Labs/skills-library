---
id: computing-software.cybersecurity-defensive.falco.troubleshoot-startup-failures
name: troubleshoot-startup-failures
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [start-up-error, kernel-driver, kmod, modern-ebpf, driver-index]
level: practitioner
status: docs-checked
description: "Tell kernel driver, userspace and config start-up failures apart, and check bpf, DKMS and host mount preconditions for each driver."
sources:
  - https://falco.org/docs/troubleshooting/start-up-error/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
First try Falco with the default configuration and no plugins. Then watch the start-up output:
- A crash after the config load stages, during syscall source setup, points to the kernel driver (device unavailable, permissions, odd printouts, or the driver missing from the kernel).
- A crash after Falco started is likely a genuine bug.

Drivers: `modern_ebpf` has been the default since Falco 0.38.0, is bundled, and needs no separate download or build. The legacy `ebpf` driver was removed in Falco 0.44.0, so use `modern_ebpf` or `kmod`.

Preconditions:
- `modern_ebpf`: the `bpf` syscall must be allowed, not blocked by SELinux or similar. Lengthy instruction printouts mean an eBPF verifier failure; report it with `uname -r` to the maintainers.
- `kmod`: DKMS installed, possibly custom-signed modules, and a `/dev:/host/dev` mount in containers. The module must exist for the exact `uname -r` kernel. Pre-built drivers for stock Ubuntu, Fedora, Debian and others are listed in the Driver Index (download.falco.org/driver/site/index.html). Network ACLs can block the download, and on-the-fly builds can fail.
- Containers and DaemonSets need the host mounts `/etc:/host/etc`, `/proc:/host/proc`, `/boot:/host/boot` and `/dev:/host/dev`.

If you use `kmod` on a kernel meeting the modern eBPF requirements, switch to `modern_ebpf`; it uses CO-RE and needs no object per kernel release.

Gotcha: resource limits can lead the OOM killer to terminate Falco, which looks like a crash restart.

## Checked

2026-11-08. Read in full: the Falco "Falco Is Not Starting Up" troubleshooting page (raw markdown `docs/content/en/docs/troubleshooting/start-up-error.md`). Confirmed driver defaults and the 0.38.0 and 0.44.0 version gates, per-driver preconditions, host mounts, the Driver Index, the CO-RE note and the OOM-killer restart.

Method: documentation only; no commands were run.
