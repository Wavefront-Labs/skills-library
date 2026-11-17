---
id: computing-software.devops-ci-cd.concourse-ci.pipeline-resource-types
name: pipeline-resource-types
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [resource-types, defaults, registry-image, privileged, overriding, core-types]
level: practitioner
status: docs-checked
description: "Declare resource types in a pipeline: name, type, source, params, privileged, check_every, tags, defaults merged into source, and overriding core types like registry-image"
sources:
  - https://concourse-ci.org/docs/resource-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A resource type's `type` determines what versions are detected, what a `get` fetches and what a `put` does. Core types such as `git` and `s3` ship with Concourse; the rest come from the community (see the resource types catalog). Pipeline `resource_types` entries:

- `name`: referenced by `resources` and by `task-config.image_resource` in the same pipeline. Using the name of a core type overrides it.
- `type`: the resource type providing the type's container image, usually `registry-image`. It can refer to other resource types and even to the core type being overridden, which lets you bring in a newer or forked `registry-image`.
- `source`: a black box passed to that image resource, e.g. `repository: username/reponame`.
- `privileged` (default `false`): full capabilities, a gaping security hole to be set only if the type's docs require it. It is not chosen by the resource type dynamically, to prevent privilege escalation by third-party exploits.
- `params`: like `get` step params when fetching the type's image.
- `check_every` (default `1m`) and `tags`.
- `defaults`: default config merged with, and overridden by, `resource.source`.

```yaml
resource_types:
  - name: gcs
    type: registry-image
    source:
      repository: frodenas/gcs-resource
    defaults:
      json_key: ((default_key))
resources:
  - name: bucket-c
    type: gcs
    source:
      bucket: c
      json_key: ((different_key))
```

Overriding `registry-image` with `defaults: registry_mirror: host: ...` gives every resource of that type a mirror. The web node can also configure defaults for base resource types.

## Checked

2026-11-04. Fields, defaults and both defaults examples confirmed on the Resource Types page.

Method: documentation only; no commands were run.
