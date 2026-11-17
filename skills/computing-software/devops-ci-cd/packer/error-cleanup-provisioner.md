---
id: computing-software.devops-ci-cd.packer.error-cleanup-provisioner
name: error-cleanup-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [error-cleanup-provisioner, failure, cleanup, build, block-provisioner, cmd-build]
level: advanced
status: docs-checked
description: "Define one provisioner that runs only if provisioning fails, before the instance is shut down."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/provisioner/"
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An `error-cleanup-provisioner` is a single specialized provisioner that runs only when the normal provisioning run fails. It runs before the instance is shut down, so you can make last-minute changes and clean up things Packer cannot, such as unsubscribing a machine from a service it registered with during the build.

```hcl
build {
  sources = ["source.null.example"]
  provisioner "shell-local" {
    inline = ["echo registering"]
  }
  error-cleanup-provisioner "shell-local" {
    inline = ["echo cleaning up"]
  }
}
```

It is a single specialized provisioner: you create one `error-cleanup-provisioner` per build, not a list.

It interacts with `-on-error` (which affects only the provisioner run, not post-processors):

- `cleanup` (default) cleans up the previous steps, deleting temporary files and virtual machines.
- `abort` exits without any cleanup, which might require the next build to use `-force`.
- `ask` prompts you to clean up, abort or retry the failed step.
- `run-cleanup-provisioner` aborts and exits without any cleanup besides the error-cleanup-provisioner, if one is defined.

The documented use is making sure the instance is properly unsubscribed from any services it connected to during the build.

## Checked

Method: docs-checked 2026-11-09 against the Packer provisioner block page (On Error Provisioner section, whole page read) and the `packer build` command page (-on-error flag), read as published page source. Dropped the unconfirmed claims about licence release, credential revocation and idempotence.
