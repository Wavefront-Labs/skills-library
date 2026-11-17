---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-audit-match-kind-only-and-opt-out
name: opa-gatekeeper-audit-match-kind-only-and-opt-out
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, audit, match-kind-only, opt-out, scoped, performance]
level: advanced
status: docs-checked
description: "Speed up Gatekeeper audit with --audit-match-kind-only, and opt individual constraints out of audit using scoped enforcement actions."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/audit.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper audit match kind only and opt out

By default audit scans every resource kind in the cluster, which can take a long time. If every constraint names the kinds it targets, set `--audit-match-kind-only=true` so audit only checks the kinds that appear in constraints. For example a single `K8sAllowedRepos` constraint matching only `Pod` restricts audit to Pods. If any constraint omits `kinds`, the flag has no effect and all resources are audited.

All constraints are opted in to audit by default. To opt a constraint out, use `enforcementAction: scoped` and list `scopedEnforcementActions` without the audit enforcement point:

```yaml
spec:
  enforcementAction: scoped
  scopedEnforcementActions:
    - action: warn
      enforcementPoints:
        - name: "validation.gatekeeper.sh"
    - action: deny
      enforcementPoints:
        - name: "gator.gatekeeper.sh"
```

## Checked

2026-11-08. Confirmed against audit.md, read in full (Audit using kinds specified in the constraints only; Opt-out of Audit in constraints): default full scan, --audit-match-kind-only flag and fallback when kinds is missing, scoped opt-out example. Removed or corrected: caveats attributed to the performance guide, which this skill does not cite and which was not read.

Method: documentation only; no commands were run.
