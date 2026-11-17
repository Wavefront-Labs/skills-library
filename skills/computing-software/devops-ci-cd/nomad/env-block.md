---
id: computing-software.devops-ci-cd.nomad.env-block
name: env-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, env-block, env, environment-variables, interpolation, hcl2, dotted-keys, template-env]
level: intro
status: docs-checked
description: "Set task environment variables in Nomad with the env block including type coercion, interpolation, dashes becoming underscores and map syntax for keys containing dots."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/env.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad env block

`env` (task level, also accepted at job and group per the placement list) injects environment variables before the task starts.

```hcl
task "server" {
  env {
    my_key     = "my-value"
    NODE_CLASS = "${node.class}"
  }
}
```

## Rules
- Any key/value is accepted. Keys and values are stored as strings; numbers and bools are coerced (`key = 1.4`, `key = "1.4"` and `key = true` all become strings, no type information is kept).
- Invalid characters in names, such as dashes, are converted to underscores.
- Values may use Nomad interpolation, for example `${node.class}`.
- Names that are not valid HCL2 identifiers (for example containing `.`) need map assignment syntax:

```hcl
env = {
  "discovery.type" = "single-node"
}
```

## Dynamic values
Nomad can populate dynamic environment variables from data stored in Consul and Vault; see the `template` block documentation.

## Related
Job `meta` values are also exposed as environment variables (`computing-software.devops-ci-cd.nomad.meta-block`).

## Checked

2026-11-03. Confirmed against the Nomad 1.10 env job specification page: placements, coercion, dash conversion, interpolation, dotted-name map syntax. Removed: the env = true template detail.

Method: documentation only; no commands were run.
