---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcloud-alpha-beta-release-tracks
name: gcloud-alpha-beta-release-tracks
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud, gcloud-release-tracks, gcloud-beta-alpha, gcloud-components, preview-features]
level: practitioner
status: docs-checked
description: "Use gcloud alpha, beta and preview release levels safely: what each means, installing the components, finding which level has a command, and keeping scripts on GA where possible."
sources: ["https://docs.cloud.google.com/sdk/gcloud", "https://docs.cloud.google.com/sdk/docs/components"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gcloud alpha and beta release tracks

By default the gcloud CLI installs only General Availability (GA) commands. Earlier release levels
live in separate components named `alpha`, `beta` and `preview`.

| Level | Label | Meaning (from the gcloud overview) |
|---|---|---|
| Preview | `preview` | gathers customer feedback; not necessarily feature-complete; no SLAs or technical support commitments; test environments only unless stated otherwise |
| Beta | `beta` | functionally complete but could have outstanding issues; breaking changes can be made without notice |
| Alpha | `alpha` | early release; may change without notice |

## Setup
```bash
gcloud components install alpha beta
gcloud components list
```
If you run an alpha, beta or preview command interactively without the component, gcloud asks
whether to install it. Components are managed with `gcloud components install|update|remove`.
To downgrade a CLI installed through a package manager, use apt-get or yum with a specified
version (see the components page).

## Finding the level for a command
Compare `gcloud <group> <command> --help` with `gcloud beta <group> <command> --help` (and
`alpha`), or check the command's page in the gcloud reference, which lists each release level
under `gcloud`, `gcloud beta` and `gcloud alpha`.

## Scripting rules
- Prefer GA commands. If a beta or alpha command is needed, comment why and re-check it when the CLI is upgraded, because breaking changes can come without notice.
- Pin the CLI version in CI images so a change in a pre-GA command cannot break pipelines unexpectedly.
- Keep preview-level features out of production paths (no SLA or support commitment).

## Checked
2026-10-31. Confirmed against the gcloud CLI overview (release levels table, GA-only default, separate alpha/beta/preview components, install prompt) and the components page (`gcloud components install`, update and remove, package-manager note). Removed: apt package names, container image tag, Terraform provider remark, `INVALID_ARGUMENT` allowlist claim, alias-removal timing, specific flag examples and verbosity advice, because none appeared in the fetched pages.
Method: documentation only; no commands were run.

## Verify
- [ ] `gcloud components list` shows the alpha and beta components installed in the CI image.
- [ ] Every non-GA command in a script has a comment explaining why GA is not enough.
