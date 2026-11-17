---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-version-compatibility-and-release-types
name: karpenter-version-compatibility-and-release-types
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [compatibility, kubernetes-version, semver, release, snapshot, upgrade]
level: intro
status: docs-checked
description: "Karpenter-to-Kubernetes compatibility matrix for v1.13, breaking change policy, and stable, release candidate and snapshot release types."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/upgrading/compatibility.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter version compatibility and release types

Minimum Karpenter version per Kubernetes version:

| Kubernetes | 1.30 | 1.31 | 1.32 | 1.33 | 1.34 | 1.35 | 1.36 |
|---|---|---|---|---|---|---|---|
| Karpenter | >= 0.37 | >= 1.0.5 | >= 1.2 | >= 1.5 | >= 1.6 | >= 1.9 | 1.13.x |

Breaking-change policy:
- Stable releases follow SemVer 2.0.0. In major version 0 anything may change, but breaking changes only land in minor releases (x.y.z, y incremented).
- Each breaking change gets a permanent `upgrading to x.y.z+` section in the release upgrade notes and a sentence at the top of the release notes.
- Check for breaking changes on every minor upgrade.
- Security patches: not backported in major 0; from major 1 an EOL policy patches a subset of older versions.

Release types:
- Stable: the only recommended type for production. Tagged `0.35.0`; releases before 0.35.0 carry a `v` prefix.
- Release candidates: `x.y.z-rc.0`, `-rc.1`, for early adopters, then graduate to `x.y.z`.
- Snapshot: built for every merged commit, in a private ECR repository, chart tagged `<major>-<git hash>` (for example `0-fc17bfc...`). Requires `aws ecr get-login-password | docker login` first. Ephemeral, deleted after 90 days, for testing only.

Images are published at gallery.ecr.aws/karpenter.

## Checked

2026-11-08. Confirmed against the Compatibility page (v1.13): matrix, breaking-change policy, release types and snapshot details. Nothing material removed.

Method: documentation only; no commands were run.
