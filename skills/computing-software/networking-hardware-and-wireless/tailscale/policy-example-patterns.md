---
id: computing-software.networking-hardware-and-wireless.tailscale.policy-example-patterns
name: policy-example-patterns
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [policy-examples, allow-all, microsegmentation]
level: practitioner
status: docs-checked
description: "Map common scenarios to the example policies the docs provide."
sources: ["https://tailscale.com/kb/1192"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Policy example patterns

Goal: start from a known pattern rather than a blank policy file.

The examples page lists scenarios and which policy sections each uses:

- **Allow all**: the default policy letting every device reach every other device (ACLs and SSH).
- **Deny all**: denies all connections (ACLs).
- **Users can access their own devices** (ACLs, SSH).
- **Resource-level access** using `hosts` aliases.
- **Restrict by purpose** using tags; **by group** using autogroups, custom groups and provisioned groups; **by individual user**.
- **Standard plan ACL**: employees reach their own devices and devices tagged `corp`; admins reach devices tagged `corp` or `prod`.
- **Internal application (VPN)** with groups, optionally with groups synced from an identity provider.
- **Remote access to production**, including `tests`.
- **VPC access (VPC peering)** using `autoApprovers`.
- **Share access with a contractor**, **remote development**, **pair programming** over SSH, **CI/CD deployment pipeline**, **monitoring access** on common ports, **application peering**, and **network microsegmentation** that allows access within segments but denies between them.

Most patterns combine `groups` and `tagOwners`; remote production access and network microsegmentation add `tests`; VPC access adds `autoApprovers`.

The page recommends migrating to grants and using grants for all new policy configuration, because ACLs will not receive new features; it points to separate grant examples.

**Checklist**

1. Choose the closest scenario.
2. Add `tests` before deploying.
3. Prefer the grant version of the example for new rules.

## Checked

2026-11-09. Confirmed against the Tailscale ACL policy examples page (scenario table and the allow-all, deny-all and own-devices sections). Removed the Convert to grants button claim and the preview checklist item, which the page does not mention.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1192 (ACL policy examples), table and first sections read.
