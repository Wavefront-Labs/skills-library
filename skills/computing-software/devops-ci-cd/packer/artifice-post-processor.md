---
id: computing-software.devops-ci-cd.packer.artifice-post-processor
name: artifice-post-processor
category: computing-software
field: devops-ci-cd
product: packer
tags: [artifice, artifact, files, post-processor, pp-artifice]
level: advanced
status: docs-checked
description: "Replace a build's artifact with your own file list so later post-processors process it."
sources:
  - "https://developer.hashicorp.com/packer/docs/post-processors/artifice/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `artifice` post-processor replaces the artifact produced by the builder with a list of files you name. Later post-processors in the chain then see those files as the artifact.

```hcl
build {
  sources = ["source.null.example"]
  post-processors {
    post-processor "shell-local" {
      inline = ["echo hello > artifice.txt"]
    }
    post-processor "artifice" {
      files = ["artifice.txt"]
    }
    post-processor "checksum" {
      checksum_types = ["sha256"]
    }
  }
}
```

Setting:

- `files` (required) is a list of files that make up the artifact. They must exist on local disk after provisioning and replace the builder's original artifacts.
- `keep_input_artifact` defaults to `true`: the original artifact files are not deleted.

The docs describe modifying builder artifacts with `shell-local` and passing them to post-processors that may not have worked with the original builder, or downloading a file from the VM with a `file` provisioner and naming it here. Artifice does not delete old artifact files even when it removes them from the artifact; use `shell-local` to delete them.

## Checked
2026-11-03. Confirmed against the artifice post-processor page: it overrides the artifact list for downstream post-processors, `files` is required and must exist locally, `keep_input_artifact` default true, old files are not deleted. Rewrote the settings and use-case text to match the page.
Method: documentation only; no commands were run.
