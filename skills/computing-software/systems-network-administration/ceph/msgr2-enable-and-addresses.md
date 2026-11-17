---
id: computing-software.systems-network-administration.ceph.msgr2-enable-and-addresses
name: msgr2-enable-and-addresses
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, msgr2, messenger, monitor, v2, v1]
level: advanced
status: docs-checked
description: "Move a Ceph cluster from v1-only to v2-plus-v1 messenger with ceph mon enable-msgr2 and fix monitor addresses."
sources:
  - https://docs.ceph.com/en/latest/rados/configuration/msgr2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Messenger v2 adds encryption modes and compression on the wire. To transition a cluster that only speaks v1, enable it on the monitors:

```
ceph mon enable-msgr2
```

If a monitor needs both address types set explicitly:

```
ceph mon set-addrs a [v2:1.2.3.4:1112,v1:1.2.3.4:1111]
```

After the transition, update `ceph.conf` and `mon_host` on clients so they list both address forms; when the default ports (3300 and 6789) are used they can be omitted.

The plain `ceph mon enable-msgr2` form applies when the monitors bind to the default legacy port 6789 for v1.

Read the page's sections on address formats, connection modes and compression modes before changing the secure or crc connection options, which are per-daemon-type configuration settings.

Defaults to know: monitors bind to the IANA-assigned port `3300` for v2 and keep `6789` for legacy v1, and `ms_bind_msgr1` and `ms_bind_msgr2` default to true while `ms_bind_ipv6` defaults to false. A monitor shows both forms in the monmap, for example `[v2:10.0.0.10:3300/0,v1:10.0.0.10:6789/0]`. In `ceph.conf`, `mon_host` may list just addresses when default ports are used, or the full bracketed form. Secure mode encrypts all traffic and compression modes are controlled by `ms_osd_compress_mode`, `ms_osd_compress_min_size` and `ms_osd_compression_algorithm`.

## Checked

2026-11-09. Confirmed against: the Ceph Messenger V2 page (docs.ceph.com/en/latest/rados/configuration/msgr2/): v2 features, ports, bind options, enable-msgr2, set-addrs and mon_host formats.

Removed: the `MON_MSGR2_NOT_ENABLED` health-check note and the DNS-lookup remark (not on the page).

Method: documentation only; no commands were run.

