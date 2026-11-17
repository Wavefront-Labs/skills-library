---
id: computing-software.devops-ci-cd.packer.post-processors-chain
name: post-processors-chain
category: computing-software
field: devops-ci-cd
product: packer
tags: [post-processors, chain, sequence, artifact, block-postprocessors]
level: advanced
status: docs-checked
description: "Chain post-processors so each consumes the previous artifact, and how it differs from separate blocks."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/post-processors/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `post-processors` block groups `post-processor` blocks into a chain: the first takes the build's artifact, the next takes the first's output, and so on.

```hcl
build {
  post-processors {
    post-processor "shell-local" {
      inline = ["echo hello > artifice.txt"]
    }
    post-processor "artifice" {
      files = ["artifice.txt"]
    }
    post-processor "checksum" {
      checksum_types      = ["md5", "sha512"]
      keep_input_artifact = true
    }
  }
}
```

Separate `post-processor` blocks directly in `build` all start from the same artifact and run independently. To make the checksum work on the artifice output you need them in one `post-processors` block.

Multiple `post-processors` blocks are separate chains. In the docs' example, three blocks, one each for checksum, amazon-import and googlecompute-import, are equivalent to three plain `post-processor` blocks. Each chain starts after each build, that is, after each provision step has run on each source, and the source image is deleted in all cases.

A skipped post-processor stops its chain: with `-except`, any post-processor following a skipped one does not run, though other chains still do.

## Checked
2026-11-03. Confirmed against the post-processors block page (chain example, equivalence of three plain blocks and three `post-processors` blocks, start after each build, source image deleted) and the build command page (`-except` behaviour). Replaced the word parallel, which the page does not use.
Method: documentation only; no commands were run.
