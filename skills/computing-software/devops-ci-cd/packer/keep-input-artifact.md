---
id: computing-software.devops-ci-cd.packer.keep-input-artifact
name: keep-input-artifact
category: computing-software
field: devops-ci-cd
product: packer
tags: [keep-input-artifact, artifact, post-processor, block-postprocessor, pp-compress]
level: intro
status: docs-checked
description: "Control whether a post-processor deletes the artifact it consumed using keep_input_artifact."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/post-processor/"
  - "https://developer.hashicorp.com/packer/docs/post-processors/compress/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

By default, the artifact a post-processor receives is automatically deleted once it has processed it. `keep_input_artifact = true` keeps both the input and the new artifact.

```hcl
post-processor "checksum" {
  checksum_types      = ["md5", "sha512"]
  keep_input_artifact = true
}
```

Per-post-processor notes from the docs:

- `compress`: defaults to `false`, so source files are discarded once the archive exists.
- `artifice`: also supports `keep_input_artifact`; it does not delete old artifact files from disk even when it removes them from the artifact list.
- `manifest`: the option does not apply. The input artifact is always retained, because deleting files that were just recorded would be unexpected.

## Checked
2026-11-03. Confirmed against the post-processor block page (default deletion, `keep_input_artifact = true`), the compress page (default false), the artifice page and the manifest page (option does not apply, input always retained). Removed unsourced closing advice.
Method: documentation only; no commands were run.
