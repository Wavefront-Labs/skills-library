---
id: computing-software.devops-ci-cd.packer.build-on-error
name: build-on-error
category: computing-software
field: devops-ci-cd
product: packer
tags: [on-error, failure, cleanup, debugging, cmd-build]
level: practitioner
status: docs-checked
description: "Choose what packer build does when provisioning fails: cleanup, abort, ask or run-cleanup-provisioner."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
  - "https://developer.hashicorp.com/packer/docs/debugging/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`-on-error` selects what happens when a build fails during provisioning. It only affects the provisioner run, not the post-processor run, because it decides whether to keep the instance and artifacts such as generated SSH keys.

Values:

- `cleanup` (default) deletes temporary files and virtual machines from the previous steps.
- `abort` exits with no cleanup. The next build may need `-force` because leftovers block it.
- `ask` prompts you to clean up, abort, or retry the failed step.
- `run-cleanup-provisioner` aborts without any cleanup except the `error-cleanup-provisioner`, if one is defined.

```bash
packer build -on-error=ask .
```

The debugging page says `-on-error=ask` lets you inspect failures and try solutions before restarting the build. When a step is retried: the template is not reloaded from file, but the resources specified by builders are reloaded, and the exact behaviour depends on the builder, so check its docs.

## Checked
2026-11-03. Confirmed against the packer build command page (values, default, scope limited to provisioning) and the Debugging Packer Builds page (retry limits). Removed an unsourced closing tip.
Method: documentation only; no commands were run.
