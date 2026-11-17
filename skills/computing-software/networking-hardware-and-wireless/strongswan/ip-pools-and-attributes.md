---
id: computing-software.networking-hardware-and-wireless.strongswan.ip-pools-and-attributes
name: ip-pools-and-attributes
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, pools, virtual-ip, dns-attribute, split-include, vips]
level: practitioner
status: docs-checked
description: "Define swanctl.conf pools of virtual IPs with extra attributes such as dns, split_include and split_exclude, and request addresses on the client with vips."
sources:
  - https://docs.strongswan.org/docs/latest/swanctl/swanctlConf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ip pools and attributes
**Pools section.** Each named pool has `addrs`, either one CIDR subnet or a range `<from>-<to>`. Pools must be unique and non-overlapping. Extra attributes are comma-separated lists under `<name>.<attr>`, where `<attr>` is one of `dns`, `nbns`, `dhcp`, `netmask`, `server`, `subnet`, `p_cscf`, `split_include` and `split_exclude`, or a numerical identifier (string values accepted).

```
pools {
  rw_pool {
    addrs = 10.3.0.0/16
  }
}
```

**Using pools.** A connection references pools by name in `pools` (comma-separated, named pools or external pools). Query order depends mainly on plugin order; the order only matters within the same backend. Load with `swanctl --load-pools`.

**Requesting addresses.** The client sets `vips` on the connection: a list of virtual IPs for IKEv2 configuration payloads or IKEv1 ModeConfig. `0.0.0.0` and `::` request any address; specific ones may be named. The responder may return a different address or none.

`pull` (default yes) selects ModeConfig pull mode; push mode exists for IKEv1 only and is not recommended.

## Checked
2026-11-04. Confirmed against the strongSwan swanctl.conf reference (pools addrs and attribute types, connection pools, vips, pull). Nothing removed.

Method: documentation only; no commands were run.
