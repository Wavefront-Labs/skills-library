---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-identity-entities-groups
name: vault-identity-entities-groups
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, identity-groups, entity-alias, external-groups]
level: practitioner
status: docs-checked
description: "Map auth aliases to Vault entities and use internal and external groups to assign policies consistently across auth methods."
sources: ["https://developer.hashicorp.com/vault/docs/concepts/policies", "https://developer.hashicorp.com/vault/docs/auth/jwt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An entity represents a person or machine; aliases tie it to logins from different auth methods. Groups attach policies to many entities.

```sh
vault write identity/entity name=alice
vault write identity/entity-alias name=alice canonical_id=<entity-id> mount_accessor=<oidc-accessor>
vault write identity/group name=platform policies=platform-admin member_entity_ids=<entity-id>
vault write identity/group name=idp-platform type=external policies=platform-admin
vault write identity/group-alias name="platform-team" mount_accessor=<oidc-accessor> canonical_id=<group-id>
```

Gotchas: an external group can have only one alias, which must map to a group outside Vault (for example an LDAP group or GitHub team). Membership is added at login and token renewal, and a user removed from the outside group is removed from the Vault group only at the next login or renewal.

## Checked

2026-11-03. Confirmed against the Vault identity concepts page (entities, aliases, internal and external groups, one alias per external group, membership updated on login or renewal). Removed: case-sensitivity of alias names, accessor orphaning on remount, entity deletion and token expiry claims, the `identity_policies` verify step and a generic tip.

Method: documentation only; no commands were run.
