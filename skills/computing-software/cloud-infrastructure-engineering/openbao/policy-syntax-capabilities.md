---
id: computing-software.cloud-infrastructure-engineering.openbao.policy-syntax-capabilities
name: policy-syntax-capabilities
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, policy, capabilities, acl, deny]
level: practitioner
status: docs-checked
description: "Write OpenBao ACL policies: path blocks, capabilities mapped to HTTP verbs, parameter constraints, deny and expiration."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/policies.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy syntax and capabilities

Policies are HCL or JSON and deny by default; an empty policy grants nothing. Each `path` block lists `capabilities`, and may set `allowed_parameters`, `denied_parameters` or `required_parameters`. Optional `comment` documents a rule; optional `expiration` (RFC3339) removes access at a set time.

## Capabilities

- `create` (POST/PUT), `read` (GET), `update` (POST/PUT), `patch` (PATCH), `delete` (DELETE)
- `list` (LIST) and `scan` (SCAN, recursive list): returned keys are not filtered by policy by default, so never put sensitive data in key names
- `sudo`: needed in addition for root-protected paths
- `deny`: always wins, even over `sudo`

Capabilities map to HTTP verbs, not to the action's meaning. Generating database credentials is a GET, so it needs `read`.

## Commands

```
bao policy write policy-name policy-file.hcl
bao read sys/policy
bao delete sys/policy/policy-name
```

Deleting is idempotent.

## Gotchas

- `allowed_parameters`, `denied_parameters` and `required_parameters` are not supported for KV v2 policies.
- Default values are not considered during parameter evaluation.
- Parameter globbing can allow unintended values, such as comma-separated lists.
- `list_scan_response_keys_filter_path` can filter list and scan results, but the page warns the result may be completely empty when evaluating individual entries needs additional parameters.

## Checked

2026-11-04. Read the OpenBao policies concepts page in full. Confirmed: deny by default, capability list with HTTP verbs, `sudo` and `deny` semantics, the verb-versus-action warning, `expiration` in RFC3339, `comment`, the policy write, list and delete commands, idempotent delete, the KV v2 limitation, default values not considered, glob caveat. Removed: the claim that results are empty in some unspecified configurations (replaced with the page's actual condition).
Method: documentation only; no commands were run.
