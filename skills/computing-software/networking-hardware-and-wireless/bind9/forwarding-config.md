---
id: computing-software.networking-hardware-and-wireless.bind9.forwarding-config
name: forwarding-config
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, forwarders, forward-only, forward-zone]
level: practitioner
status: docs-checked
description: "Forward queries in BIND 9 globally with forwarders and forward only, or per zone with type forward."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forwarding config
Global forwarding in `options`:

```
options {
    forwarders { /* upstream resolver addresses */ };
    forward only;
};
```

`forward only` means named queries only the forwarders; `forward first` (the default) queries them and, if that does not answer the question, then looks for the answer itself.

Per-domain forwarding uses a forward zone:

```
zone "internal.example" {
    type forward;
    forwarders { /* internal DNS addresses */ };
};
```

A zone-level `forwarders` and `forward` override the global values for that zone. In a forward zone with no `forwarders` of its own, no forwarding is done and the global options are not used.

## Checked

2026-11-04. Confirmed against the ARM reference entries for `forward`, `forwarders` and `type forward`: first is the default, only fails after the forwarders give no answer, per-zone override. Added the forward-zone behaviour when `forwarders` is absent.

Method: documentation only; no commands were run.
