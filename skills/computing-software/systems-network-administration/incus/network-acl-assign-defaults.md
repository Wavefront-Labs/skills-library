---
id: computing-software.systems-network-administration.incus.network-acl-assign-defaults
name: network-acl-assign-defaults
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network-acl, security-acls, default-action, logging, show-log, bridge-limitations]
level: advanced
status: docs-checked
description: "Apply Incus ACLs to networks or NICs with security.acls, how rules are evaluated, default reject actions, logging, and bridge limitations."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_acls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assign ACLs, defaults and limits

```
incus network set <network> security.acls="<ACL>"
incus config device set <instance> <device> security.acls="<ACL>"
incus network acl show-log <ACL>
```

- Rule order in the list is irrelevant: evaluation is `drop`, then `reject`, then `allow`. With several ACLs on a NIC, the first matching action wins.
- Once ACLs apply, a default reject rule rejects unmatched traffic. Change with `security.acls.default.ingress.action` and `security.acls.default.egress.action` on the network or NIC; NIC settings override network settings.
- A rule with `state=logged` records matching traffic: use it to test before enforcing.

Bridge limitations:
- ACLs apply only at the bridge/host boundary, so they cannot filter traffic between instances on the same bridge.
- Applied directly to a NIC, ingress `reject` becomes `drop` (nftables limitation).
- No ACL group or network selectors.
- Baseline network-service rules run before ACLs and cannot be blocked.

## Checked

2026-11-04: confirmed against the Incus network ACLs how-to (`security.acls` on networks and NICs, drop-reject-allow ordering, default action keys and NIC override, `state=logged`, `show-log`, bridge limitations). Corrected: the default rule rejects unmatched traffic (it does not drop it).

Method: documentation only; no commands were run.
