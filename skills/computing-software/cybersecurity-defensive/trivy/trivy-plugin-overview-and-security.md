---
id: computing-software.cybersecurity-defensive.trivy.trivy-plugin-overview-and-security
name: trivy-plugin-overview-and-security
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [trivy-plugins, plugin-security, sandbox, credentials, plugin-quickstart, extensibility]
level: intro
status: docs-checked
description: "What Trivy plugins are, the quickstart commands, and the security model: plugins run unsandboxed with your permissions and environment variables."
sources:
  - https://trivy.dev/latest/docs/guide/plugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy plugins let others extend the CLI without changing the Trivy code base. The system was inspired by the plugin systems of kubectl, Helm and Conftest. Plugins are add-on tools that can be added and removed without affecting core Trivy, can be written in any programming language, and show up in Trivy help and subcommands.

Quickstart:

1. `trivy plugin update` downloads the plugin list.
2. `trivy plugin search` discovers plugins on the plugin index.
3. `trivy plugin install referrer` installs one.
4. `trivy referrer --help` uses it.
5. `trivy plugin upgrade` keeps plugins up to date.
6. `trivy plugin uninstall referrer` removes it.

Security considerations: plugins are external programs executed with the privileges of the user running Trivy. They inherit the Trivy process environment variables, which may include credentials, and can access files and network services permitted by the execution environment. Trivy does not sandbox plugins or isolate them from these resources.

Publicly available plugins are not audited for security, so install and run only plugins from sources you trust. In CI, provide only the credentials and permissions the plugin requires, and use an isolated execution environment when you need additional restrictions. The same permissions apply to output-mode plugins that receive scan results.

## Checked

2026-11-03. Read and confirmed against the Plugins overview page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
