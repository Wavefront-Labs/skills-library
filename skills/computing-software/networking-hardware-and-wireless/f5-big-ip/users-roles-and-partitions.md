---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.users-roles-and-partitions
name: users-roles-and-partitions
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, user-roles, partitions, rbac]
level: practitioner
status: draft
description: "Create local BIG-IP users with roles bound to partitions and understand the Common partition and default route domain interplay."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Local users, roles and partitions

```
tmsh create auth partition AppA description "App A"
tmsh create auth user alice password 'ChangeMe!' partition-access add { AppA { role resource-admin } }
tmsh modify auth user alice shell none
tmsh list auth user alice
tmsh modify auth password admin
tmsh modify cli preference
```
- Roles include `admin`, `resource-admin`, `manager`, `application-editor`, `operator`, `guest`, `certificate-manager`, `irule-manager`, `auditor`, `web-application-security-*` (confirm exact list on your version). `admin` and `resource-admin` are the only ones that can see all partitions; others see only partitions assigned.
- Objects in `Common` are visible to every partition; `/Common/` pool referenced by a virtual in `/AppA/` works, but the reverse does not.
- A user in `AppA` creates objects only there, so a shared profile must be created by an admin in `/Common`.
- `shell none` leaves GUI/REST access only; `tmsh` or `bash` shell need explicit grants.
- Gotcha: the `admin` user has the root-equivalent role. Change the default password on all units and sync does not copy passwords of local users unless in the same device group config sync (they do sync; the `root` account does not).

Verify: log in as the user and run `tmsh list ltm pool`; objects from other partitions must be absent. `tmsh show auth user` lists roles; the audit log is `/var/log/audit`.
