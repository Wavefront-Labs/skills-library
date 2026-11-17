---
id: computing-software.cybersecurity-defensive.trivy.vex-oci-attestation-discovery
name: vex-oci-attestation-discovery
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [vex-oci, cosign-attest, openvex, purl, oci-referrer, attestation]
level: advanced
status: docs-checked
description: "Discover VEX attestations attached to container images with --vex oci, build an OpenVEX document with OCI purl product IDs and attach it using cosign."
sources:
  - https://trivy.dev/latest/docs/guide/supply-chain/vex/oci/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy can discover VEX attestations for container images when you scan with `--vex oci`. It looks in these layouts: an OCI 1.1 referrer holding a Sigstore bundle (the default for `cosign attest` since Cosign v3); an OCI 1.1 referrer holding a DSSE envelope or bare in-toto statement under the `application/vnd.in-toto+json` artifact type; and the legacy `.att` tag, the Cosign v2 default. Referrers take precedence, with fallback to `.att`. Trivy uses the `in-toto.io/predicate-type` annotation to pick the VEX attestation without downloading the others, and skips referrers it cannot decode.

Step 1, create an OpenVEX document manually (Trivy has no built-in generator). The product ID must be an OCI purl, for example `pkg:oci/trivy?repository_url=ghcr.io/aquasecurity/trivy`, which applies to all tags; add `@sha256:<digest>` to target one digest. Tags in the product ID are not supported. List vulnerable packages as subcomponents such as `pkg:apk/alpine/busybox`, optionally with version and qualifiers like `arch`, and give vulnerability names, `status` (`not_affected` in the example), `justification` and `impact_statement`.

Step 2, attach with Cosign:

```
cosign attest --predicate oci.openvex.json --type openvex <IMAGE>
```

This attaches only to that tag; repeat for other tags and digests. Add `--no-upload` to preview without writing to the registry.

Step 3, scan: `trivy image --vex oci <IMAGE>`, optionally with `--show-suppressed`.

Trivy does not verify the attestation signature, so use `--vex oci` only with registries you trust.

## Checked

2026-11-03. Read and confirmed against the VEX OCI attestation page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
