---
id: computing-software.cloud-infrastructure-engineering.openbao.seal-migration
name: seal-migration
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, seal-migration, migrate, downtime, disabled]
level: advanced
status: docs-checked
description: "Migrate an OpenBao cluster between seal mechanisms: prerequisites, the disabled seal block, unseal -migrate and standby ordering."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/seal.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seal migration

## Before you start

- Migration needs cluster downtime. Take a backup first.
- Both the old and the new seal must be available during migration.
- Migrating AWSKMS to AWSKMS is not supported. Other same-type migrations are.

## Procedure (from the seal concepts page)

1. Update the seal configuration on one standby at a time, marking the old seal block `disabled = "true"` where needed.
2. Unseal each node with the `-migrate` flag:

```
bao operator unseal -migrate
```

3. Step down the active node so a standby takes over and performs the migration.
4. Update the former active node's config, then restart the remaining nodes.

## Gotchas

- Both seals must stay available throughout, so keep the old seal's backing service reachable until every node is done.
- Auto-unseal clusters use recovery keys; see auto-unseal-and-recovery-keys.

## Checked

2026-11-04. Confirmed against the Seal migration section of the Seal/Unseal concepts page: downtime, backup, both seals available, the AWSKMS to AWSKMS limitation, disabled = "true" on the old seal block, unseal -migrate, standby ordering and stepping down the active node. Nothing removed.

Method: documentation only; no commands were run.
