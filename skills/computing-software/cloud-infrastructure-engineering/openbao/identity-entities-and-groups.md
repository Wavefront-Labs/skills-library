---
id: computing-software.cloud-infrastructure-engineering.openbao.identity-entities-and-groups
name: identity-entities-and-groups
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, identity, entity, alias, groups]
level: advanced
status: docs-checked
description: "OpenBao identity model: entities, aliases, internal vs external groups, implicit entity creation and the privilege-escalation risks."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/identity.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity: entities, aliases, groups

- An **entity** is the consolidated representation of a user; it holds zero or more **aliases**, one per auth backend at most, mapping to that user's accounts.
- An alias is identified by its name plus the accessor of its auth mount. Same auth type on different mounts can link to one entity.
- Operators manage entities; OpenBao is a cache of identities, not a source.
- With no entity on a successful login, OpenBao implicitly creates one with a new alias.

## Groups

- **Internal** (default): membership managed manually.
- **External**: map to a group outside (LDAP group, GitHub team); one alias only. Membership updates at login and token renewal, so removals apply at the next one.
- Subgroups pass policies up: members of a subgroup inherit the parent's policies.

## Policies

Entity and group policies add to a token's own and are evaluated at request time, so changes affect tokens already issued. They never replace token policies.

Token-store tokens normally have no identity; assign an entity with `entity_alias` when the role's `allowed_entity_aliases` permits.

## Warnings

Restrict write access to identity endpoints. Anyone who can edit group membership can add their entity to a higher-privilege group; editing an entity or login alias can likewise grant privileges.

## Checked

2026-11-04. Confirmed against the Identity concepts page: entities and aliases, one alias per auth backend, alias name plus mount accessor, OpenBao as a cache of identities, implicit entity creation, internal and external groups, subgroup policy inheritance, additional-only entity policies evaluated at request time, entity_alias with allowed_entity_aliases and the privilege warnings. Nothing removed.

Method: documentation only; no commands were run.
