---
id: computing-software.devops-ci-cd.packer.post-processor-block
name: post-processor-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [post-processor, artifact, build, hcl2, block-postprocessor]
level: practitioner
status: docs-checked
description: "Post-processors take a build's artifact and upload, repackage or record it; syntax and per-source filtering."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/post-processor/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `post-processor` block configures one post-processor. Each runs after each defined build, takes the artifact from the build, and may upload, repackage or otherwise process it.

```hcl
build {
  post-processor "checksum" {
    checksum_types      = ["md5", "sha512"]
    keep_input_artifact = true
  }
  post-processor "amazon-import" {}
}
```

Points from the docs:

- By default the input artifact is deleted after the post-processor. Set `keep_input_artifact = true` to keep both.
- `only` / `except` restrict a post-processor to sources, by source name rather than builder type.
- On the command line, `-except` removes a post-processor by `name`, which defaults to its type; give a `name` to make it unique. `-only` does not work for post-processors.
- Contextual `build` variables are available inside the block.
- Post-processors can take the artifact from another post-processor when chained in a `post-processors` block.

Several `post-processor` blocks directly in a build all start from the builder's artifact. If you want one to consume another's output, use `post-processors` instead.

## Checked
2026-11-03. Confirmed against the post-processor block page: when post-processors run, default deletion of the input artifact, `keep_input_artifact`, `only` / `except` by source name, `-except` by post-processor name, `-only` not working for post-processors, build contextual variables, and chaining via `post-processors`.
Method: documentation only; no commands were run.
