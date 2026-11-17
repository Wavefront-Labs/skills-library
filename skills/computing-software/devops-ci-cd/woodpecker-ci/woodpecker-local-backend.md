---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-local-backend
name: woodpecker-local-backend
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [local-backend, no-isolation, shell]
level: advanced
status: docs-checked
description: "Run Woodpecker steps directly on the agent host with the local backend and its risks."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/backends/local", "https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker local backend

The local backend executes pipelines on the agent host with no isolation. Commands run as the agent's user in the same filesystem, so a malicious pipeline could read the agent configuration, including `WOODPECKER_AGENT_SECRET` (steps do not inherit it but can read it other ways). Use it only for private setups with trusted code and pipelines, never on a public instance, and do not run the agent as root.

Facts:

- Services are not supported.
- Download or build the agent, configure it and run it on the host. Supported on Windows, macOS, FreeBSD and OpenBSD.
- Each workflow uses a random directory under `$TMPDIR`; change it with `WOODPECKER_BACKEND_LOCAL_TEMP_DIR`.
- `WOODPECKER_BACKEND_LOCAL_ISOLATED_HOME` (default true) gives each workflow its own `HOME` and `USERPROFILE`. If false, the user's home is used and no netrc file is written.

Shell: the step `image` names the shell, resolved from `PATH`:

```yaml
steps:
  - name: build
    image: bash
    commands: [...]
```

Override the executable with `WOODPECKER_SHELL_PATH_bash=/custom/path/bash`.

Plugins are executable binaries found in `$PATH` or by absolute path, for example `image: /usr/bin/tree` with no commands.

The default clone step needs the `plugin-git` binary in `$PATH`.

## Checked

2026-11-03. Confirmed against: local backend page (no isolation, services unsupported, TMPDIR, env variables, shell, plugins) and workflow-syntax (default clone needs plugin-git). Removed: the claim that the agent comes from GitHub releases.

Method: documentation only; no commands were run.
