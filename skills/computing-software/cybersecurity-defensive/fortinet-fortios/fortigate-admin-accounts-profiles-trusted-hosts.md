---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-admin-accounts-profiles-trusted-hosts
name: fortigate-admin-accounts-profiles-trusted-hosts
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [admin-profile, fortios, accprofile, trusthost, administrators, rbac, api-user]
level: practitioner
status: draft
description: "Create FortiGate administrator accounts with custom access profiles, trusted hosts and a read-only API user."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: each person or tool has a named account with least privilege and a restricted source address.

```
config system accprofile
    edit "auditor"
        set secfabgrp read
        set ftviewgrp read
        set authgrp read
        set sysgrp read
        set netgrp read
        set loggrp read
        set fwgrp read
        set vpngrp read
        set utmgrp read
    next
end
config system admin
    edit "alice"
        set accprofile "auditor"
        set trusthost1 192.0.2.0 255.255.255.240
        set password <PASSWORD>
    next
end
config system api-user
    edit "monitor-api"
        set accprofile "auditor"
        config trusthost
            edit 1
                set ipv4-trusthost 192.0.2.50 255.255.255.255
            next
        end
    next
end
```
Generate the REST API token with `execute api-user generate-key monitor-api` and store it in a vault.

Gotchas
- Always set trusthosts; a login from outside them is refused even with the right password (and the same applies to API tokens).
- The `super_admin` profile is global; VDOM admins need a profile plus the `vdom` assignment.
- Prefer remote authentication (LDAP, RADIUS, SAML) with a local break-glass account.

## Verify
```
show system admin alice
diagnose sys admin-session list
```
Log in as the account from a permitted and a non-permitted host and confirm only the first succeeds.
