---
id: computing-software.cybersecurity-defensive.zeek.live-capture-checksums
name: live-capture-checksums
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, live-capture, checksum-offloading, interface-capture]
level: intro
status: docs-checked
description: "Monitor a live interface with zeek -i, why -C is needed for checksum offloading, and why root is required."
sources: ["https://docs.zeek.org/en/current/quickstart.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# live capture checksums

Monitor a network device directly:

```
zeek -i en0 -C
```

Replace `en0` with the device to watch. Root access is typically required. Stop with Ctrl+C; logs land in the current directory and include every flow on the interface, not just test traffic.

`-C` tells Zeek to ignore checksums. By default Zeek discards packets with checksum errors. Modern operating systems and network devices use checksum offloading, which leaves checksums uninitialised, so monitoring local traffic needs `-C`.

Scripts work on live traffic the same way:

```
zeek example.zeek -i en0 -C
```

For anything beyond a single process, use ZeekControl, which keeps logs under the install prefix instead of the current directory.

## Checked

2026-11-08. Read the Quick Start Guide in full; every claim confirmed.

Method: documentation only; no commands were run.
