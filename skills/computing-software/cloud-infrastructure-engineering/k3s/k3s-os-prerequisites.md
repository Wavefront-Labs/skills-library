---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-os-prerequisites
name: k3s-os-prerequisites
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, firewalld, ufw, cgroups, nm-cloud-setup]
level: practitioner
status: docs-checked
description: "OS preparation for K3s covering firewalld, ufw, old RHEL NetworkManager, Raspberry Pi cgroups and unique hostnames."
sources:
  - https://docs.k3s.io/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pass the OS checks before installing.

Hostnames: two nodes cannot share a hostname. Use `--with-node-id` to append a random suffix, or pass a unique `--node-name` or $K3S_NODE_NAME.

Firewalld: recommended off (`systemctl disable firewalld --now`). If kept, allow:

```
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --zone=trusted --add-source=10.42.0.0/16
firewall-cmd --permanent --zone=trusted --add-source=10.43.0.0/16
firewall-cmd --reload
```

(10.42.0.0/16 is pods, 10.43.0.0/16 services; update if you change the CIDRs.)

ufw: recommended off (`ufw disable`); otherwise `ufw allow 6443/tcp`, `ufw allow from 10.42.0.0/16 to any`, `ufw allow from 10.43.0.0/16 to any`.

RHEL 10 needs `sudo dnf install -y kernel-modules-extra`. Releases before RHEL 8.4 have a NetworkManager bug; disable `nm-cloud-setup.service nm-cloud-setup.timer` and reboot.

Raspberry Pi OS: enable cgroups by appending `cgroup_memory=1 cgroup_enable=memory` to /boot/firmware/cmdline.txt (/boot/cmdline.txt on Debian 11 and older). Ubuntu 21.10 to 23.10 on Pi needs `sudo apt install linux-modules-extra-raspi` for vxlan; not needed on 24.04 and later.

Architectures: x86_64, armhf, arm64/aarch64.

Related: ports and firewall rules are in the network ports skill, and the Flannel VXLAN and WireGuard ports apply only when those backends are used. Check each requirement on every node, servers and agents alike, before running the install script.

## Checked

2026-11-03: read docs.k3s.io installation/requirements. Confirmed: unique hostname rules, firewalld and ufw guidance, RHEL 10 kernel-modules-extra, the pre-8.4 nm-cloud-setup bug, Raspberry Pi cgroup and cmdline.txt paths, Ubuntu 21.10-23.10 linux-modules-extra-raspi, and supported architectures.

Method: documentation only; no commands were run.
