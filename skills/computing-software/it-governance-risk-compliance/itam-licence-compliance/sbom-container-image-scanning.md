---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-container-image-scanning
name: sbom-container-image-scanning
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-container-image-scanning, sbom-generation, container sbom, trivy, syft, oci attestation, cosign attach sbom, image layers, os packages, itam-licence-compliance]
level: practitioner
status: docs-checked
description: "Create SBOMs for container images and OS packages with Syft or Trivy and attach them to the image in the registry."
sources:
  - https://github.com/anchore/syft
  - https://github.com/aquasecurity/trivy/blob/main/docs/guide/supply-chain/sbom.md
  - https://github.com/sigstore/cosign
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOMs for container images and operating systems

Goal: inventory of what is inside each image.

Method:
- Syft: syft <image> -o cyclonedx-json=./image.cdx.json; Trivy: trivy image --format cyclonedx --output image.cdx.json <image> (--format cyclonedx disables security scanning unless you add --scanners vuln).
- Cover OS packages (dpkg, rpm, apk) and language packages.
- Attach the SBOM to the image digest as an OCI artifact/attestation (cosign attest --predicate sbom.json --type cyclonedx <image@digest>).
- Use minimal or distroless base images to reduce noise.
- Record the base image digest and the multi-stage build info.

Gotchas:
- Scan the final image, not only the Dockerfile.
- Tags are mutable; use digests.

Verify: image digest in the SBOM matches the deployed digest.

## Checked

2026-11-02. Checked against the Syft README (-o cyclonedx-json=FILE, ecosystems apk, dpkg, RPM), the Trivy SBOM guide (trivy image --format cyclonedx --output, scanning disabled by default) and the cosign attest reference (--predicate, --type cyclonedx). Removed: binary scanning claim and the 'confirm flags' hedge.

Method: documentation only; no commands were run.
