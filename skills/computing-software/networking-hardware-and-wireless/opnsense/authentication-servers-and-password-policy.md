---
id: computing-software.networking-hardware-and-wireless.opnsense.authentication-servers-and-password-policy
name: authentication-servers-and-password-policy
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [authentication-servers, password-policy, local-database, sha-512]
level: practitioner
status: docs-checked
description: "Configure OPNsense authentication servers and the local database password policy: duration, length, complexity, SHA-512 compliance."
sources: ["https://docs.opnsense.org/manual/users.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Authentication servers and local password policy

Authentication services are configured in System > Access > Servers, covering both local and remote sources. The web GUI uses local accounts by default; change this under System > Settings > Administration, in the Authentication group, with the Server option. Authentication always keeps a local anchor user for access rights, although some remote servers can report a user's group memberships after login.

Local account hardening: in System > Access > Servers, edit the Local Database entry (pencil icon). Policy options:

- Policy: enable password constraints.
- Duration: how often passwords must change.
- Length: minimum length.
- Complexity: enforce complexity checks.
- Compliance: require SHA-512 password hashing instead of the default Blowfish.

One-time passwords combined with the local database follow the same policy. The docs note the default Blowfish is outside AES and not FIPS compliant; although they consider it more secure than SHA-512, some environments forbid it, so use the Compliance toggle there.

Setup how-tos exist for local users, LDAP and RADIUS, and two-factor authentication builds on these servers. Any external server must be reachable from the firewall, which sometimes needs explicit routes (for example when it lies behind a classic IPsec tunnel).

## Checked

2026-11-03. Confirmed against the OPNsense Access / User Management manual page: System > Access > Servers, the Administration Server option, the local anchor user, the five policy options, the Blowfish and FIPS note, and the routing note. Nothing removed.

Method: documentation only; no commands were run.
