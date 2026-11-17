---
id: computing-software.devops-ci-cd.packer.provisioner-block
name: provisioner-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [provisioner, build, hcl2, configuration, block-provisioner]
level: practitioner
status: docs-checked
description: "Provisioner blocks install and configure software on the booted machine, run in order inside a build block."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/provisioner/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `provisioner` block configures one provisioner, which installs and configures software on the machine after it boots and before the image is captured.

```hcl
build {
  provisioner "shell" {
    inline = [
      "echo provisioning all the things",
      "echo the value of 'foo' is '${var.foo}'",
    ]
  }
}
```

The label is the provisioner type, for example `shell`, `file`, `powershell`, `shell-local`, `windows-restart` or `breakpoint`.

Options common to all provisioners, described on the provisioner block page:

- `pause_before`: sleep for a duration before running.
- `max_retries`: times to retry on failure; default 0, meaning no retry.
- `only` / `except`: restrict to listed sources.
- `override`: change settings for a specific source.
- `timeout`: fail the provisioner if it exceeds a duration like `5m`; no timeout by default and no effect in debug mode.
- `continue_on_error`: continue the build after the provisioner fails, applied after `max_retries` is exhausted.

## Checked
2026-11-03. Confirmed against the provisioner block page: purpose, example, `only` / `except`, build-specific `override`, `error-cleanup-provisioner`, `pause_before` (no pause by default), `max_retries` (default zero), `continue_on_error` and `timeout`. Removed `windows-shell` from the type list and the unsourced closing advice.
Method: documentation only; no commands were run.
