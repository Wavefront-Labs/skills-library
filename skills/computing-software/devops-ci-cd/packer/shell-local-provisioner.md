---
id: computing-software.devops-ci-cd.packer.shell-local-provisioner
name: shell-local-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [shell-local, provisioner, host, execute-command, prov-shelllocal]
level: practitioner
status: docs-checked
description: "Run commands on the machine running Packer with shell-local, including the default execute_command per platform."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/shell-local/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `shell-local` provisioner runs shell scripts on the machine where Packer is running, not on the guest. The remote `shell` provisioner runs scripts on the remote machine.

```hcl
provisioner "shell-local" {
  inline = ["echo hello from the build host"]
}
```

Exactly one of these is required:

- `command`: a single command, written to a temporary file and run with `execute_command`.
- `inline`: array of commands concatenated by newlines into one file, so they share context (a `cd` carries over).
- `script`: path to a script, absolute or relative to Packer's working directory.
- `scripts`: scripts run in order; each runs in isolation, so state does not carry over.

Optional settings:

- `env` map and `environment_vars` (`key=value` strings) are injected before `execute_command`; duplicate `env` settings override `environment_vars`.
- `env_var_format` defaults to `set %s=%s &&` on Windows hosts and `%s='%s'` on Unix.
- `execute_command` defaults to `["/bin/sh", "-c", "{{.Vars}}", "{{.Script}}"]` on Unix and `["cmd", "/c", "{{.Vars}}", "{{.Script}}"]` on Windows. Available variables are `Script` (path to the script) and `Vars` (the `environment_vars`). The first element must be the shell program and a later element must be `{{.Script}}`. Other shells are not officially supported.
- `inline_shebang` defaults to `/bin/sh -e`; if customised, keep something like `-e` or failing steps will not fail the provisioner.
- `only_on` lists runtime operating systems where it runs; if unset it always runs.
- `use_linux_pathing` (Windows hosts with WSL) makes Packer use the Linux path (`/mnt/c/...`) for a bash script, together with an `execute_command` such as `["bash", "-c", "{{.Vars}} {{.Script}}"]`. With WSL, `inline` and `command` are not available; use `script` or `scripts`.
- `valid_exit_codes` defaults to `0`.
- `tempfile_extension` is needed for inline commands on Windows (for example `.cmd` or `.ps1`).

On Windows builds on AWS, Azure, Google Compute or OpenStack, `{{.WinRMPassword}}` exposes the generated WinRM password, for example `"WINRMPASS={{.WinRMPassword}}"` in `environment_vars`.

Default environment variables include `PACKER_BUILD_NAME`, `PACKER_BUILDER_TYPE` and `PACKER_HTTP_ADDR` (set when the builder provides an HTTP server, such as hyperv, parallels, qemu, virtualbox and vmware).

Safe-scripting notes from the docs:

- The scripts run once per builder: with an amazon-ebs and a docker builder, they run twice.
- If any provisioner fails, `packer build` stops and interim artifacts are cleaned up, so a shell script must exit with a zero code; be careful to `exit 0` when necessary.

## Checked

Method: docs-checked 2026-11-09 against the Packer shell-local provisioner page (read in full as published page source). Dropped the unconfirmed build.Host/Ansible aside and the post-processor comparison.
