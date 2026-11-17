---
id: computing-software.cloud-infrastructure-engineering.openbao.templated-policies
name: templated-policies
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, templated-policy, identity-entity, groups, policy]
level: advanced
status: docs-checked
description: "Inject OpenBao identity values into policy paths using entity, alias and group template parameters, and why IDs beat names."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/policies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Templated policies

Templates inject identity values into `path` keys so one policy serves many users. Documented parameters:

- `identity.entity.id`, `identity.entity.name`
- `identity.entity.metadata.<key>`
- `identity.entity.aliases.<mount accessor>.id`, `.name`, `.metadata.<key>`, `.custom_metadata.<key>`
- `identity.groups.ids.<group id>.name`, `identity.groups.names.<group name>.id`
- `identity.groups.ids.<group id>.metadata.<key>`, `identity.groups.names.<group name>.metadata.<key>`

Prefer IDs over names: names can change or be reused.

## Default and root policies

- `default`: built in, cannot be removed, attached to all tokens by default. Its contents can be edited and OpenBao does not overwrite your changes. Attachment can be disabled at creation:

```
bao token create -no-default-policy
```

- `root`: built in, cannot be modified or removed, full access. Revoke initial root tokens after setup in production:

```
bao token revoke "<token>"
```

Get the mount accessor for the `aliases` form from `bao auth list`.

## Checked

2026-11-04. Read the OpenBao policies concepts page in full. Confirmed: the parameter table, only `path` keys allow injection, the advice to use IDs, `default` and `root` policy behaviour, `-no-default-policy` and `bao token revoke`, and `bao auth list` for the accessor. Removed: two gotchas the page does not state, a cross-reference to a skill not in this folder, and the vague alias `<field>` placeholder.
Method: documentation only; no commands were run.
