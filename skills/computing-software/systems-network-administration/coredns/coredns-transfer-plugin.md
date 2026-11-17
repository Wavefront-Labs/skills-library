---
id: computing-software.systems-network-administration.coredns.coredns-transfer-plugin
name: coredns-transfer-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, transfer, axfr, ixfr, notify]
level: advanced
status: docs-checked
description: "Allow outgoing AXFR and IXFR for zones served by file, auto, secondary or kubernetes, send NOTIFY, and restrict with acl."
sources:
  - https://coredns.io/plugins/transfer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let secondaries pull your zones.

transfer answers AXFR and IXFR requests (IXFR falls back to AXFR when the zone has changed) for authoritative plugins that implement transfer.Transferer: file, auto, secondary and kubernetes. Plugins call back into transfer to notify secondaries.

Syntax:

```
transfer [ZONE...] {
    to ADDRESS...
    source ADDRESS
}
```

- ZONE defaults to the enclosing block's zones. Another plugin in the same block must serve the zone and implement transfer.Transferer.
- `to ADDRESS...` hosts that may transfer; `*` permits all. NOTIFY goes to every ADDRESS that is an IP or IP and port, e.g. `1.2.3.4`, `[12:34::56]:5300`. `to` may repeat.
- `source ADDRESS` is the local address for sending notifications. It does not change who may request transfers.

Restrict with acl, from the docs:

```
acl {
    allow type AXFR net 10.1.0.0/16
    allow type IXFR net 10.1.0.0/16
    block type AXFR net *
    block type IXFR net *
}
transfer {
    to *
}
```

## Checked

2026-11-08. Checked in full against the transfer plugin README. Accurate; removed a closing tsig sentence that this page does not state.

Method: documentation only; no commands were run.
