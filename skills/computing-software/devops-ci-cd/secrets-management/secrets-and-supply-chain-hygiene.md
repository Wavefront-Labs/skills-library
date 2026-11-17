---
id: computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene
name: secrets-and-supply-chain-hygiene
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secrets, credentials, vault, hashicorp-vault, openbao, aws-secrets-manager, azure-key-vault, gcp-secret-manager, external-secrets-operator, sops, sealed-secrets, oidc, workload-identity, secret-rotation, secret-scanning, gitleaks, trufflehog, supply-chain-security, sbom, syft, cyclonedx, spdx, artifact-signing, cosign, sigstore, slsa, provenance, dependency-pinning, dependabot, renovate]
level: practitioner
status: gated
description: "Keep a delivery pipeline's credentials and dependencies safe: OIDC over static keys, secret stores, rotation, leak scanning, dependency pinning, SBOMs and cosign signing."
sources: ["https://slsa.dev/", "https://docs.sigstore.dev/", "https://developer.hashicorp.com/vault/docs", "https://owasp.org/www-project-top-10-ci-cd-security-risks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets and supply-chain hygiene in CI/CD

**Goal:** no long-lived credential sits in CI, a leaked secret is detected and rotated
within hours, and every artifact you ship can be traced to its source and checked for
tampering.

## 1. Prefer no secret at all: OIDC / workload identity
CI platforms issue a short-lived signed identity token per job (GitHub Actions
`id-token: write`, GitLab `id_tokens:`, CircleCI OIDC). Configure the cloud (AWS IAM OIDC
provider, Azure federated credentials, GCP Workload Identity Federation) or Vault's JWT
auth to trust it and exchange it for credentials valid for minutes.
- **Scope the trust policy tightly:** match the `sub` claim to the repo *and* branch or
  environment (e.g. `repo:<org>/<repo>:environment:production`), never just the org.
  A wildcard `sub` lets any repo in the org — or any fork-triggered job — assume the role.
- Inside Kubernetes, use workload identity (IRSA/EKS Pod Identity, GKE/AKS workload
  identity) instead of mounting cloud keys.

## 2. When you must store secrets
- One source of truth: **Vault/OpenBao** or a cloud secret manager. CI fetches at runtime
  with a short TTL; apps read via **External Secrets Operator** or the CSI secrets driver.
- GitOps repos: never commit plaintext Kubernetes `Secret`s (base64 is not encryption).
  Use **SOPS** (age or KMS keys; `sops --encrypt --age <pubkey> --encrypted-regex '^(data|stringData)$' secret.yaml`; run on sops 3.13.3 with age: only `data` and `stringData` values became `ENC[AES256_GCM,...]`, `kind`/`metadata` stayed readable, and `sops --decrypt` restored them with `SOPS_AGE_KEY_FILE`),
  Sealed Secrets, or an External Secrets reference.
- CI-native secret stores (GitHub/GitLab variables) are fine for a few values: mark them
  masked/protected, scope to environments, and remember masking is best-effort —
  a transformed value (base64'd, split, JSON-escaped) prints in clear.
- Never pass secrets as command-line arguments (visible in process lists and often in
  logs); use env vars or files with `0600` permissions, and `set +x` around them in shell.

## 3. Rotation and leak response
- Every stored secret has an owner, a purpose and a rotation interval; dynamic secrets
  (Vault database engine issuing per-job DB users) remove rotation work entirely.
- **Scan for leaks** in pre-commit and CI: `gitleaks git --redact` (the `detect` command still works but is deprecated since v8.19, see the gitleaks skill) or
  `trufflehog git file://. --results=verified` (`--only-verified` still accepted); enable the platform's push protection.
- If a secret leaks: **revoke/rotate first**, then clean history. Removing the commit
  (`git filter-repo`) does not un-leak it — forks, caches and clones already have it.
  Check the provider's access logs for use during the exposure window.

## 4. Dependency and build integrity
- Pin dependencies with lockfiles and hashes; pin CI actions/images to digests or SHAs.
- Automate updates with **Renovate** or **Dependabot** so pinning doesn't mean rotting;
  group minor/patch updates and auto-merge them when tests pass.
- Use a private registry proxy (Artifactory, Nexus, or a scoped registry) and configure
  scopes so internal package names can't be satisfied from the public registry
  (dependency confusion): e.g. npm `@org:registry=` in `.npmrc`; for pip avoid
  `--extra-index-url` mixing public and private indexes.
- Run `npm ci --ignore-scripts` where install scripts aren't needed.

## 5. SBOMs, signing and provenance
- Generate an SBOM per artifact: `syft <image> -o cyclonedx-json > sbom.cdx.json`
  (or SPDX); scan it with `grype sbom:sbom.cdx.json` or Trivy.
- **Sign images keylessly with cosign** in CI (uses the job's OIDC identity, logs to the
  Rekor transparency log): `cosign sign --yes <registry>/app@sha256:<digest>`.
  Sign the digest, never a tag.
- Attach the SBOM and build provenance as attestations
  (`cosign attest --predicate sbom.cdx.json --type cyclonedx ...`; SLSA provenance from
  your platform's generator or `actions/attest-build-provenance`).
- **Verify at deploy time**, or signing is theatre:
  `cosign verify <image>@<digest> --certificate-identity-regexp '^https://github.com/<org>/<repo>/' --certificate-oidc-issuer https://token.actions.githubusercontent.com`,
  enforced in-cluster by Kyverno or Sigstore policy-controller.
- Aim for SLSA Build L2+: builds run on a hosted platform, provenance is generated by
  the platform rather than the build script.

## Unconfirmed
Run here: SOPS+age, gitleaks, trufflehog, syft, grype, cosign (3.1.3) key-based sign/verify/attest and keyless verify of a public image. Not run (gated: unconfirmed): Renovate/Dependabot, External Secrets Operator, the CSI driver, IRSA/workload identity, Kyverno/policy-controller enforcement, and CI OIDC signing. The issuer URL above is GitHub's; other CIs differ.
Use `--certificate-identity*` flags on verify (required in keyless mode on cosign 3.1.3) and sign digests, as in the cosign skills.

## Verify
- [ ] No cloud access keys are stored in CI; deploy roles trust only specific repo + environment subjects.
- [ ] `gitleaks`/`trufflehog` runs on every PR and the full history scan is clean.
- [ ] Every secret has an owner and rotation date; a rotation drill has been done.
- [ ] Each released image has an SBOM and a signature tied to the CI identity.
- [ ] The cluster rejects an unsigned image (test with a hand-built one).
