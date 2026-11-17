---
id: computing-software.devops-ci-cd.nomad.constraint-block
name: constraint-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, constraint-block, constraint, distinct-hosts, distinct-property, regexp, set-contains, semver, version, is-set, node-attributes, hcl]
level: practitioner
status: docs-checked
description: "Restrict Nomad placement with constraint blocks covering every operator such as distinct_hosts, distinct_property, regexp, set_contains, version, semver and is_set."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/constraint.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad constraint block

A `constraint` hard-filters eligible nodes by node attribute (`${attr.*}`, `${node.*}`) or client metadata (`${meta.*}`). Valid at `job`, `group` and `task` level, applied hierarchically, so repeating a job constraint in a group is redundant. Editing constraints is a non-destructive update: existing allocations are not moved.

Warning from the docs: irreconcilable constraints make a job unplaceable. All tasks of a group run on one client, so different `${attr.unique.hostname}` constraints on two tasks in the same group can never be satisfied.

```hcl
constraint {
  attribute = "${meta.my_custom_value}"
  operator  = ">"
  value     = "3"
}
```

## Parameters
- `attribute` - the interpolated value to test.
- `operator` (default `"="`) - `=`, `!=`, `>`, `>=`, `<`, `<=`, `distinct_hosts`, `distinct_property`, `regexp`, `set_contains`, `set_contains_any`, `version`, `semver`, `is_set`, `is_not_set`. Ordering operators compare numerically when both sides are integers or both floats, lexically otherwise.
- `value` - literal, attribute or interpolation; required except for `is_set`, `is_not_set`, `distinct_hosts`, `distinct_property` (where it defaults to 1).

## Operators worth knowing
- `distinct_hosts`: no two groups on one machine (job level covers all groups, group level only that group; **not allowed at task level**). Omit `attribute`. Compact form: `distinct_hosts = true`.
- `distinct_property`: at most `value` allocations share a property value, for example `distinct_property = "${meta.rack}"` with `value = "2"` keeps a rack to two instances. Not allowed at task level.
- `regexp` uses RE2 syntax.
- `set_contains` needs **all** comma-separated elements; `set_contains_any` needs any.
- `version` accepts comma lists and the pessimistic operator (`">= 0.1.0, < 0.2"`) but a prerelease like `1.6.0-beta` does not satisfy `>= 1.0`. `semver` is strict Semantic Versioning 2.0 (no pessimistic operator) and does count prereleases.
- `is_set` can be combined with `!=`: by default `!=` also matches nodes lacking the attribute.

## Examples
```hcl
constraint { attribute = "${attr.kernel.version}" operator = "version" value = "> 3.19" }
constraint { attribute = "${attr.platform.aws.instance-type}" value = "m4.xlarge" }
constraint { attribute = "${meta.cached_binaries}" set_contains = "redis,cypress,nginx" }
```
For soft preferences use `computing-software.devops-ci-cd.nomad.affinity-block` instead.

## Checked

2026-11-03. Confirmed against the constraint job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
