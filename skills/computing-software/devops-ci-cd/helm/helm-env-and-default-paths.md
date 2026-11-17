---
id: computing-software.devops-ci-cd.helm.helm-env-and-default-paths
name: helm-env-and-default-paths
category: computing-software
field: devops-ci-cd
product: helm
tags: [helm-env, paths, cache-home, config-home, data-home, xdg, windows, macos, linux]
level: intro
status: docs-checked
description: "Where Helm keeps cache, config and data by default on Linux, macOS and Windows, and how helm env shows them."
sources:
  - "https://helm.sh/docs/helm/helm/"
  - "https://helm.sh/docs/helm/helm_env/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Helm uses three base directories, each overridable by an environment variable:

- Cache (`HELM_CACHE_HOME`): alternative location for cached files.
- Config (`HELM_CONFIG_HOME`): alternative location for Helm configuration, including `repositories.yaml` and `registry/config.json`.
- Data (`HELM_DATA_HOME`): alternative location for Helm data.

Order of precedence: a `HELM_*_HOME` variable if set, then the XDG variables on systems that support the XDG base directory specification, then the OS default.

Defaults by operating system:

- Linux: `$XDG_CACHE_HOME/helm` or `$HOME/.cache/helm`; `$XDG_CONFIG_HOME/helm` or `$HOME/.config/helm`; `$XDG_DATA_HOME/helm` or `$HOME/.local/share/helm`.
- macOS: `$HOME/Library/Caches/helm`, `$HOME/Library/Preferences/helm`, `$HOME/Library/helm`.
- Windows: `%TEMP%\helm` for cache, `%APPDATA%\helm` for config and data.

Finer-grained variables point at single locations: `HELM_REPOSITORY_CACHE`, `HELM_REPOSITORY_CONFIG`, `HELM_REGISTRY_CONFIG`, `HELM_PLUGINS`.

`helm env` is the Helm client environment information command. The default registry config path is `~/.config/helm/registry/config.json`.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/helm/helm/ (environment variable table, precedence order, per-OS default paths, default registry and repository paths). Removed: the `helm env` output format and single-variable form, the cache-wiping and CI isolation advice, and the registry logout advice (not on the page).
Method: documentation only; no commands were run.

