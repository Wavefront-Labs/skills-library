---
id: computing-software.networking-hardware-and-wireless.unbound.rpz-zone-configuration
name: rpz-zone-configuration
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, rpz, respip, rpz-action-override, rpz-log, rpz-disable]
level: advanced
status: docs-checked
description: "Configure RPZ in Unbound: respip module, rpz clauses, transfer sources, overrides, logging, tags and runtime enable and disable."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rpz zone configuration
1. Load the module: `module-config: "respip validator iterator"`.
2. Add an `rpz:` clause per policy zone with `name` and `zonefile`; add `primary` (alias `master`, AXFR/IXFR) or `url` to transfer it.

```
server:
    module-config: "respip validator iterator"
rpz:
    name: policy.example.net
    zonefile: policy.example.net.zone
    rpz-log: yes
    rpz-log-name: example
```

Per-zone options: `rpz-action-override` (`nxdomain`, `nodata`, `passthru`, `drop`, `disabled`, `cname`), `rpz-cname-override`, `rpz-log` (default no), `rpz-log-name`, `rpz-signal-nxdomain-ra`, `for-downstream` (default no), `tags`, `allow-notify`, `max-transfer-size`, `max-transfer-time`.

`respip` goes before `dns64` if both are used. With `primary`, a full AXFR runs after every 5 IXFR transfers to consolidate memory. `url` and `primary` together: primaries are probed with SOA first, then URLs tried, then IXFR/AXFR. `for-downstream: yes` answers the RPZ zone itself to clients (for monitoring its SOA); `rpz-signal-nxdomain-ra` sends the NXDOMAIN with RA unset so clients like dnsmasq can tell it is externally blocked.

Behaviour: zones apply in config order. PASSTHRU counts as a match and stops later zones; `disabled` does not count as a match. `disabled` plus `rpz-log` tests a policy without affecting users. With tags, clients that match no tag are not filtered by tagged zones.

unbound-control: `rpz_disable zone`, `rpz_enable zone`, `auth_zone_reload`, and `list_auth_zones`. Per-action counters `num.rpz.action.<action>` need `extended-statistics`. `for-downstream` and `primary` behave as in auth-zone.

## Checked

2026-11-08. Read the RPZ topic page in full, the whole rpz section of unbound.conf and rpz_enable, rpz_disable and the num.rpz.action counters in unbound-control. Added respip versus dns64 ordering, the AXFR after 5 IXFR rule, for-downstream and rpz-signal-nxdomain-ra.

Method: documentation only; no commands were run.
