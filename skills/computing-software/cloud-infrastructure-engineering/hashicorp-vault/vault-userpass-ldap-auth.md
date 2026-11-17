---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-userpass-ldap-auth
name: vault-userpass-ldap-auth
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, ldap-auth, ldap, group-mapping]
level: practitioner
status: docs-checked
description: "Configure Vault LDAP auth with TLS, a bind account, group mapping to policies, and the default user lockout."
sources: ["https://developer.hashicorp.com/vault/docs/auth/ldap", "https://developer.hashicorp.com/vault/api-docs/auth/ldap"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
vault auth enable ldap
vault write auth/ldap/config url="ldaps://ldap.example.com" \
  binddn="cn=vault,ou=Users,dc=example,dc=com" bindpass=... \
  userdn="ou=Users,dc=example,dc=com" userattr=sAMAccountName \
  groupdn="ou=Groups,dc=example,dc=com"
vault write auth/ldap/groups/engineers policies=app-read
vault login -method=ldap username=mitchellh
```

- Use `ldaps://`, or `starttls` for upgrading a plain connection. `insecure_tls` defaults to false; leave it so.
- `case_sensitive_names` defaults to false, so entity and group names are lowercased.
- Policies are mapped from groups when the token is created. Changing directory group membership does not change existing tokens; revoke them and have the user authenticate again.
- User lockout is on by default for ldap, userpass and approle: 5 failed attempts, 15 minute lockout duration, 15 minute counter reset.
- `auth/ldap/rotate-root` rotates the bind account password.

## Checked
2026-11-03. Confirmed on the LDAP auth docs and API pages (config fields, defaults, group mapping, login command, policy mapping at token creation, lockout defaults, `rotate-root`). Fixed `sources`, which pointed at the policies and AppRole pages. Removed: the "case sensitive in some directories" hedge, MFA and root-policy advice, the Verify step and the joiner-mover-leaver paragraph.
Method: documentation only; no commands were run.
