---
id: computing-software.cloud-infrastructure-engineering.openbao.control-groups
name: control-groups
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, control-group, approval, accessor, second-party]
level: advanced
status: docs-checked
description: "Require second-party approval for OpenBao requests with a control_group policy stanza, accessor hand-off and unwrap."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/control-groups.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control groups

A policy factor requires approval before a secret is released or certificate generated. A triggering request gets a wrapped response with a token and accessor. OpenBao stores the original request and runs it only after the approved wrapping token is unwrapped.

## Policy

```hcl
control_group = {
  factor "pki-approvers" {
    controlled_capabilities = ["update"]
    identity {
      group_names = ["pki-approvers", "security-team"]
      approvals = 1
      ttl = "5d"
      self_authorization = false
    }
  }
}
```

- `controlled_capabilities` limits which operations trigger the factor; omitted means all operations on the path. Must be a subset of the policy's `capabilities`.
- `self_authorization` defaults to false.

## Flow

- `sys/control-group/request`: review the original request by accessor
- `sys/control-group/authorize`: approve by accessor
- `sys/wrapping/unwrap`: execute once approved

## Gotchas

OpenBao sends no notification to approvers; the requester must pass them the accessor. A requester who is in the approving group needs a different approver unless self-authorization is on.

## Checked

2026-11-04. Confirmed against the Control groups page: the workflow, wrapped response with token and accessor, no approver notification, the three sys paths, the factor policy example, controlled_capabilities rules and the self_authorization default of false. Nothing removed.

Method: documentation only; no commands were run.
