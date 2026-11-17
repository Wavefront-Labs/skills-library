---
id: computing-software.systems-network-administration.linux.disable-ipv6-and-per-interface-ipv6-sysctls
name: disable-ipv6-and-per-interface-ipv6-sysctls
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sysctl, disable-ipv6, ipv6, net-ipv6-conf, ipv6-disable-kernel-param, use-tempaddr, ipv6-forwarding]
level: practitioner
status: docs-checked
description: "Disable or tune IPv6 correctly: ipv6.disable=1 vs net.ipv6.conf.*.disable_ipv6, per-interface settings, side effects on services, and why disabling is usually wrong."
sources:
  - https://docs.kernel.org/networking/ip-sysctl.html
  - https://docs.kernel.org/networking/ipv6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disabling or tuning IPv6

## Two very different switches
| Method | Effect |
|---|---|
| `ipv6.disable=1` (module parameter / kernel cmdline) | module loaded but IPv6 functionality disabled: no IPv6 addresses are added to interfaces and no IPv6 socket can be opened; a reboot is required to enable IPv6 again |
| `net.ipv6.conf.all.disable_ipv6=1` (sysctl) | IPv6 disabled on all interfaces: addresses and routes are deleted and none are added; switching back to 0 recreates a link-local address and restarts DAD |
Both are documented in the kernel docs; some software that expects IPv6 breaks either way.

## Per-interface
```ini
# /etc/sysctl.d/70-ipv6.conf
net.ipv6.conf.default.disable_ipv6 = 1     # future interfaces
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 0          # keep IPv6 on loopback (::1)
net.ipv6.conf.eth0.use_tempaddr = 2        # privacy extensions, prefer temporary addresses
net.ipv6.conf.all.forwarding = 1           # router: accept_ra then defaults to off unless set to 2
```
NetworkManager: `nmcli con mod eth0 ipv6.method disabled` disables IPv6 for that connection (documented method since NetworkManager 1.20).

## Side effects to check after disabling
- Services configured to listen on IPv6 addresses (or `::`) may fail to start once IPv6 is off: set their address-family or listen options to IPv4 (see each service's documentation).
- sysctl settings apply after they are loaded; early boot may still have IPv6 (a kernel command-line parameter acts earlier).

## Gotchas
- `sysctl --system` order: a later file can re-enable; check with `sysctl -a | grep disable_ipv6`.
- Disabling IPv6 to work around slow name resolution usually hides a broken AAAA record or IPv6 route; fix that instead.

## Verify
- [ ] `ip -6 addr` shows only what you intended; `ss -tlnp` shows services listening; the setting persists after reboot.

## Checked

Date: 2026-10-25. Documentation release: Linux kernel Documentation/networking (torvalds/linux master)/ipv6.rst and ip-sysctl.rst (disable_ipv6 semantics, conf/all vs conf/default), NetworkManager settings reference text and libnm headers (NetworkManager main), read 2026-10-25.
Corrected: the skill described `ipv6.disable=1` as never initialising the module and sysctl as still allowing IPv6 sockets; the kernel docs say the parameter loads the module but disables all functionality (no addresses, no IPv6 sockets), and that `disable_ipv6` removes addresses and routes.
Confirmed: `disable_ipv6` all/default/per-interface behaviour, `use_tempaddr`, `forwarding` and `accept_ra` interplay; NetworkManager `ipv6.method disabled`.
Removed as unconfirmed: the Red Hat recommendation and both external links, the dotted-interface-name sysctl rule, specific daemon directives, the dracut remark and the resolver workarounds.

Method: documentation only; no commands were run.
