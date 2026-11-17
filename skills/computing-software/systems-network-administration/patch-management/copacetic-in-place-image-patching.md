---
id: computing-software.systems-network-administration.patch-management.copacetic-in-place-image-patching
name: copacetic-in-place-image-patching
category: computing-software
field: systems-network-administration
product: patch-management
tags: [copacetic, image-patching, trivy, base-image-update, container-images, immutable-infrastructure]
level: practitioner
status: docs-checked
description: "Patch OS-package vulnerabilities in container images you can't rebuild quickly using Copacetic (copa) with a Trivy report, plus limits, tagging and verification."
sources:
  - https://project-copacetic.github.io/copacetic/website/
  - https://github.com/project-copacetic/copacetic/blob/main/website/docs/faq.md
  - https://trivy.dev/latest/docs/references/configuration/cli/trivy_image/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-place image patching with Copacetic

Rebuilding from an updated base image is the right fix. Copacetic (`copa`) covers
the gap: third-party or vendor images you can't rebuild, or emergency fixes before the
upstream image updates. It adds a layer with updated OS packages using BuildKit.

## Requirements
- `copa` CLI, Docker/BuildKit (or a buildkitd address).
- A vulnerability report (Trivy JSON) for the image, or let copa update all packages.
- Copa patches OS-level packages managed by system package managers (apt, yum/dnf, apk). Debian-based
  and Azure Linux images use a tooling image; support for several RPM-based distributions is listed in
  the Copacetic FAQ with its maturity; Copa does not patch distroless Alpine images.

## Patch
```sh
IMG=registry.example/vendor/app:3.2.1
trivy image --pkg-types os --ignore-unfixed -f json -o app.json $IMG
copa patch -i $IMG -r app.json        # creates $IMG-patched in the local image store
# or update every OS package (no report)
copa patch -i $IMG
trivy image --pkg-types os --ignore-unfixed registry.example/vendor/app:3.2.1-patched
docker push registry.example/vendor/app:3.2.1-patched   # the default tag adds -patched
```

## Pipeline pattern
Nightly: scan deployed third-party images → if fixable OS vulns above threshold → copa
patch → rescan → push `-patched` tag → sign (cosign) → open PR to bump the deployment
manifest (or Renovate picks it up).

## Limits
- Only **OS packages**. Vulnerable application dependencies (JARs, npm, pip) are untouched;
  those need a rebuild or vendor update.
- Can't fix what the distro hasn't fixed (`--ignore-unfixed`).
- The image's original signature/provenance no longer applies; sign your patched image and
  record provenance.
- Vendor support may not cover modified images.

## Verify
Rescan shows the targeted CVEs gone; container starts and passes health checks;
deployment references the patched digest.

## Checked
Date: 2026-10-27. Documentation checked: Copacetic README, quick start and FAQ (patch command forms, `-patched` tag, `-r` report, OS-level scope, tooling images, distroless Alpine limit), Trivy `--pkg-types os` and `--ignore-unfixed` (current Trivy CLI reference; the Copacetic quick start still shows the older `--vuln-type`). Removed the unconfirmed `-t` tag flag and the CNCF sandbox statement.

Method: documentation only; no commands were run.
