---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-user-id-group-mapping
name: pan-os-user-id-group-mapping
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [user-id, pan-os, ldap-group-mapping, ip-user-mapping, user-based-policy, usernames, group-include-list]
level: practitioner
status: draft
description: "Enable PAN-OS User-ID with LDAP group mapping and IP to user mapping so policy and logs use usernames and groups."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/user-id/user-id-concepts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: rules and logs that name people and groups instead of IP addresses.

Pieces: (1) group mapping from LDAP, (2) IP-to-user mapping from a source such as AD security log monitoring, syslog, GlobalProtect, Captive Portal or XML API, (3) User-ID enabled on the source zone.

```
configure
set user-id-collector group-mapping GM-CORP server-profile LDAP-CORP group-include-list [ "cn=firewall-allow,ou=groups,dc=example,dc=com" ]
set zone trust enable-user-identification yes
commit
```
(Confirm exact hierarchy for your release; the GUI path is Device > User Identification > Group Mapping Settings.)

Use the group in policy by its distinguished name or short name:
```
set rulebase security rules allow-eng from trust to untrust source-user "cn=firewall-allow,ou=groups,dc=example,dc=com" application [ ssl web-browsing ] action allow
```

Gotchas
- Group include list keeps memory small; do not pull the whole directory.
- Mapping timeout (default 45 minutes for AD monitoring, confirm) means stale mappings after DHCP changes; shorten for DHCP-heavy networks.
- Multi-user hosts (terminal servers) need Terminal Services Agent or port mapping, otherwise every user shares an IP.

## Verify
```
show user group list
show user group name "cn=firewall-allow,ou=groups,dc=example,dc=com"
show user ip-user-mapping all
show user ip-user-mapping ip 10.1.1.5
```
