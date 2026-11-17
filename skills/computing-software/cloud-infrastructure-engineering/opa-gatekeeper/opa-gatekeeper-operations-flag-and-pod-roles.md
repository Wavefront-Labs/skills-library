---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-operations-flag-and-pod-roles
name: opa-gatekeeper-operations-flag-and-pod-roles
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, operations, operation-flag, webhook, audit, status, mutation-webhook, generate]
level: sme
status: docs-checked
description: "Split Gatekeeper into separate pods with the --operation flag: webhook, mutation-webhook, audit, status, mutation-status, mutation-controller and generate."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/operations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper operations flag and pod roles

By default, with no `--operation` flag, one Gatekeeper pod does everything. Repeat `--operation` to enable specific functions per deployment, so you can scale them separately and isolate failures (an audit OOM then cannot hurt the validation webhook).

- `webhook`: validating webhook; ingests templates and constraints, creates constraint CRDs, reports status, syncs data from Config, and serves the namespace-label webhook.
- `mutation-webhook`: mutating webhook; ingests mutators and reports their status.
- `audit`: periodic scan; should be a singleton to limit API traffic and status write contention.
- `status`: pods do not talk to each other; each writes its own `ConstraintTemplatePodStatus` and `ConstraintPodStatus`, and this operation aggregates them into `status`. Without it, status is blank. Run as a singleton.
- `mutation-status`: the same for mutators, separate so clusters without mutation CRDs do not error.
- `mutation-controller`: registers mutators; implied by `mutation-webhook` and `mutation-status`, but needed explicitly if `webhook` or `audit` runs alone and you want mutation with workload expansion.
- `generate`: creates CRDs and ValidatingAdmissionPolicies/Bindings; singleton.

RBAC: "Create" includes delete, "Write" includes update, "Read" is get, list and watch.

## Checked

2026-11-08. Confirmed against operations.md, read in full: --operation behaviour and default, each operation key and its role, singleton guidance for audit, status and generate, mutation-controller implication, permission verb meanings. Removed or corrected: nothing.

Method: documentation only; no commands were run.
