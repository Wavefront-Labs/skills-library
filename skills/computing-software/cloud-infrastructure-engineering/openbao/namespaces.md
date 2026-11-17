---
id: computing-software.cloud-infrastructure-engineering.openbao.namespaces
name: namespaces
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, namespaces, multi-tenancy, x-vault-namespace, delegation]
level: practitioner
status: docs-checked
description: "OpenBao namespaces for multi-tenancy: nesting, naming limits, the X-Vault-Namespace header, and why not to enable cross-namespace identity."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/namespaces/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespaces

Each namespace is a mini-OpenBao: tenants manage their own secret engines, auth methods, ACL/EGP/RGP policies, password policies, entities, groups and tokens. Namespaces nest (`A/B/C`); delegated admins can create children but cannot escape their namespace.

Manage with the `/sys/namespaces` API or the `namespace` CLI command.

## Addressing

All three reach `ns1/ns2/secret/foo`:

1. path `ns1/ns2/secret/foo`
2. path `secret/foo` with header `X-Vault-Namespace: ns1/ns2/`
3. path `ns2/secret/foo` with header `X-Vault-Namespace: ns1/`

Relative header values are children of the calling namespace.

## Rules

- Names cannot end with `/` or contain spaces.
- Reserved: `.`, `..`, `root`, `sys`, `audit`, `auth`, `cubbyhole`, `identity`.
- Some `sys/` endpoints work only from the root namespace or with an elevated root-namespace token.

## Warning

Entities and groups cannot be referenced across namespaces by default. `unsafe_cross_namespace_identity` enables it for Vault Enterprise compatibility but has no controls on which identities another namespace may reference, allowing unconfined permission sharing. Do not enable it.

## Checked

2026-11-04. Confirmed against the Namespaces overview page: tenant contents, nesting and delegated administrators, naming rules and reserved names, the three addressing examples with X-Vault-Namespace, relative header values, restricted sys endpoints, and the unsafe_cross_namespace_identity warning. Nothing removed.

Method: documentation only; no commands were run.
