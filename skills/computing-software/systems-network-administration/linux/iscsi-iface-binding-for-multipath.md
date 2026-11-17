---
id: computing-software.systems-network-administration.linux.iscsi-iface-binding-for-multipath
name: iscsi-iface-binding-for-multipath
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, iscsi, iscsi-iface, iface-binding, iscsiadm, multipath, storage-network]
level: advanced
status: docs-checked
description: "Bind iSCSI sessions to specific NICs with iscsiadm ifaces so each path uses its own network, discovery through each iface, and verifying sessions per interface."
sources:
  - https://github.com/open-iscsi/open-iscsi/blob/master/README
  - https://github.com/open-iscsi/open-iscsi/blob/master/etc/iscsid.conf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iSCSI iface binding

**Why:** without binding, the kernel routes all iSCSI traffic out of one interface (by routing table) — two "paths"
that share one NIC aren't redundant. Ifaces pin each session to a NIC.

The open-iscsi README marks this feature experimental and says that if `ping -I ethX <portal>` fails, binding a session to that NIC will not work: fix the network first.

## Create ifaces
Each iface needs a unique name of at most 64 characters; never name one `default` or `iser` (special values).
```bash
iscsiadm -m iface -I iface0 --op=new
iscsiadm -m iface -I iface0 --op=update -n iface.hwaddress -v 00:0F:1F:92:6B:BF   # NIC 1 MAC
iscsiadm -m iface -I iface1 --op=new
iscsiadm -m iface -I iface1 --op=update -n iface.hwaddress -v 00:C0:DD:08:63:E7   # NIC 2 MAC
iscsiadm -m iface                       # lists default + your ifaces
```
The README's example binds by `iface.hwaddress`; `iface.net_ifacename` is described as the field used for software iSCSI vlan or alias binding. `--op=new` on an existing name overwrites it, and an iface with logged-in sessions cannot be updated until you log out.

## Discover and log in
```bash
iscsiadm -m discoverydb -t st -p 10.10.1.50:3260 --discover -P 1   # binds portals to every tcp iface defined
iscsiadm -m discoverydb -t st -p 10.10.1.50:3260 -I iface0 --discover -P 1   # only through iface0
iscsiadm -m node -L all                  # log in all discovered node records
iscsiadm -m session -P 1
```
Discovery itself uses the default route, not the iface. When tcp ifaces are defined, discovery binds the portals it finds to them; `-I default` gives the old unbound behaviour. Each target portal then has one session per iface, so multipath sees one path per iface. Remove bindings with `iscsiadm -m node -T <target> -I iface0 --op=delete`.

## When NOT to bind
The README says to skip ifaces if portals and NICs are on different subnets and the network layer can pick the right path itself. Follow the array vendor's design.

## Prep and startup
- Set `net.ipv4.conf.default.rp_filter` to 0 or 2 (the README requires it for iface binding; a reboot may be needed for it to apply).
- `node.startup = automatic` in node records (the `iscsid.conf` default is `manual`) for boot-time login; mark fstab entries `_netdev`.

## Verify
- [ ] `iscsiadm -m session -P 1` shows sessions on both ifaces; `multipath -ll` shows one path per iface for each LUN.

## Checked

Checked 2026-10-26 against the open-iscsi README and etc/iscsid.conf (open-iscsi/open-iscsi master, last commit 2026-10-06), section 5.1 (iface binding, discovery) and 8.1. Confirmed: iface create/update commands, 64-character iface names and the reserved names default and iser, rp_filter 0 or 2 requirement, discoverydb syntax and -I iface, discovery using the default route, automatic binding of discovered portals to tcp ifaces, node deletion per iface, node.startup default manual, _netdev. Corrected: the subnet statement (README says binding is unnecessary when portals and NICs are on different subnets), rp_filter value, discovery syntax; removed unconfirmed jumbo-frame, VLAN and gateway advice.

Method: documentation only; no commands were run.
