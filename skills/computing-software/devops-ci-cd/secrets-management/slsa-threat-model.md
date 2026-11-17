---
id: computing-software.devops-ci-cd.secrets-management.slsa-threat-model
name: slsa-threat-model
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, slsa-threats, slsa-levels, supply-chain-security]
level: advanced
status: verified
description: "Use the SLSA threat model (source, build, dependency and distribution threats A-I) to map supply-chain risks to controls and decide which SLSA requirements matter first."
sources: ["https://slsa.dev/spec/v1.0/threats", "https://slsa.dev/spec/v1.0/threats-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLSA threat model

The SLSA v1.1 threats overview (slsa.dev/spec/v1.1/threats-overview, fetched) labels threats A-I along the flow source -> build -> package -> consumer, with real incidents as examples (SpySheriff, SushiSwap, PHP, The Great Suspender, SolarWinds, CodeCov, package mirrors, Browserify typosquatting, default credentials).

| Id | Threat | Example | Main controls |
|---|---|---|---|
| A | Producer: software producer is malicious (SpySheriff); SLSA does not directly address it | malicious maintainer | public source code, monitoring |
| B | Authoring & reviewing: unauthorised change (SushiSwap contractor commit) | compromised dev account pushes | two-person review, branch protection, MFA, signed commits |
| C | Source code management compromised (PHP git server) | SCM server hacked | hardened SCM, audit logs |
| D | External build parameters: build from modified source (The Great Suspender) | build runs on a fork's code | provenance records exact source revision; verify expected repo/ref |
| E | Build process compromised (SolarWinds) | tampered runner, poisoned cache (SolarWinds-style) | hosted, isolated, ephemeral builders (Build L3), unforgeable provenance |
| F | Artifact publication: modified package uploaded (CodeCov GCS bucket) | push artifact bypassing CI | provenance + verification at consumption |
| G | Distribution channel compromised (malicious package mirrors) | registry or mirror takeover | signing, verification, registry MFA |
| H | Package selection: consumer picks a bad package (Browserify typosquat); SLSA does not address it directly | typosquat, dependency confusion | dependency review, pinning, verified provenance of deps |
| I | Usage (default credentials); SLSA does not address it | misconfiguration | hardening outside SLSA |
| (dep) | Compromised dependency | malicious upstream release | SLSA applied recursively, cooldowns, review |

## Using it
1. Map your pipeline onto the diagram and list where each threat applies.
2. The Build track (L1-L3) addresses D, E, F with provenance; verification at deploy (admission
   policy, `slsa-verifier`, `gh attestation verify`) is what turns provenance into protection.
3. Source threats (A-C) need source controls; the SLSA Source track formalises them but exists only in the Working Draft (v1.1 is the latest release and has the Build track only).
4. Dependency threats need SBOM, pinning and policy on what you consume.

## Common gap
Generating provenance but never verifying it gives no protection against F/G. Verification
must be enforced somewhere in the consumer path.

## Verify
- [ ] A threat-to-control table exists for the main product with an owner per gap.
