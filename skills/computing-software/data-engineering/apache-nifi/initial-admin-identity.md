---
id: computing-software.data-engineering.apache-nifi.initial-admin-identity
name: initial-admin-identity
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, initial-admin, fileaccesspolicyprovider, node-identity, policies]
level: practitioner
status: docs-checked
description: "Seed the first NiFi administrator and cluster node identities in FileAccessPolicyProvider, and why the admin must grant themselves root group policies on a new flow."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initial admin and node identities

In `authorizers.xml`, `FileAccessPolicyProvider` accepts:
- `Initial Admin Identity`: applied only when no policies exist; cannot be combined with `Legacy Authorized Users File`.
- `Legacy Authorized Users File`: converted on first use.
- `Node Identity` (one per node, unique property names) and `Node Group`.
- `Authorizations File` (example `./conf/authorizations.xml`).

Steps: set the identity, restart; NiFi writes the user and policies to `users.xml` and `authorizations.xml`. The admin can then manage users, groups and policies.

Rules:
- Identities must exist in the referenced User Group Provider and be unmapped, such as the full certificate DN.
- On a brand-new flow the admin must grant themselves policies on the root process group before editing it. Upgrades from an existing `flow.json.gz` grant flow-modify automatically.

Verify: after the restart, the admin appears in `users.xml` and `authorizations.xml` and can manage users, groups and policies in the UI.

## Checked

Checked against the NiFi Administration Guide, FileAccessPolicyProvider properties and Initial Admin Identity (New NiFi Instance) sections: property names and exclusivity with the legacy file, the no-existing-policies rule, unique Node Identity names, Node Group, the unmapped-identity rule, the root process group caveat and the upgrade exception match. The proxy-policy wording in the verify step was removed as unsourced.

Method: docs-only read of cited pages, 2026-11-08
