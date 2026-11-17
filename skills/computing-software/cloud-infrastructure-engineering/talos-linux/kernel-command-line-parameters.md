---
id: computing-software.cloud-infrastructure-engineering.talos-linux.kernel-command-line-parameters
name: kernel-command-line-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [kernel-args, talos-platform, ip-parameter, talos-config, dashboard, boot]
level: advanced
status: docs-checked
description: "Reference of Talos kernel parameters: required KSPP flags, talos.platform values, ip= and bond= syntax, talos.hostname, wipe, device settle time, auditd and halt_if_installed."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/reference/kernel.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Required parameters: `talos.platform` (one of `akamai`, `aws`, `azure`, `container`, `digitalocean`, `equinixMetal`, `gcp`, `hcloud`, `metal`, `nocloud`, `openstack`, `oracle`, `scaleway`, `upcloud`, `vmware`, `vultr`), `slab_nomerge` and `pti=on` (KSPP). Optional KSPP knobs: `init_on_alloc` and `init_on_free`.

Network and identity:

- `ip=<client-ip>:<server-ip>:<gw-ip>:<netmask>:<hostname>:<device>:<autoconf>:<dns0-ip>:<dns1-ip>:<ntp0-ip>`: initial interface, routes, DNS and NTP; repeatable and partial (`ip=:::::::<dns0-ip>:<dns1-ip>:<ntp0-ip>`). IPv6 in brackets. DHCP: `ip=:::::eth0.3:dhcp` or `ip=eth0.3:dhcp`.
- `bond=<bondname>:<bondslaves>:<options>:<mtu>`, for example `bond=bond1:eth3,eth4:mode=802.3ad,xmit_hash_policy=layer2+3:1450`. Name only defaults to `eth0`,`eth1` with `balance-rr`.
- `vlan=eth0.100:eth0` (one VLAN only).
- `net.ifnames=0` disables predictable names.
- `talos.hostname`, and `talos.network.interface.ignore` to skip DHCP attempts on NICs without a server.

Behaviour:

- `panic`: seconds before reboot after a panic (`0` disables rebooting).
- `talos.experimental.wipe`: `system` or `system:EPHEMERAL,STATE` (the latter returns to maintenance mode).
- `talos.shutdown`: `halt` or `poweroff`.
- `talos.device.settle_time`: extra wait for slow RAID controllers, max `10m`, for example `talos.device.settle_time=3m`.
- `talos.halt_if_installed=1`: pause boot if booted from ISO/PXE with an install already on disk.
- `talos.auditd.disabled=1`, `talos.dashboard.disabled=1` (default on SBCs), `talos.board` for ARM64 boards.
- `talos.environment=key=value`, repeatable, sets default environment variables.

## Checked

2026-11-04. Parameter list, ip/bond/vlan syntax, platform values and behavioural options confirmed on the Kernel reference page.

Method: documentation only; no commands were run.
