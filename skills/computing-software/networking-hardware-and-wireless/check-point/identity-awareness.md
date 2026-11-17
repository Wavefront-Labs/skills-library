---
id: computing-software.networking-hardware-and-wireless.check-point.identity-awareness
name: identity-awareness
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, identity-awareness, ad-query, identity-collector]
level: practitioner
status: draft
description: "Enable Check Point Identity Awareness with AD Query, Captive Portal or Identity Collector and use access roles in rules."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_IdentityAwareness_AdminGuide/Default.htm
  - https://www.checkpoint.com/training/certification/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identity Awareness: AD Query, Browser-Based and Identity Collector

- Identity Awareness maps IP addresses to users and machines. Sources: **AD Query** (reads domain controller Security event logs through WMI/DCOM; clientless, passive), **Browser-Based Authentication** (Captive Portal, Transparent Kerberos SSO), **Terminal Servers** agent, **Identity Agent**, and the **Identity Collector** (Windows service on a member server, which scales better and reads events/ADFS/syslog).
- Enable on the gateway object: Network Security > Identity Awareness. Add the **LDAP Account Unit** (Servers and OPSEC > LDAP Account Unit) with a read-only service account, then enable the sources.
```
pdp monitor all                 # gateway: show IP-to-user sessions
pdp control revoke_ip 10.1.10.55   # kick a stale session
pep show user all
adlog a dc                       # AD Query connectivity per DC
adlog a query                     # last AD Query results
```
- **Access Roles** (users, groups, machines, networks) are used in the rulebase Source/Destination, replacing IP-based rules.
- Time sync matters: Kerberos and event ordering fail with clock skew above 5 minutes.
- Gotcha: AD Query needs the DC audit policy to log account logon events (4624/4768), and the service account must be in Event Log Readers and have DCOM/WMI access; "Unauthorized" errors in `adlog a dc` point to that.
- Gotcha: shared IPs (NAT, terminal servers) break mapping unless you use the terminal servers agent.

Verify: `pdp monitor all` shows the logged-in user for a test IP; the Identity Awareness log in **Logs & Monitor** contains `Source User` and `Access Role`.
