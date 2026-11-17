---
id: computing-software.networking-hardware-and-wireless.check-point.administrator-permission-profiles
name: administrator-permission-profiles
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, permission-profiles, administrators, rbac]
level: practitioner
status: draft
description: "Create Check Point administrators with permission profiles (read-only, specific blades) and optional two-factor authentication."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/latest/APIs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Administrators and permission profiles

```
mgmt_cli -r true add administrator name "auditor1" authentication-method "check point password" password "..." permissions-profile "Read Only All" must-change-password true
mgmt_cli -r true add permissions-profile name "NetOps" access-control-objects true access-control-policy "write" threat-prevention-policy "read" logs-and-monitor "read"
mgmt_cli -r true set administrator name "auditor1" permissions-profile "NetOps"
mgmt_cli -r true publish
cpconfig                  # add the first administrator when installing
```
- Each **Administrator** has an authentication method (Check Point password, OS password, RADIUS, SecurID, TACACS, API key) and one **Permission Profile**. Profiles are built-in (Read Only All, Super User, Read/Write All) or custom, defining which policies, objects, Logs & Monitor and Management functions are read/write.
- Use named accounts for all admins and avoid the shared `admin`. Keep one local breakglass Super User with a long password stored in a vault.
- Set **Session timeout**, **Account lockout**, password complexity and expiration in Global Properties > Advanced / Gaia password policy.
- Install-policy permission is part of the profile ("Install policy" under Gateways); restricting it prevents edits from being pushed.
- Gaia OS users are separate (clish `add user`, roles), controlling CLI access to the gateways, not SmartConsole.
- Gotcha: a locked-out admin on a standby management needs `cpconfig` or `mgmt_cli -r true set administrator ... must-change-password` on the active server to fix.

Verify: log in to SmartConsole as the new user and confirm the greyed-out functions; **Audit Logs** records created admins.
