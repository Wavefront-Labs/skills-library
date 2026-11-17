---
id: computing-software.devops-ci-cd.skaffold.global-skaffold-config
name: global-skaffold-config
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [config, global, set, context, user-settings]
level: practitioner
status: docs-checked
description: "Store per-user and per-context settings in the Skaffold global config with skaffold config set."
sources:
  - "https://skaffold.dev/docs/design/global-config/"
  - "https://skaffold.dev/docs/environment/env-file/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

User-level settings live in the global config file, `~/.skaffold/config` by default, managed with `skaffold config`:

```bash
skaffold config set default-repo <myrepo>
skaffold config set --kube-context <mycluster> local-cluster true
skaffold config set --global insecure-registries localhost:5000
skaffold config list
skaffold config unset insecure-registries
```

`skaffold config` has the subcommands `list`, `set` and `unset`. `set` and `unset` take `-g/--global` and `-k/--kube-context`; `list` takes `-a/--all` (show values for all kube-contexts) and `-k`. `-c/--config` points at another config file.

Documented options: `default-repo`, `multi-level-repo`, `debug-helpers-registry`, `insecure-registries`, `k3d-disable-load`, `kind-disable-load`, `local-cluster`, `update-check` and `collect-metrics`. Note `local-cluster`: when true, Skaffold does not try to push images after building; by default the contexts `docker-for-desktop`, `docker-desktop` and `minikube` count as local.

Scope: options can be set globally or for specific Kubernetes contexts, and context name matching supports regular expressions, for example `.*-cluster.*-regex.*-test.*`. Without `--global`, `set` applies to the current kube-context (or the one given with `-k`); `--global` applies to every context.

Environment alternatives: set a flag with `SKAFFOLD_` plus the upper-case flag name (`SKAFFOLD_CACHE_ARTIFACTS=true`). A `skaffold.env` file in the project root holds `KEY=value` lines that Skaffold loads before running commands; it does not overwrite variables already in the process environment, and a command-line flag wins over the same flag set in `skaffold.env`.

Use project-level settings (`skaffold.yaml`, `skaffold.env`) for team-wide behaviour and the global config for personal preferences. Because context names are matched as regular expressions, anchor them when needed so a short name does not match several clusters. List the current values with `skaffold config list` before changing them.

## Checked

2026-11-04. Read the Skaffold Global Configuration page, the "Load environment variables from a file" page and the CLI reference for `skaffold config`. Confirmed the option list, regex matching of contexts, `local-cluster` default contexts, subcommands and flags, the `skaffold.env` behaviour and flag precedence. Replaced the dead `/docs/environment/global-config/` source with the working page. Removed the blanket claim that all flags map to `SKAFFOLD_` variables except as documented on the env-file page.
Method: documentation only; no commands were run.
