---
id: computing-software.devops-ci-cd.concourse-ci.put-step
name: put-step
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [put-step, steps, implicit-get, inputs, get-params, no-get, resource]
level: practitioner
status: docs-checked
description: "Configure a put step: the implicit get that follows it, how inputs detect/all/list controls which artifacts are streamed, params, get_params such as skip_download, and no_get."
sources:
  - https://concourse-ci.org/docs/steps/put/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `put` step pushes to a resource. When it succeeds, the version it created is immediately fetched by an implicit `get`, so later steps can use the artifact under the identifier given to `put`. `resource` (default: the `put` value) lets you give the artifact a different name than the pipeline resource, for example `put: thecode` with `resource: repo`.

**`inputs`** controls which build artifacts are streamed into the put container (default `detect`):
- `detect`: artifacts are inferred from the `params` by taking all string values and using the first path segment as an identifier. With `file: ci/version.txt` only `ci` is streamed.
- `all`: every artifact is provided. This can be slow if earlier steps registered large artifacts, so be explicit if you can.
- a list of identifiers: only those artifacts are provided.

`params` configure the put and depend on the resource type. `get_params` configure the implicit get. For a `registry-image` put that should not download the image:

```yaml
plan:
  - put: app-image
    params:
      build: git-resource
    get_params:
      skip_download: true
```

`no_get: true` skips the implicit get entirely. Set it when the put is at the very end of the job and nothing uses the fetched artifact.

## Checked

2026-11-04. Defaults, inputs modes, get_params and no_get confirmed on the Put Step page.

Method: documentation only; no commands were run.
