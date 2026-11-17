---
id: computing-software.systems-network-administration.openldap.overlay-ppolicy
name: overlay-ppolicy
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, ppolicy, password-policy, ppolicy-default, overlay, pwdpolicysubentry]
level: practitioner
status: docs-checked
description: "Enable the OpenLDAP ppolicy overlay: directives, a default policy entry, per-user policy via pwdPolicySubentry, hash_cleartext, lockout reporting and replica forwarding."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-ppolicy&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ppolicy overlay
```
overlay ppolicy
ppolicy_default "cn=default,ou=policies,dc=example,dc=com"
ppolicy_hash_cleartext
```
Policy entry:
```
dn: cn=default,ou=policies,dc=example,dc=com
cn: default
objectClass: pwdPolicy
objectClass: namedPolicy
objectClass: top
pwdAttribute: userPassword
pwdMinLength: 5
pwdMaxFailure: 5
pwdLockout: TRUE
pwdLockoutDuration: 0
pwdInHistory: 5
```
`pwdPolicy` is auxiliary, so pair it with a structural class like `namedPolicy` (needs `cn`). `pwdAttribute` only accepts `userPassword`.

Directives:
- `ppolicy_default <DN>`: applies to entries with no `pwdPolicySubentry`. With no default and no per-entry policy, nothing is enforced.
- `ppolicy_hash_cleartext`: hash cleartext passwords on Add/Modify; it breaks the LDAP model, so protect access and use only for clients that skip Password Modify.
- `ppolicy_use_lockout`: return AccountLocked instead of InvalidCredentials; leaks information.
- `ppolicy_forward_updates`: on a consumer, forward bind-triggered state changes to the provider (needs `updateref` and the chain overlay).
- `ppolicy_send_netscape_controls`, `ppolicy_check_module <path>`.

Gotchas: based on the expired draft-behera-ldap-password-policy-09; rootdn bypasses history checks; replicas' local state is overwritten by the provider.

## Checked

2026-11-04. Confirmed against slapo-ppolicy(5) and the Administrator's Guide overlays chapter: ppolicy_default, ppolicy_forward_updates (needs updateref and chain overlay), ppolicy_hash_cleartext and its access advice, ppolicy_use_lockout information leak, ppolicy_send_netscape_controls, ppolicy_check_module, pwdPolicy auxiliary with namedPolicy and cn, pwdAttribute userPassword only, no default means no enforcement, rootdn exemptions, replica state overwrite, and the guide default policy example values. Reworded the draft status to the guide's wording.

Method: documentation only; no commands were run.
