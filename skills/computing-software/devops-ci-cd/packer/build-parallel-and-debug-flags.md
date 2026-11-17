---
id: computing-software.devops-ci-cd.packer.build-parallel-and-debug-flags
name: build-parallel-and-debug-flags
category: computing-software
field: devops-ci-cd
product: packer
tags: [parallel-builds, debug, pem-key, ssh, cmd-build, debugging]
level: practitioner
status: docs-checked
description: "Limit concurrency with -parallel-builds and step through a build with -debug, which also emits an SSH key."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
  - "https://developer.hashicorp.com/packer/docs/debugging/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Two flags change how a build executes.

`-parallel-builds=N` limits how many builds run at once. The default `0` means no limit, so every source in the template starts together.

`-debug` disables parallelization and enables builder debug mode. Builders usually pause between steps and wait for a keypress so you can inspect state. For cloud builders Packer writes the ephemeral private SSH key to the current directory as a `.pem` file, so you can connect while it is paused:

```bash
packer build -debug .
ssh -i key.pem user@instance
```

The key is deleted at the end of the run during cleanup, and is only emitted for cloud-based builders. For local builders, set `PACKER_LOG=1` to see the SSH session details, and log in with the user and password from the kickstart or preseed file.

On Windows, the WinRM communicator in debug mode emits the Remote Desktop password after the instance boots (several minutes), and decrypts it for you.

For a pause at one chosen point rather than at every step, add a `breakpoint` provisioner.

## Checked
2026-11-03. Confirmed against the packer build command page and the Debugging Packer Builds page: `-parallel-builds`, `-debug`, the emitted `.pem` key, `PACKER_LOG=1` for local builders and the WinRM Remote Desktop password. Removed an unsourced sentence on when to lower concurrency.
Method: documentation only; no commands were run.
