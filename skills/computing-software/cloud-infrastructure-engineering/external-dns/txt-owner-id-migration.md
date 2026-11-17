---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-owner-id-migration
name: txt-owner-id-migration
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, migrate-from-txt-owner, txt-owner-id, ownership-migration, dry-run]
level: advanced
status: docs-checked
description: "Change an ExternalDNS TXT owner ID with --migrate-from-txt-owner, preview it with --dry-run, and know the default owner value."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TXT owner ID migration

The owner ID stored in registry TXT records can be changed. Setting `--migrate-from-txt-owner` enables migration checks in the run loop, using the new `--txt-owner-id` and the old value you name.

Before:
```yaml
args:
- "--txt-prefix=%{record_type}-"
- "--txt-owner-id=old-owner"
- "--policy=sync"
- "--registry=txt"
```

After:
```yaml
args:
- "--txt-prefix=%{record_type}-"
- "--txt-owner-id=new-owner"
- "--migrate-from-txt-owner=old-owner"
- "--policy=sync"
- "--registry=txt"
```

- If you never set an owner ID, ExternalDNS used `default`; set `--migrate-from-txt-owner=default` to migrate those records.
- Preview first: add `--dry-run` alongside `--migrate-from-txt-owner` and read the planned changes.
- The docs warn that automating DNS migration is risky because DNS is business-critical; plan it deliberately.
- The example deployment uses one replica with `strategy: type: Recreate`.

**Shared zones:** do not use this casually where several clusters share a zone. See the shared-zone owner migration skill.

**Verify:** after rollout, registry TXT values contain `external-dns/owner=new-owner` and no records are deleted.

## Checked

2026-11-04. Read the TXT registry page (OwnerID migration). Confirmed --migrate-from-txt-owner, the default owner value, the --dry-run preview, the before/after args and the business-critical warning. Removed the claim that Recreate guarantees two owners never run together, which the page does not state.

Method: documentation only; no commands were run.
