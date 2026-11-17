---
id: computing-software.cybersecurity-defensive.application-security.cicd-pipeline-hardening
name: cicd-pipeline-hardening
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [cicd-hardening, ci-cd-security, owasp-top-10-cicd, pipeline-security, build-integrity, runner-security]
level: advanced
status: docs-checked
description: "Harden CI/CD pipelines using the OWASP CI/CD Security Cheat Sheet: SCM and pipeline configuration, IAM, dependency chain, integrity and logging."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD pipeline hardening

Pipeline steps often run with high-privileged identities, so a compromised pipeline has high damage potential. The
OWASP Top 10 CI/CD Security Risks, which the cheat sheet is organised around: CICD-SEC-1 Insufficient Flow Control
Mechanisms, 2 Inadequate Identity and Access Management, 3 Dependency Chain Abuse, 4 Poisoned Pipeline Execution,
5 Insufficient PBAC (Pipeline-Based Access Controls), 6 Insufficient Credential Hygiene, 7 Insecure System
Configuration, 8 Ungoverned Usage of Third-Party Services, 9 Improper Artifact Integrity Validation, 10 Insufficient
Logging and Visibility.

## Secure SCM configuration
- Avoid auto-merge rules; require pull request review that cannot be bypassed; use protected branches.
- Require signed commits and MFA where available.
- Do not rely on default permissions; manage them carefully. Limit external contributors and their permissions.
- Restrict forking of private or internal repositories and the ability to make a repository public.
- Legitify (open source) scans GitHub and GitLab for these misconfigurations.

## Pipeline and execution environment
- Build on appropriately isolated nodes; secure SCM-to-CI traffic with TLS 1.2 or greater; restrict access to CI/CD
  environments by IP if possible.
- If feasible, store the CI config file outside the repository it builds. If it lives alongside the code, review it
  before any merge request is approved.
- Version-control pipeline configuration; enforce MFA.
- Add SAST, DAST and IaC scanning to the pipeline; require manual approval and review before production deployment.
- Do not use the Docker `--privileged` flag in pipeline steps run in Docker images.
- Patch the OS, container images and web servers behind CI/CD, keep an asset inventory with versions, and harden to
  CIS Benchmarks or STIGs where appropriate.

## Secrets
- Never hardcode secrets in repositories or CI configuration; detect them with tools such as git-leaks or git-secrets
  and prevent commits where possible. Remove secrets from Docker images and compiled binaries.
- Do not print secrets to the console, log them or leave them in shell history files. A vault or secrets manager
  (HashiCorp Vault, AWS Secrets Manager, AKeyless, CyberArk) may be used.
- Reduce impact of theft with temporary credentials or OTPs and IP or other restrictions.

## Least privilege and identity lifecycle
- Apply least privilege to the secrets pipelines use, to what one pipeline or step can reach in the CI/CD platform
  (PBAC), and to the OS user running the pipeline (not root or comparable). Deny by default.
- Do not share credentials across pipelines of different sensitivity.
- Use a central IdP rather than local accounts, no shared accounts, no self-provisioning, and only
  organisation-controlled email domains. Keep an identity inventory (owner, provider, last used, last updated,
  granted and actually used permissions) to find over-privileged and forgotten identities.

## Third-party code
- Dependency chain abuse includes dependency confusion, typosquatting and maintainer account takeover. Make
  dependency references immutable: pin versions, verify hashes via lock files (for example `package-lock.json`,
  `Pipfile.lock`) and enforce the lock file.
- Prefer private repositories, configure the package manager to use a single private feed, use scoped npm packages or
  NuGet ID prefixes for private packages, and commit settings files such as `.npmrc`.
- Treat plug-ins and integrations like software acquisition: restrict who can install them, vet the vendor,
  popularity, maintenance and configuration changes required, keep them patched and remove unneeded ones.

## Integrity
Require signed commits, verify package hashes, use code signing (Sigstore or Signserver), and consider in-toto. Code
signing is not an absolute guarantee because the signing process itself can be exploited (see NIST Security
Considerations for Code Signing).

## Visibility and monitoring
Log in a parsable format (JSON or syslog) following your log management policy; never log plaintext passwords, tokens
or API keys. Send logs to a central system or preferably a SIEM and tune alerts regularly; expect false positives and
negatives.

## Verify
Merge cannot bypass review; a pipeline step has only the identity it needs; locked dependencies fail on hash
mismatch; logs contain no secrets.

## Checked
Method: docs-checked 2026-11-09 against the OWASP CI/CD Security Cheat Sheet (read in full). Removed unconfirmed
claims and sources not read: the OWASP Top 10 CI/CD project page, the NSA/CISA PDF and the SLSA levels page; the
per-risk bullets that came from those (ephemeral runners, Docker-socket mounts, SLSA level 2 advice, cosign and
specific audit-log products).
