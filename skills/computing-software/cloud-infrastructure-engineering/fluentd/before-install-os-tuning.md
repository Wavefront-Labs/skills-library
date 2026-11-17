---
id: computing-software.cloud-infrastructure-engineering.fluentd.before-install-os-tuning
name: before-install-os-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, ntp, file-descriptors, sysctl, ulimit, kernel-parameters, symlink-protection]
level: practitioner
status: docs-checked
description: "Prepare a host for Fluentd: NTP, file descriptor limits (ulimit, LimitNOFILE), network sysctl parameters and symlink/hardlink protection."
sources:
  - https://docs.fluentd.org/installation/before-install
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd pre-installation OS setup
1. **NTP**: run an NTP daemon (chrony, ntpd) so timestamps are accurate; the page recommends the AWS-hosted NTP server on AWS.
2. **File descriptors**: `ulimit -n` showing `1024` is insufficient. Add to `/etc/security/limits.conf` and reboot:
```
root soft nofile 65536
root hard nofile 65536
* soft nofile 65536
* hard nofile 65536
```
Under systemd use `LimitNOFILE=65536`. The td-agent package sets this by default.
3. **Network kernel parameters** (high load, many instances), in `/etc/sysctl.conf`, applied with `sysctl -p`:
```
net.core.somaxconn = 1024
net.core.netdev_max_backlog = 5000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_wmem = 4096 12582912 16777216
net.ipv4.tcp_rmem = 4096 12582912 16777216
net.ipv4.tcp_max_syn_backlog = 8096
net.ipv4.tcp_slow_start_after_idle = 0
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 10240 65535
net.ipv4.ip_local_reserved_ports = 24224
```
Reserve port 24224 (forward); for another port such as monitor_agent 24220, make it a comma-separated list.
4. **Link protection**: keep `fs.protected_hardlinks = 1` and `fs.protected_symlinks = 1`, since Fluentd sometimes writes to predictable paths (the page says these settings are almost enough against time-of-check to time-of-use bugs). Apply with `sysctl -p` or reboot.

## Checked

2026-11-04. Confirmed against the Fluentd Before Installation page (docs.fluentd.org/installation/before-install): NTP advice, ulimit and limits.conf lines, LimitNOFILE, the sysctl block, reserved ports and symlink/hardlink protection. Reworded the TOCTOU claim to match the page.

Method: documentation only; no commands were run.
