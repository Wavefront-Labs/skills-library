---
id: computing-software.cybersecurity-defensive.falco.falcoctl-rules-install
name: falcoctl-rules-install
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falcoctl, artifact-install, rules-oci, index-add, falco-rules]
level: intro
status: docs-checked
description: "Download and update Falco rules distributed as OCI artifacts with falcoctl index add and falcoctl artifact install."
sources:
  - https://falco.org/docs/concepts/rules/default-custom/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The falcoctl tool downloads and updates rules files distributed as OCI artifacts. Add the official index, then install a rules artifact at a version:

```
falcoctl index add falcosecurity https://falcosecurity.github.io/falcoctl/index.yaml
falcoctl artifact install falco-rules:3.2.0
```

By default `install` downloads to `/etc/falco`, and the directory is configurable. Rules artifacts are published on GitHub Packages for the falcosecurity/rules repository; the Helm chart (3.0.0 or later) loads the latest one compatible with your Falco version and keeps it updated through falcoctl.

falcoctl is available in several forms:
- a standalone tool;
- included in Falco packages and container images;
- installed automatically as a systemd unit;
- deployed as an init container by the Helm chart.

Falco reads rules from the `rules_files` entries in `falco.yaml` (default `/etc/falco/falco_rules.yaml`, `/etc/falco/falco_rules.local.yaml`, `/etc/falco/rules.d`), or from `-r` on the command line, so check an installed file is covered by one of them. The rules also have auto-generated documentation at falcosecurity.github.io/rules.

Gotcha: the docs example pins a version (`falco-rules:3.2.0`); name the version you want rather than assuming the latest.

In the Helm chart, automatic updates are turned off with `falcoctl.artifact.install.enabled=false` and `falcoctl.artifact.follow.enabled=false`, which implies they are on by default.

## Checked

2026-11-08. Read the Default and Local Rules page in full. Corrected the claim that falcoctl serves the latest compatible rules (that is the Helm chart behaviour), added the default /etc/falco target, and removed the unsupported pin-for-reproducibility and must-list assertions.

Method: documentation only; no commands were run.
