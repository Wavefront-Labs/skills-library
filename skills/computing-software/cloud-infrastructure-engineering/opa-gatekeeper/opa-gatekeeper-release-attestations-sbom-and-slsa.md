---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-release-attestations-sbom-and-slsa
name: opa-gatekeeper-release-attestations-sbom-and-slsa
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, sbom, slsa, provenance, attestations, buildx, supply-chain]
level: practitioner
status: docs-checked
description: "Retrieve Gatekeeper image build attestations, SBOMs and SLSA provenance (v3.12.0 and later) with docker buildx imagetools."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/security.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper release attestations sbom and slsa

Starting with v3.12.0, each Gatekeeper release image carries build attestations (SBOM and SLSA provenance) generated with Docker BuildKit 0.11 or later. List the image manifests and attestations per OS and architecture:

```shell
docker buildx imagetools inspect openpolicyagent/gatekeeper:v3.12.0-rc.0
```

Get the SBOM for all architectures, then narrow to one with jq:

```shell
docker buildx imagetools inspect openpolicyagent/gatekeeper:v3.12.0-rc.0 --format '{{ json .SBOM }}'
docker buildx imagetools inspect openpolicyagent/gatekeeper:v3.12.0-rc.0 --format '{{ json .SBOM }}' | jq -r '.["linux/amd64"]'
```

Gatekeeper generates two SBOMs: one for the build stage (builder image and Gatekeeper source) and one for the final stage (the built `manager` binary). SLSA provenance comes from the same tool with `--format '{{ json .Provenance }}'`.

The platforms listed include linux/amd64, linux/arm64 and linux/arm/v7, with extra manifests of unknown platform holding the attestations. Report vulnerabilities by email to the open-policy-agent security group address given in the security page, which follows the OPA security release process.

## Checked

2026-11-08. Confirmed against security.md, read in full: attestations from v3.12.0, BuildKit 0.11 or later, SBOM and SLSA provenance commands, two SBOMs, platform list, reporting address and release process pointer. Removed or corrected: nothing.

Method: documentation only; no commands were run.
