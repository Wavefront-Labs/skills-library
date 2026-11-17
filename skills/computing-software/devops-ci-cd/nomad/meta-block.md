---
id: computing-software.devops-ci-cd.nomad.meta-block
name: meta-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, meta-block, meta, nomad-meta, metadata, interpolation, template-env, hcl]
level: intro
status: docs-checked
description: "Attach user-defined metadata in Nomad with meta blocks at job, group and task level, merge rules, key character conversion and reading NOMAD_META values in templates."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/meta.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad meta block

`meta` holds arbitrary user key/values at `job`, `group` or `task` level.

```hcl
job "docs" {
  meta { my-key = "job-value" }
  group "example" {
    meta { team = "sre" }
    task "server" {
      meta { class = "${node.class}" }
    }
  }
}
```

## Behaviour
- Metadata merges downward: job meta applies to every group and task, group meta to the group's tasks.
- Values become runtime environment variables inside tasks (`NOMAD_META_<key>`).
- Keys and values are strings; other types coerce (`key = true`, `key = 1.4`). Any key character outside `[A-Za-z0-9_.]` is converted to `_`.
- Interpolation like `"${node.class}"` is allowed.
- Keys that are not HCL2 identifiers (for example with a dot) use map syntax:

```hcl
meta = {
  "project.team" = "sre"
}
```

## In a template
Use the environment form: `{{ env "NOMAD_META_mykey" }}`.

## Related
Parameterized jobs read dispatch metadata the same way (`computing-software.devops-ci-cd.nomad.parameterized-block`). Client-side metadata for constraints is a different thing (`${meta.*}` node attributes in `computing-software.devops-ci-cd.nomad.constraint-block`).

## Checked

2026-11-03. Confirmed against the Nomad 1.10 meta job specification page: levels, merge direction, environment variable exposure, string coercion, character conversion, interpolation, dotted-key map syntax, the template example. Nothing removed.

Method: documentation only; no commands were run.
