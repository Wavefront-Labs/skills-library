---
id: computing-software.cloud-infrastructure-engineering.openbao.self-initialization
name: self-initialization
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, self-init, initialize, declarative, request]
level: advanced
status: docs-checked
description: "Bootstrap OpenBao declaratively with the initialize stanza: request blocks, ordering, auto-unseal requirement and no root token."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/self-init.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-initialization

Requests in the `initialize` stanza run once on first start, so mounts, auth and audit are set up without manual API calls. They obey normal rules (auditing, authentication, API restrictions).

```hcl
initialize "audit" {
  request "enable-audit" {
    operation = "update"
    path = "sys/audit/stdout"
    data = {
      type = "file"
      options = {
        file_path = "stdout"
      }
    }
  }
}
```

## request keys

`operation` (required), `path` (required), `token` (optional, defaults to the root token), `data` (map), `allow_failure` (default false). Names match `^[A-Za-z_][A-Za-z0-9_-]*$`.

## Rules

- `initialize` stanzas run in file order; requests inside run in listed order.
- No two blocks of the same type share a name.
- Requires an auto-unseal mechanism. No recovery keys are generated; use the authenticated recovery key rotation endpoints if you need them.
- The root token is never returned and is revoked after use.
- It runs once; to repeat, remove all storage and initialize again.

## Warnings

`TRACE` logging records every request and response with sensitive data. Failures are logged; check logs for partial failures.

## Checked

2026-11-04. Read the OpenBao self-initialization (initialize stanza) page in full. Confirmed: the example block, the `request` parameters and defaults, the name regex, stanza ordering, the auto-unseal requirement, no recovery keys, root token not returned and revoked after use, the run-once behaviour and the `TRACE` warning. Removed: the claim that recovery keys should be rotated later (the page points to the authenticated rotation endpoints).
Method: documentation only; no commands were run.
