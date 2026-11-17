---
id: computing-software.devops-ci-cd.packer.host-plugin-mirror
name: host-plugin-mirror
category: computing-software
field: devops-ci-cd
product: packer
tags: [plugin-mirror, https, sha256sums, index-json, plugins-install]
level: advanced
status: docs-checked
description: "Serve plugins from your own HTTPS host using the index.json and SHA256SUMS layout Packer expects."
sources:
  - "https://developer.hashicorp.com/packer/docs/plugins/install-plugins/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Plugins can come from infrastructure you run, such as an internal mirror or artifact repository. Put the host and path in the plugin's `source`, for example `plugins.example.com/mirror/hashicorp/happycloud`.

The host must serve this layout over HTTPS under the source path:

```text
packer-plugin-happycloud/index.json
packer-plugin-happycloud/<version>/packer-plugin-happycloud_<version>_SHA256SUMS
packer-plugin-happycloud/<version>/<zip files listed in SHA256SUMS>
```

It is the same structure releases.hashicorp.com serves. Packer reads `index.json` to discover versions, selects the one matching the template's constraints, downloads the zip for the host platform, and verifies it against that version's SHA256SUMS file.

Version directory names have no `v` prefix.

For plugins on GitHub, the requirements are different: a repository named `packer-plugin-<name>`, semantic version tags `v<major>.<minor>.<patch>`, and a release with a shasums file.

## Checked
2026-11-03. Confirmed against the Install plugins page (Host your own plugin source): HTTPS layout, `index.json`, SHA256SUMS, discovery and verification flow, no `v` prefix, and the GitHub repository, tag and shasums requirements. Removed unsourced closing advice.
Method: documentation only; no commands were run.
