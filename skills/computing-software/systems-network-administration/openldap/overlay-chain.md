---
id: computing-software.systems-network-administration.openldap.overlay-chain
name: overlay-chain
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, chain, referral-chasing, chain-uri, overlay, idassert]
level: advanced
status: docs-checked
description: "Make OpenLDAP chase referrals itself with the chain overlay: chain-uri, per-URI identity assertion, chain-max-depth, chain-return-error and chain-cache-uri."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapo-chain&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapd-ldap&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# chain overlay
Automatic referral chasing for local storage backends. Referrals on bind are never chased. Every directive is prefixed `chain-`.

```
overlay                 chain
chain-rebind-as-user    FALSE

chain-uri               "ldap://ldap1.example.com"
chain-rebind-as-user    TRUE
chain-idassert-bind     bindmethod="simple" binddn="cn=Auth,dc=example,dc=com"
                        credentials="secret" mode="self"

chain-uri               "ldap://ldap2.example.com"
chain-idassert-bind     bindmethod="simple" binddn="cn=Auth,dc=example,dc=com"
                        credentials="secret" mode="none"
```
Directives:
- `chain-uri <ldapuri>`: one underlying ldap instance per URI.
- `chain-idassert-bind`: identity assertion (proxied authorization, RFC 4370) to that server only.
- `chain-cache-uri {FALSE|TRUE}` (default FALSE): cache connections for unlisted referral URIs (chased anonymously).
- `chain-max-depth <n>` (default 1, no further chasing).
- `chain-return-error {FALSE|TRUE}` (default FALSE): return the real error instead of the referral.
- `chain-chaining [resolve=r] [continuation=c] [critical]`: experimental control.

Inheritance: ldap settings before the first `chain-uri` apply to all URIs; settings after it apply only to that URI.

Gotchas: do not use it on ldap or meta backends, which already chase; URIs not listed are chased anonymously.

## Checked

2026-11-04. Confirmed against slapo-chain(5): referral chasing except on bind, built into the ldap backend, chain- prefix, overlay chain use with local backends and uselessness with ldap and meta, chain-cache-uri, chain-chaining, chain-max-depth default 1, chain-return-error, chain-uri with one URI per instance, identity assertion by RFC 4370, the example, inheritance of directives before the first chain-uri, anonymous chasing of unlisted URIs. Removed the unconfirmed ppolicy forwarding remark.

Method: documentation only; no commands were run.
