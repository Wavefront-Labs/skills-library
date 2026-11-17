---
id: computing-software.devops-ci-cd.packer.checksum-post-processor
name: checksum-post-processor
category: computing-software
field: devops-ci-cd
product: packer
tags: [checksum, post-processor, sha256, artifact, pp-checksum]
level: intro
status: docs-checked
description: "Compute md5 or SHA checksums of an artifact with the checksum post-processor and name the output file."
sources:
  - "https://developer.hashicorp.com/packer/docs/post-processors/checksum/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `checksum` post-processor computes checksums for the artifact and writes them to a file.

```hcl
post-processor "checksum" {
  checksum_types = ["sha256", "md5"]
  output         = "packer_{{.BuildName}}_{{.ChecksumType}}.checksum"
}
```

Settings:

- `checksum_types` lists algorithms: `md5` (the default), `sha1`, `sha224`, `sha256`, `sha384`, `sha512`.
- `output` is the file name template. Default: `packer_{{.BuildName}}_{{.BuilderType}}_{{.ChecksumType}}.checksum`.
- Template variables available: `{{.BuildName}}`, `{{.BuilderType}}`, `{{.ChecksumType}}`.
- `keep_input_artifact` keeps the source file.

The docs say to use `{{.ChecksumType}}` in `output` when `checksum_types` has more than one value. All downstream post-processors see the new artifacts.

## Checked
2026-11-03. Confirmed against the checksum post-processor page: algorithms, default `md5`, default `output`, the three template variables. Removed unsourced chaining and publishing advice. `keep_input_artifact` is covered on the post-processor block page.
Method: documentation only; no commands were run.
