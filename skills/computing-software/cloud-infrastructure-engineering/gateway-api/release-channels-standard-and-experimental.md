---
id: computing-software.cloud-infrastructure-engineering.gateway-api.release-channels-standard-and-experimental
name: release-channels-standard-and-experimental
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [versioning, release-channels, standard, experimental, bundle-version, semver]
level: practitioner
status: docs-checked
description: "Choose between Standard and Experimental release channels, read the bundle-version and channel CRD annotations, and know the release cadence."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/versioning.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/crd-management/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gateway API ships two channels of CRDs. All new features and resources start in Experimental; they may graduate to Standard or be dropped.

- **Standard**: resources that graduated to Beta or GA API versions (Beta versions are being phased out) plus fields that graduated from Experimental. Recommended by default for a stable experience.
- **Experimental**: everything in Standard plus resources with Alpha API versions and new fields before they graduate. No backwards-compatibility guarantees; breaking changes can ship in any minor release, and some upgrades may need the Experimental CRDs uninstalled and reinstalled (release notes say so). A proposal with no progress in 6 months is auto-dropped.

Identify what is installed from CRD annotations:

- `gateway.networking.k8s.io/bundle-version`: the release (Git tag, such as `v0.4.0`) the CRD came from.
- `gateway.networking.k8s.io/channel`: `standard` or `experimental`.

Release cadence:

- Standard releases target a 4-month cadence with a fixed date; content that is not ready waits for the next release.
- Monthly Experimental releases are tagged `monthly-<year>-<month>`, contain only `experimental-install.yaml`, are snapshots of main, get no bugfix backports and do not use SemVer.
- SemVer releases include both `experimental-install.yaml` and `standard-install.yaml` and use release branches for backports.
- Each release supports at least the 5 most recent Kubernetes minor versions.

Graduation from Experimental to Standard requires full conformance test coverage, multiple conformant implementations, widespread usage, at least 6 months of soak as an alpha API, no significant change for at least 1 minor release and 3 months, and approval from subproject owners and KEP reviewers.

Validating Admission Policies protect channel boundaries: the Upgrade VAP prevents applying Experimental CRDs over Standard CRDs (remove it if you must), and the Guardrails VAP prevents setting experimental fields unless an annotation is present.

CRD management: a cluster admin or cluster provider should install CRDs. Bundlers must never overwrite CRDs with unrecognised or newer versions or a different channel, or remove them. Avoid moving backwards (rollback can lose configuration), read the release notes first, and upgrade one minor version at a time for the safest path.

## Checked

2026-11-08. Read in full (GitHub markdown): the Versioning page and CRD Management guide; the API overview was read for channel badges. Confirmed: channel definitions, annotations, cadence, monthly and SemVer release contents, supported Kubernetes versions, graduation criteria, the two VAPs, CRD ownership and upgrade guidance. Removed: the example resources Backend and BackendTrafficPolicy, the claim that VAPs block older-over-newer CRD installs, and "never mix channels from different releases" (not stated in the sources).

Method: documentation only; no commands were run.
