---
id: computing-software.devops-ci-cd.secrets-management.slsa-build-levels
name: slsa-build-levels
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, slsa, slsa-levels, slsa-build-l1, slsa-build-l2, slsa-build-l3, slsa-provenance, build-platform-hardening, hosted-build-platform, isolated-builds, ephemeral-builders, unforgeable-provenance, trusted-builder, slsa-github-generator, gitlab-slsa, tekton-chains, google-cloud-build-slsa, supply-chain-security, build-integrity, source-track, dependency-track, slsa-verifier, slsa-assessment, build-l3-checklist]
level: advanced
status: gated
description: "Understand and reach SLSA v1.0 Build levels: what L1/L2/L3 require (provenance exists, hosted and signed, hardened and isolated), which platforms give L3, how to assess and close gaps."
sources: ["https://slsa.dev/spec/v1.0/levels", "https://slsa.dev/spec/v1.0/requirements", "https://slsa.dev/spec/v1.0/threats", "https://github.com/slsa-framework/slsa-github-generator", "https://docs.gitlab.com/ee/ci/runners/configure_runners.html#artifact-attestation", "https://tekton.dev/docs/chains/slsa-provenance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLSA build levels

**Goal:** know which SLSA Build level your artifacts actually meet, what it would take to
reach L3, and which claims you can honestly make to customers and auditors.

## 1. What SLSA v1.0 is (and isn't)
SLSA ("salsa") is a ladder of *build integrity* guarantees. v1.0 has one track, **Build**,
with levels 0–3. v1.1 is the latest published version (slsa.dev/spec/v1.2 returns 404); the Source track exists only in the Working Draft, not in v1.0 or v1.1. It answers: *can I trust that this
artifact was built from this source by this build definition on this platform, without
tampering?* It does **not** cover vulnerabilities in your code or dependencies (that's
scanning/SBOM), nor the trustworthiness of the source itself (Source track).

| level | requirement (short) | protects against |
|---|---|---|
| **L0** | nothing | — |
| **L1** | consistent build process; **provenance exists** (who/what/how); spec: "trivial to bypass or forge" | mistakes, documentation drift |
| **L2** | build runs on a **hosted platform** (not a developer laptop); provenance **signed by the platform**, verifiable by consumers | tampering *after* the build, forged provenance by individuals |
| **L3** | **hardened platform**: builds run in isolated, ephemeral environments; the build's user-defined steps **cannot access the signing key** nor influence the provenance; no persistent cache poisoning between builds | tampering *during* the build by the build definition itself, compromised dependencies writing provenance, cross-build contamination |

Key L3 phrase: provenance is **unforgeable** by the build's own steps — the attestation
is produced by the platform/trusted builder from its own observation, not by a script you
control in the job.

## 2. Platforms and what they give
- **GitHub Actions**: hosted runners + `slsa-github-generator` reusable workflows
  (`generator_generic_slsa3.yml`, `generator_container_slsa3.yml`, language builders for
  Go/Node/Maven) → **L3**: the provenance is created in a separate, trusted reusable
  workflow with its own OIDC identity, signed via Sigstore keyless. GitHub's native
  `actions/attest-build-provenance` yields L2 (GitHub docs: artifact attestations by themselves provide SLSA v1.0 Build L2; L3 needs a vetted reusable workflow) (the attestation is created in your own
  job, which can influence it) — unless used from a reusable workflow with the subject
  computed outside the user's job, which GitHub documents as L3-eligible on hosted runners.
  Self-hosted persistent runners drop to L2 at best (no isolation guarantee) — use
  ephemeral ARC runners.
(Platform rows below other than GitHub were not checked against vendor docs: gated: unconfirmed.)
- **GitLab**: `RUNNER_GENERATE_ARTIFACTS_METADATA: "true"` produces SLSA provenance
  statements per job artifact (L1/L2 depending on runner isolation and signing via
  GitLab's keys); GitLab documents the resulting level per runner type — shared SaaS
  runners with ephemeral VMs are the L3 candidates.
- **Google Cloud Build**: L3 provenance for container images by default
  (`gcloud artifacts docker images describe --show-provenance`).
- **Tekton Chains**: signs TaskRun results and emits SLSA provenance; L3 depends on
  isolating steps from the Chains signing key (separate namespace/KMS).
- **Jenkins/self-hosted anything**: typically L1–L2; L3 needs ephemeral agents, no
  shared workspaces/caches with write access across builds, and signing performed by a
  component the job cannot reach (e.g. a post-build signer with KMS keys the agent lacks
  IAM for).

## 3. Assessing your pipeline (checklist)
L1:
- [ ] Build steps are in version-controlled config (Jenkinsfile, workflow YAML), not clicked.
- [ ] Each released artifact has a provenance statement naming source repo + commit, builder, build config, dependencies/inputs where known.
L2:
- [ ] Builds run on a hosted/managed platform; developers cannot push artifacts from laptops to the release registry (registry write restricted to the CI identity).
- [ ] Provenance is signed by the platform (Sigstore keyless with the workflow identity, or a platform-held key) and consumers can verify it.
L3:
- [ ] Each build gets a fresh, isolated environment (ephemeral VM/container; no reuse of workspace, no shared writable caches unless content-addressed and verified).
- [ ] The build's steps cannot read the signing key or write the provenance (separate trusted builder/reusable workflow/signer).
- [ ] Build inputs are declared and pinned (actions by SHA, base images by digest, lockfiles) — not strictly required by L3 but expected by "hardened".
- [ ] Secrets available to the build are limited to what the build needs (no registry-admin creds).
Document the assessment per pipeline; the honest answer for most orgs today is "L2 on
GitHub-hosted, L1 on Jenkins" — fine, as long as it's stated.

## 4. Closing typical gaps
- Laptop releases → make the registry/package index accept pushes only from the CI OIDC
  identity (ECR/GHCR/PyPI trusted publishing); humans get read-only.
- Shared persistent runners → ephemeral runners (ARC runner scale sets, GitLab autoscaler
  with one-job VMs, Jenkins pod-per-build).
- Provenance generated by `run:` steps → move to `slsa-github-generator` or the native
  attestation action in a reusable workflow; the subject digest is computed by the
  trusted workflow from the uploaded artifact.
- Caches: read-only restores from content-addressed keys; never cache binaries that are
  executed in the next build unless verified.
- Secrets: OIDC instead of static keys; the job never sees the signing key (Sigstore
  keyless with the job's identity is fine — the *identity* is the key, bound to the
  workflow ref).

## 5. Consumption: verification is where value appears
Provenance nobody checks is paperwork. Consumers (deploy pipelines, admission controllers)
verify: `slsa-verifier verify-image ghcr.io/org/app@sha256:… --source-uri github.com/org/app --source-tag v1.4.2`,
`gh attestation verify oci://… --owner org --signer-workflow org/release/.github/workflows/build.yml`,
or Kyverno/policy-controller rules requiring the expected builder id and source repo.
Pin **which builder and which source** you trust — that's the actual policy.

## 6. Talking about it honestly
Say "artifacts carry SLSA Build L3 provenance generated by `<builder>`; verified at
deploy by `<policy>`", not "we are SLSA compliant". Levels are per artifact/pipeline, not
per company. Keep the assessment and the verification logs for audits (SOC 2 CC8, ISO
27001 A.8.25–8.32 map well to this).

## Verify
- [ ] For a sample release: `slsa-verifier`/`gh attestation verify` passes and shows the expected builder + source.
- [ ] A build job cannot `curl` the signing material or modify the attestation (tested by attempting it from a step).
- [ ] Registry/package index rejects a push from a developer credential.
- [ ] Written per-pipeline level assessment exists and matches reality.
