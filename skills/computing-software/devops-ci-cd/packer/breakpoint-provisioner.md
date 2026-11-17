---
id: computing-software.devops-ci-cd.packer.breakpoint-provisioner
name: breakpoint-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [breakpoint, debugging, provisioner, pause, prov-breakpoint]
level: intro
status: docs-checked
description: "Pause a build at a chosen point with the breakpoint provisioner and resume with Enter."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/breakpoint/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `breakpoint` provisioner pauses the build at its position until you press the Enter key, to help you debug errors.

```hcl
provisioner "breakpoint" {
  note = "check the installed packages before continuing"
}
```

Options (both optional):

- `disable` (boolean, default `false`): if `true`, the breakpoint is skipped. Useful when you have set several breakpoints and want to toggle them off or on.
- `note` (string): text explaining the purpose or location of the breakpoint, for example a number or a label for where in the build it sits.

When the build reaches it, the UI prints the note and a prompt:

```
==> docker: Pausing at breakpoint provisioner with note "foo bar baz".
==> docker: Press enter to continue.
```

After you press Enter the build resumes and runs normally until it completes or errors.

An alternative is `packer build -debug`, which disables parallelisation and halts the operation at every step and between every provisioner. A breakpoint stops only where you put it.

Because the build waits for keyboard input, set `disable = true` or remove the provisioner before unattended runs.

## Checked

Method: docs-checked 2026-11-09 against the Packer breakpoint provisioner page and the `packer build` command page, read as the published page source (full text). Dropped unconfirmed claims about other sources being unaffected and about connecting by ssh.
