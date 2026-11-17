---
id: computing-software.devops-ci-cd.packer.shell-provisioner
name: shell-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [shell, provisioner, inline, scripts, prov-shell]
level: practitioner
status: docs-checked
description: "Run commands or scripts on the guest with the shell provisioner, choosing one of inline, script or scripts."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/shell/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `shell` provisioner runs shell scripts on the machine Packer builds, to install and configure software. For Windows images use the PowerShell or Windows Shell provisioners. Exactly one of `inline`, `script` or `scripts` must be set.

```hcl
provisioner "shell" {
  inline = ["echo foo"]
}
provisioner "shell" {
  scripts          = ["./scripts/prepare.sh", "./scripts/install.sh"]
  environment_vars = ["APP_ENV=prod"]
}
```

Options:

- `inline`: commands concatenated by newlines into one file, so they share context. `script`: one path. `scripts`: uploaded and run in order, each in isolation.
- `valid_exit_codes` defaults to `[0]`; `binary` stops Windows line endings being converted.
- `env` map and `environment_vars` (`key=value` list); duplicate `env` settings override `environment_vars`.
- `execute_command` defaults to `chmod +x {{ .Path }}; {{ .Vars }} {{ .Path }}`. With `use_env_var_file = true` it becomes `chmod +x {{.Path}}; . {{.EnvVarFile}} && {{.Path}}`. Available variables: `Path`, `Vars`, `EnvVarFile`.
- `inline_shebang` defaults to `/bin/sh -e`; if customised, keep something like `-e` or failing steps will not fail the provisioner.
- `expect_disconnect` (default false) allows the server to disconnect without an error, such as when SSH restarts or the host reboots.
- `remote_folder` defaults to `/tmp`, `remote_file` to `script_nnn.sh`; `remote_path` overrides both.
- `skip_clean` (default false) keeps the uploaded helper scripts on the machine.
- `start_retry_timeout` (default `5m`) is how long Packer retries to start the remote process, to cope with SSH restarting during a reboot.
- `pause_after` waits after a successful script.

Default environment variables: `PACKER_BUILD_NAME`, `PACKER_BUILDER_TYPE`, and `PACKER_HTTP_ADDR` when the builder provides an HTTP server (hyperv, parallels, qemu, virtualbox, vmware).

Reboots: Packer tolerates restarts by retrying to start scripts. When a command like `reboot` returns before SSH actually quits, use `pause_before` (for example `"10s"`) so Packer waits before running the next script.

Root access: the usual customisation of `execute_command` is dealing with sudo password prompts, for example `"echo 'packer' | sudo -S sh -c '{{ .Vars }} {{ .Path }}'"` (the `-S` flag reads the password from stdin). If environment variables contain spaces or single quotes, use `"echo 'packer' | sudo -S env {{ .Vars }} {{ .Path }}"`. On FreeBSD, whose default shell is `tcsh`, use `chmod +x {{ .Path }}; env {{ .Vars }} {{ .Path }}`.

## Checked

Method: docs-checked 2026-11-09 against the Packer shell provisioner page and its included shell configuration section (read in full as published page source). Corrected `start_retry_timeout`, which retries starting the process, not the upload.
