---
id: computing-software.cybersecurity-defensive.fortinet-fortios.fortigate-ldap-servers-and-user-groups
name: fortigate-ldap-servers-and-user-groups
category: computing-software
field: cybersecurity-defensive
product: fortinet-fortios
tags: [ldap-server, fortios, user-group, ldaps, active-directory, remote-groups, authentication-test]
level: practitioner
status: draft
description: "Add an LDAP/Active Directory server to FortiGate, create user groups from LDAP groups and test authentication."
sources: ["https://docs.fortinet.com/document/fortigate/7.4.0/administration-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: policies that use directory groups.

```
config user ldap
    edit "AD-CORP"
        set server "192.0.2.20"
        set cnid "sAMAccountName"
        set dn "dc=example,dc=com"
        set type regular
        set username "cn=svc-fgt,ou=service,dc=example,dc=com"
        set password <PASSWORD>
        set secure ldaps
        set ca-cert "CA_Cert_1"
        set port 636
    next
end
config user group
    edit "ENG"
        set member "AD-CORP"
        config match
            edit 1
                set server-name "AD-CORP"
                set group-name "cn=eng,ou=groups,dc=example,dc=com"
            next
        end
    next
end
```
Test:
```
diagnose test authserver ldap AD-CORP alice <PASSWORD>
```
Use the group as `set groups "ENG"` in an identity-based firewall policy or in VPN user groups.

Gotchas
- LDAPS validates the server certificate against the CA you import; with no `ca-cert`, binding can fail or be unverified depending on `server-identity-check`.
- Nested groups require the AD-specific group-search filter and `member-attr` settings; confirm.
- Limit the service account to read-only.

## Verify
`diagnose test authserver ldap` prints the group membership with a success result; `diagnose debug application fnbamd -1` and `diagnose debug enable` show the bind steps (disable after).
