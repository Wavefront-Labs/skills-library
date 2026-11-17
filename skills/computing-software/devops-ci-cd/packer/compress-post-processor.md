---
id: computing-software.devops-ci-cd.packer.compress-post-processor
name: compress-post-processor
category: computing-software
field: devops-ci-cd
product: packer
tags: [compress, archive, tar, gzip, pp-compress]
level: practitioner
status: docs-checked
description: "Compress artifact files into zip, tar, gz or lz4 archives with the compress post-processor."
sources:
  - "https://developer.hashicorp.com/packer/docs/post-processors/compress/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `compress` post-processor builds an archive from the artifact's files.

```hcl
post-processor "compress" {
  output              = "image_{{.BuildName}}.tar.gz"
  compression_level   = 9
  keep_input_artifact = false
}
```

The format is inferred from the output file extension: `.zip`, `.tar`, `.gz`, `.tar.gz`, `.lz4`, `.tar.lz4`. `.gz` and `.lz4` fail if there are multiple files to compress. Without a detectable extension it behaves as `.tar.gz` but keeps the filename; `format` disables the autodetection.

Settings:

- `output` sets the file name. Default: `packer_{{.BuildName}}_{{.BuilderType}}`.
- `compression_level` runs from 1 to 9 and defaults to 6; a larger number compresses harder and runs slower.
- `keep_input_artifact` defaults to false, so the source files are discarded once the archive exists.

Template variables: `{{.BuildName}}` and `{{.BuilderType}}`.

With parallel builders make `output` unique for each, for example `packer_{{.BuildName}}.zip`.

## Checked
2026-11-03. Confirmed against the compress post-processor page: default archive and name, format inference, supported extensions, `compression_level` 1-9 default 6, `keep_input_artifact` default false and the template variables. Removed unsourced chaining advice.
Method: documentation only; no commands were run.
