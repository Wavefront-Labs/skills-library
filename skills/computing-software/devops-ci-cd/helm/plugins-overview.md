---
id: computing-software.devops-ci-cd.helm.plugins-overview
name: plugins-overview
category: computing-software
field: devops-ci-cd
product: helm
tags: [plugins, plugin-yaml, plugin-install, plugin-list, plugin-uninstall, helm-plugin, downloaders]
level: practitioner
status: docs-checked
description: "Helm plugins: plugin.yaml fields, install, list, update and uninstall, signature verification and plugin discovery."
sources:
  - "https://helm.sh/docs/topics/plugins/"
  - "https://helm.sh/docs/helm/helm_plugin_install/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A plugin is an add-on tool that appears as `helm NAME`. Plugins live in the directory pointed to by `$HELM_PLUGINS` and each has a `plugin.yaml`.

```yaml
name: "last"
version: "0.1.0"
usage: "get the last release name"
description: "get the last release name"
ignoreFlags: false
platformCommand:
  - command: "${HELM_PLUGIN_DIR}/bin/last"
```

Fields: `name` (required), `version` (SemVer 2), `usage`, `description`, `ignoreFlags` (true means flags are not passed to the plugin), `platformCommand`, `platformHooks`, `downloaders` (protocol handlers for custom `getter` schemes), and the deprecated `command` and `hooks` fields (the page says to use `platformCommand` and `platformHooks`; setting both of a pair is an error).

Commands:

- `helm plugin install PATH|URL [--version V]`: from a local folder or VCS URL (`--version` picks a version for VCS installs), or a tarball URL. `--verify` defaults to true: tarball installs need a `.prov` file alongside, while plugins from local directories count as local dev and need no signature. `--verify=false` skips the check (not recommended).
- `helm plugin list`
- `helm plugin uninstall NAME`

Helm sets environment variables for plugins including `HELM_PLUGIN_NAME`, `HELM_PLUGIN_DIR` (the plugin's directory), `HELM_BIN` (the path to the helm command) and `HELM_PLUGINS`.

Helm 4 supports both the Helm 3-style `plugin.yaml` format and the new Helm 4 plugin system. `HELM_NO_PLUGINS=1` disables plugins.

## Checked

2026-11-03. Confirmed against https://helm.sh/docs/topics/plugins/ (plugin.yaml fields, platformCommand, platformHooks, downloaders, ignoreFlags, SemVer 2 version, plugin env vars, Helm 3 format still supported in Helm 4) and https://helm.sh/docs/helm/helm_plugin_install/ (--verify default true, tarball .prov, local dev). Removed: the `helm plugin update` line, the name character rule, the extra environment variables, and the `list --short | head -1` example command (not on the pages).
Method: documentation only; no commands were run.

