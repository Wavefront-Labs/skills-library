---
id: computing-software.cybersecurity-defensive.trivy.discover-and-install-trivy-plugins
name: discover-and-install-trivy-plugins
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-plugin, plugin-index, plugin-search, plugin-install, go-getter, xdg-data-home]
level: practitioner
status: docs-checked
description: "Search the plugin index, install plugins by name, URL, archive or tagged version, and know the plugin cache location and supported download protocols."
sources:
  - https://trivy.dev/latest/docs/guide/plugin/user-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Discovery: refresh your local copy of the plugin index, then search it.

```bash
trivy plugin update
trivy plugin search
trivy plugin search referrer
```

Search lists plugins whose name or description contains the keyword, with NAME, DESCRIPTION, MAINTAINER and OUTPUT columns. Plugins are listed in trivy-plugin-index.

Install:

```bash
trivy plugin install referrer
trivy plugin install github.com/aquasecurity/trivy-plugin-kubectl
trivy plugin install https://github.com/aquasecurity/trivy-plugin-kubectl/archive/refs/heads/main.zip
trivy plugin install ./myplugin.tar.gz
trivy plugin install referrer@v0.3.0
```

Plugins not registered in the index can be installed by URL or file path. To pin a version the plugin's Git repository must be properly tagged; the leading `v` is required and the version must follow Semantic Versioning.

Location: Trivy follows the XDG specification. It uses `XDG_DATA_HOME` if set and `.trivy/plugins` exists inside it, otherwise `~/.trivy/plugins`.

Downloads use go-getter, so supported protocols are OCI registries, local files, Git, HTTP/HTTPS, Mercurial, Amazon S3 and Google Cloud Storage.

Manage installed plugins with `trivy plugin list`, `trivy plugin upgrade` (all) or `trivy plugin upgrade <PLUGIN1> <PLUGIN2>`, and `trivy plugin uninstall kubectl`.

## Checked

2026-11-03. Read and confirmed against the Plugins User Guide on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
