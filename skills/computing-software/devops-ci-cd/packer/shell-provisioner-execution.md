---
id: computing-software.devops-ci-cd.packer.shell-provisioner-execution
name: shell-provisioner-execution
category: computing-software
field: devops-ci-cd
product: packer
tags: [execute-command, sudo, remote-folder, env-var-format, prov-shell-exec]
level: advanced
status: docs-checked
description: "Control how the shell provisioner runs scripts: execute_command, sudo wrapping, remote folder and env var format."
sources:
  - "https://developer.hashicorp.com/packer/docs/provisioners/shell/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The shell provisioner can be customised in how it runs scripts.

Defaults:

- `execute_command`: `chmod +x {{ .Path }}; {{ .Vars }} {{ .Path }}`.
- `inline_shebang`: `/bin/sh -e`.
- `remote_folder`: `/tmp`.
- `remote_file`: `script_nnn.sh`.
- `env_var_format`: `%s='%s' `; with `use_env_var_file` the default is `export %s='%s'` followed by a newline.

To run as root with sudo and a password:

```hcl
provisioner "shell" {
  execute_command = "echo 'packer' | sudo -S sh -c '{{ .Vars }} {{ .Path }}'"
  scripts         = ["./scripts/setup.sh"]
}
```

Template variables inside `execute_command`: `{{ .Path }}` is the script to run, `{{ .Vars }}` the `environment_vars` if configured, `{{ .EnvVarFile }}` the env var file path if `use_env_var_file` is true.

Other options:

- `remote_path` sets the full target path of the uploaded script.
- `use_env_var_file` writes variables to a temporary file and sources it; the docs say it is unnecessary for most cases but may be needed if a custom `execute_command` has extra quoting. The default `execute_command` then becomes `chmod +x {{.Path}}; . {{.EnvVarFile}} && {{.Path}}`.

The docs add that the sudo example fails if environment variables contain spaces or single quotes; then use `echo 'packer' | sudo -S env {{ .Vars }} {{ .Path }}`.

## Checked
2026-11-03. Confirmed against the shell provisioner page: `execute_command` defaults and variables, `inline_shebang`, `remote_folder`, `remote_file`, `remote_path`, `env_var_format`, `use_env_var_file` and the sudo example. Removed the noexec and quoting advice, which the page does not state.
Method: documentation only; no commands were run.
