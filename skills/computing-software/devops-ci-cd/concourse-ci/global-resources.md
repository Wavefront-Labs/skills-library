---
id: computing-software.devops-ci-cd.concourse-ci.global-resources
name: global-resources
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [global-resources, resource-config, check, version-history, time-resource, iam, intercept]
level: advanced
status: docs-checked
description: "Understand global resources: versions shared by resources with identical type and source, the check savings, and risks for time resources, IAM credentials and check containers."
sources:
  - https://concourse-ci.org/docs/operation/global-resources/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With global resources enabled (introduced in v5.0.0), resource versions are attached to an anonymous resource config, meaning the `resource.type` plus `resource.source`, instead of to a resource name per pipeline.

**Benefits.**
- Fewer checks: resources with identical configuration share one version history and one check interval. Three teams with the same resource config used to mean three check containers and three checks a minute; now there is one. The shortest `resource.check_every` among them decides how often the shared check runs.
- Less redundant data: a git resource on the same repository always returns the same versions.
- Reliable history: changing `type` or `source` resets the versions, rather than appending new versions after stale ones as the per-name model did.

**Complications.** Resources with `resource.tags`, and teams with their own workers, are exceptions to container sharing: a check container may be reused from elsewhere if one exists, otherwise one is created on a matching worker. The page says this is hard to reason about and plans to stop reusing check containers.

**Risks.**
- The `time` resource would cause a thundering herd if shared (everyone with a 10-minute interval fires together). The stated direction is modelling time as a `var_source`.
- Resource types that learn credentials outside `source:` (such as IAM roles) must not share history, or someone could configure the same source without credentials and see versions another pipeline discovered.
- Intercepting check containers is limited to admin users, since they are shared across teams.

## Checked

2026-11-04. Benefits, complications and risks confirmed on the Global Resources page.

Method: documentation only; no commands were run.
