---
id: computing-software.cybersecurity-defensive.system-hardening.registry-hardening
name: registry-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [registry-hardening, harbor, container-registry, ecr, acr, image-signing, tag-immutability]
level: practitioner
status: draft
description: "Harden a private container registry (Harbor, ECR, ACR, Artifact Registry): authn and RBAC, TLS, tag immutability, scanning and signing gates, robot accounts, and audit."
sources: ["https://goharbor.io/docs/main/administration/", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/security.html", "https://learn.microsoft.com/en-us/azure/container-registry/container-registry-best-practices", "https://distribution.github.io/distribution/about/deploying/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Private registry hardening

The registry is the source of truth for what runs in production. Anyone who can push to it can deploy code.

## Access
- No anonymous pull for private projects (Harbor project "Public" off; ECR repository policies without `*`
  principals; ACR anonymous pull disabled; Artifact Registry IAM without `allUsers`).
- RBAC: CI deploy identities push to specific repositories only; clusters get pull-only identities (IRSA/
  workload identity, ACR `AcrPull` on kubelet identity, ECR pull via node role); humans rarely push.
- Robot/service accounts (Harbor robot accounts, ACR tokens/scope maps) with expiry; OIDC from CI instead of
  long-lived passwords where supported.
- SSO for the UI (Harbor OIDC), admin accounts with MFA.

## Network and TLS
TLS with valid certificates (never `insecure-registries` in Docker/containerd), private endpoints (ECR VPC
endpoints, ACR Private Link) and firewall rules; self-hosted distribution/Harbor behind a hardened reverse
proxy.

## Integrity
- **Tag immutability** (Harbor immutable tag rules, ECR `imageTagMutability=IMMUTABLE`, ACR locking via
  `--write-enabled false`): stops `:1.4.2` being silently replaced.
- Sign images (cosign/Notation) and enforce verification at admission; Harbor can store signatures and
  prevent pulling unsigned images ("Cosign" content trust policy per project).
- Deploy by digest.

## Vulnerability gates
Scan on push (Harbor with Trivy, ECR enhanced scanning via Inspector, Defender for Containers for ACR); Harbor
"Prevent vulnerable images from running" with a severity threshold; rescan regularly since new CVEs appear for
old images.

## Lifecycle
Retention/garbage collection policies remove old untagged images (less to scan, less risk of redeploying old
vulnerable builds); quarantine and proxy-cache projects for upstream images (Docker Hub rate limits and
supply-chain control).

## Audit
Registry audit logs (Harbor audit log, CloudTrail for ECR, ACR diagnostic logs) to SIEM; alert on pushes by
unexpected principals, policy changes, deletion bursts, and pulls from unknown networks.

## Verify
Anonymous `docker pull` fails; pushing an existing tag is rejected; an unsigned image is blocked at admission;
audit log shows push events with CI identity only.
