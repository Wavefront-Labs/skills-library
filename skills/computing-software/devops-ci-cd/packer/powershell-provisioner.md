---
id: computing-software.devops-ci-cd.packer.powershell-provisioner
name: powershell-provisioner
category: computing-software
field: devops-ci-cd
product: packer
tags: [powershell, windows, provisioner, elevated, prov-powershell]
level: practitioner
status: docs-checked
description: "Run PowerShell on Windows guests, with pwsh option, debug mode, elevated execution and path rules."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/powershell/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `powershell` provisioner runs PowerShell scripts on Windows machines. It is designed for machines using WinRM as the communicator, but can also be used with the SSH communicator.

```hcl
provisioner "powershell" {
  inline = ["dir c:/"]
}
provisioner "powershell" {
  script   = "scripts/install.ps1"
  use_pwsh = true
}
```

Exactly one of `inline` (commands concatenated into one file), `script` (path, relative to Packer's working directory if relative) or `scripts` (uploaded and run in order, each in isolation) is required.

Settings:

- `use_pwsh` (boolean, default false): run `pwsh.exe` instead of `powershell.exe`.
- `debug_mode`: sets PowerShell's PSDebug mode; for instance the value 1 adds `Set-PSDebug -Trace 1` to the execute command.
- `elevated_user` and `elevated_password`: run the script with elevated privileges as the given Windows user. An empty `elevated_password` runs the script as a service account, e.g. `elevated_user = "SYSTEM"`. On AWS, Azure, Google Compute or OpenStack the generated WinRM password is available as `build.Password` in HCL, e.g. `elevated_password = build.Password`.
- `elevated_execute_command` customises the elevated command; `execute_command` customises the normal one. Both default to a `powershell -executionpolicy bypass "& { ... }"` wrapper and accept `{{.Path}}` and `{{.Vars}}`. If you use the SSH communicator with a changed default shell, you may need to adjust `execute_command`.
- `execution_policy` defaults to "bypass"; setting "none" prevents wrapping, which lets you see exit codes on Docker for Windows.
- `environment_vars` (`key=value`) and `env` (map; duplicates override `environment_vars`).
- `valid_exit_codes` defaults to `[0]`; `binary` stops Windows line endings being converted.
- `remote_path` defaults to `/Windows/Temp/script-UUID.ps1` on the C drive; `remote_env_var_path` defaults to `/Windows/Temp/packer-ps-env-vars-UUID.ps1` on the C drive. Both must be writable with existing parent directories.
- `skip_clean` (default false): when true, scripts from non-elevated runs are left on the machine. Elevated scripts, along with their scheduled tasks, are always removed.
- `start_retry_timeout` defaults to `5m`, to cope with restarts; raise it if reboots take longer.
- `pause_after` waits after a successful script.

Path rule: separate paths with a forward slash, especially relative paths. Packer only recognises `/` as a separator when it builds from a non-Windows system and treats backslashes as plain text, which can lead to errors.

## Checked

Method: docs-checked 2026-11-09 against the Packer powershell provisioner page and its included shell configuration and path separator sections (all read as published page source; the environment-variables tail was skimmed). Dropped the windows-restart pairing advice and the sensitive-password advice, which the page does not state.
