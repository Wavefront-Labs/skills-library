---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-release-channels
name: k3s-release-channels
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, release-channel, stable-latest, install-k3s-channel]
level: intro
status: docs-checked
description: "Understand the stable, latest and per-minor-version K3s release channels used by the installer and automated upgrades."
sources:
  - https://docs.k3s.io/upgrades/manual
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrades through the install script or automated upgrades can follow release channels:

- stable: the default; recommended for production. Releases have had a period of community testing.
- latest: always the highest non-prerelease version by semver order. These have not been through the community testing period.
- a minor-version channel such as v1.33: one channel exists per Kubernetes minor version, including end-of-life ones. It picks the latest release of that minor, not necessarily a stable one.

Select with the installer variable:

```
curl -sfL https://get.k3s.io | INSTALL_K3S_CHANNEL=latest sh -
```

INSTALL_K3S_CHANNEL defaults to stable; options include stable, latest and testing. INSTALL_K3S_CHANNEL_URL defaults to https://update.k3s.io/v1-release/channels. The full list is available from the K3s channel service API, and the channelserver project explains how channels work.

Warning: the Kubernetes version skew policy applies when moving to a new version. Make sure the plan does not skip intermediate minor versions; the system-upgrade-controller does not protect against unsupported Kubernetes version changes.

## Checked

2026-11-03: read docs.k3s.io upgrades/manual (and reference/env-variables). Confirmed: the stable, latest and minor-version channels, INSTALL_K3S_CHANNEL and CHANNEL_URL defaults and the skew policy warning. Removed: the FAQ sentence about servers newer than agents, which was not in a fetched page.

Method: documentation only; no commands were run.
