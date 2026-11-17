---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.choosing-a-configuration-language
name: choosing-a-configuration-language
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [configuration-language-choice, jsonnet-vs-yaml, configuration-design, jsonnet, cue, dhall, kustomize, helm]
level: advanced
status: draft
description: "Choose a config language: plain YAML/JSON, Helm templating, Kustomize overlays, or Jsonnet/CUE/Dhall, by scale, abstraction and safety needs."
sources: ["https://sre.google/workbook/configuration-specifics/", "https://jsonnet.org/learning/tutorial.html", "https://cuelang.org/docs/", "https://kubectl.docs.kubernetes.io/references/kustomize/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a configuration language

Workbook "Configuration Specifics": configuration grows from simple key/values to needing abstraction
(reuse, templates, computed values). Ad hoc templating of text (string substitution in YAML) causes subtle
bugs; a proper configuration language (Jsonnet is the chapter's example) gives functions, imports and
hermetic evaluation, producing plain data (JSON) for the tool to consume.

## Options
| Approach | Good for | Pain points |
|---|---|---|
| Plain YAML/JSON/TOML | small, few environments | copy-paste duplication; no validation of semantics |
| Text templating (Helm/Go templates, Jinja) | packaging for many installers | indentation bugs, stringly typed, hard to test |
| Overlays/patches (Kustomize) | per-environment variants of K8s manifests | no functions; complex patches get opaque |
| Jsonnet | large configs with reuse; libraries (grafonnet, kube-libsonnet) | learning curve; evaluation errors can be cryptic |
| CUE | schemas + values + validation in one; constraints | newer ecosystem |
| Dhall | strongly typed, total (always terminates) | smaller community |
| General-purpose languages (Pulumi, CDK, cdk8s) | complex logic, existing tooling | can become non-hermetic, side effects |

## Decision guide
1. Fewer than ~5 near-identical variants and no logic: plain YAML + schema validation.
2. Kubernetes variants by environment: Kustomize overlays.
3. Distributing a package to third parties: Helm (with `values.schema.json`).
4. Large internal fleets with shared abstractions (dashboards, alerts, many services): Jsonnet or CUE.
5. Whatever you choose: evaluation must be **hermetic** (no network, no clock) and output plain data that
   is committed or rendered in CI for review.

## Jsonnet example
```jsonnet
local service(name, tier, rps) = {
  name: name,
  replicas: if tier == 'critical' then std.max(3, std.ceil(rps / 300)) else 2,
  alerts: { severity: if tier == 'critical' then 'page' else 'ticket' },
};
{ services: [service('checkout', 'critical', 1500), service('reports', 'batch', 50)] }
```
`jsonnet services.jsonnet | yq -P` renders the data; CI diffs rendered output on every change.

## Gotchas
- Review rendered output, not just source; abstractions hide large effective changes.
- Mixed approaches (Helm + Kustomize + sed) multiply failure modes; standardise per domain.

## Verify
- [ ] Rendered config committed or diffed in CI for every change.
- [ ] Evaluation is reproducible offline.
