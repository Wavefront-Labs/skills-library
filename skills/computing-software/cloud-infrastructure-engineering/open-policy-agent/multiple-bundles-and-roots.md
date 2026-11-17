---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.multiple-bundles-and-roots
name: multiple-bundles-and-roots
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [bundles, roots, manifest, multi-source, bundle-conflicts]
level: advanced
status: docs-checked
description: "Load policy and data from several OPA bundles by giving each a manifest roots list, the validation rules, and why central aggregation is preferred."
sources:
  - https://www.openpolicyagent.org/docs/management-bundles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let separate teams or services own separate parts of OPA's policy and data.

By default a bundle defines the entire policy and data cache. To scope it, add a top-level `roots` key to the bundle manifest listing the `data` paths the bundle owns:

```json
{
    "roots": ["acmecorp/policy", "acmecorp/oncall"]
}
```

OPA then erases and overwrites only policy and data under those roots; content under other roots is left intact.

Validation when loading scoped bundles:
- roots must not overlap (`a/b/c` and `a/b` overlap and error); this is not enforced across different bundles, only within one manifest
- policies in the bundle must live under its roots

Prefer central aggregation. The docs warn that with multiple sources there are no ordering guarantees for which bundle loads first and takes over a root, and if bundles conflict but load at different times OPA may enter an error state. Use multiple sources only when aggregation is impractical, for example for latency reasons.

Mitigation: the docs highly recommend the health check with bundle state (see policy-api-and-health-checks) to detect this.

Check: start OPA with two bundles on disjoint roots and confirm both appear under `data`; policy outside a bundle's declared roots is rejected by validation.

## Checked

2026-11-04. Confirmed against the Bundles page section Multiple Sources of Policy and Data: roots key, erase-and-overwrite only under the roots, overlap rule (within one manifest only), policies and data must be contained under the roots, no load-order guarantee and possible error state, recommendation to use the health check with bundle state. The skill originally listed only two validation rules; the page also requires data to be under the roots (not contradicted). Nothing removed.

Method: documentation only; no commands were run.
