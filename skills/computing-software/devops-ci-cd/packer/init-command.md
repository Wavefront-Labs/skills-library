---
id: computing-software.devops-ci-cd.packer.init-command
name: init-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [init, plugins, required-plugins, install, cmd-init, plugins-install]
level: practitioner
status: docs-checked
description: "packer init installs the plugins named in required_plugins; usage, file selection, -upgrade and -force."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/init/"
  - "https://developer.hashicorp.com/packer/docs/plugins/install-plugins/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer init` downloads and installs the plugins listed in the `required_plugins` block of an HCL2 template. Run it first on any new or existing template; you can run it repeatedly, and it never deletes plugins that are already installed. Legacy JSON templates are not supported; convert them with `packer hcl2_upgrade`.

```bash
packer init .
packer init template.pkr.hcl
packer init builds/foo/
```

Rules from the docs:

- It processes files ending in `pkr.hcl`.
- Given a single file, that template must contain all its dependencies; the command fails if the template is meant to be built as a bundle of partials.
- Name variable files `.pkrvars.hcl` or `.auto.pkrvars.hcl`; these are excluded automatically when you init a directory.
- `-upgrade` moves installed plugins to the newest version allowed by the template's constraints.
- `-force` reinstalls plugins.

Default install location is `$HOME/.config/packer/plugins` on Unix and `%APPDATA%\packer.d\plugins` on Windows; `PACKER_PLUGIN_PATH` overrides it. Vet third-party plugins before installing. Set `PACKER_GITHUB_API_TOKEN` in CI to avoid GitHub rate limits.

## Checked
2026-11-03. Confirmed against the packer init command page: scope, JSON unsupported, `pkr.hcl` processing, single-file rule, var file naming, `-upgrade`, `-force`, install locations and `PACKER_PLUGIN_PATH`; and the Configure Packer page for `PACKER_GITHUB_API_TOKEN`.
Method: documentation only; no commands were run.
