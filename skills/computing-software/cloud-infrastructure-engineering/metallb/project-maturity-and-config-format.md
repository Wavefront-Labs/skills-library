---
id: computing-software.cloud-infrastructure-engineering.metallb.project-maturity-and-config-format
name: project-maturity-and-config-format
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, maturity, beta, config-format, compatibility, release-notes, cncf]
level: intro
status: docs-checked
description: "MetalLB project maturity: beta status, how backward-incompatible config changes are rolled out, Kubernetes compatibility policy and what to expect from support."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/maturity.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project maturity

- MetalLB is labelled beta. It is used in production and non-production clusters and bundled with major Kubernetes distributions for on-premise use; bug reports are infrequent.
- Test coverage is reasonable with many end-to-end tests, but edge cases may have bugs. File issues at github.com/metallb/metallb/issues.

Config format policy:
- The configuration format may change in backwards-incompatible ways as new protocols and features land.
- Changes roll out "make before break": one release understands both old and new formats so you can upgrade config separately from code; the next release removes the old format.
- Release notes during beta highlight required config changes and warn of removals planned for the following version. Read them before every upgrade (`computing-software.cloud-infrastructure-engineering.metallb.upgrading-metallb`).

Kubernetes compatibility: maintainers aim to keep compatibility with supported Kubernetes versions; unsupported versions are best effort.

Support expectations: the project is run by a small group of maintainers (no corporate sponsorship; copyright was owned by Google until March 2019, never an official Google project; it is a CNCF sandbox project). Set expectations accordingly; the docs say they may be incomplete in parts.

## Checked

2026-11-04. Read the MetalLB Project Maturity page in full and the home page beta note: beta label, adoption, test coverage, make-before-break config policy, release-note policy, Kubernetes compatibility, documentation caveat, Google copyright until March 2019, no sponsorship, CNCF sandbox all match. Nothing removed.

Method: documentation only; no commands were run.
