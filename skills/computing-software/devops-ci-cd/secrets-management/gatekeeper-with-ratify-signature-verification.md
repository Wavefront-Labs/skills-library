---
id: computing-software.devops-ci-cd.secrets-management.gatekeeper-with-ratify-signature-verification
name: gatekeeper-with-ratify-signature-verification
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, ratify, gatekeeper, admission-control, notation]
level: advanced
status: docs-checked
description: "Verify image signatures at admission with OPA Gatekeeper external data and Ratify: quick start, provider timeout and cache, index caveat."
sources: ["https://ratify.dev/docs/what-is-ratify", "https://ratify.dev/docs/quick-start", "https://open-policy-agent.github.io/gatekeeper/website/docs/", "https://open-policy-agent.github.io/gatekeeper/website/docs/externaldata/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPA Gatekeeper with Ratify

Ratify is a verification engine, as a binary and on Kubernetes, that verifies artifact security metadata and admits for deployment only artifacts that comply with policies you create. On Kubernetes it plugs into Gatekeeper, a validating and mutating admission webhook that enforces CRD-based policies run by Open Policy Agent. Gatekeeper's external data feature (beta since v3.11) lets it query providers such as image registries; Ratify is listed among the community-maintained providers (others include cosign-gatekeeper-provider).

## Quick start (Ratify 1.4 docs)
- Prerequisites: Kubernetes 1.30 or higher, Gatekeeper v3.18 or higher, and helmfile >= 0.14 and < 1.0.0.
- Install Gatekeeper, Ratify and constraints together: `helmfile sync -f 'git::https://github.com/notaryproject/ratify.git@helmfile.yaml?ref=v1.4.3'`. For production, the docs point to manual install steps instead of helmfile.
- Test: a Notation-signed demo image is admitted; an unsigned one is denied by the `validation.gatekeeper.sh` webhook with a message like `[ratify-constraint] Subject failed verification: <image>`.
- If an image reference resolves to an OCI index or Docker manifest list, validation happens only at the index or manifest list level; Ratify does not support automatic platform selection.

## How Gatekeeper talks to the provider
- A `Provider` resource (`externaldata.gatekeeper.sh/v1beta1`) has `spec.url`, `spec.timeout` (seconds, on the Provider resource, not the implementation) and `caBundle` for TLS verification. For the mutating webhook the effective timeout is the smaller of the remaining webhook deadline and `spec.timeout`.
- Gatekeeper docs recommend providers respond within 1 to 2 seconds. Batch keys (for example, all container images in a pod) into one `external_data` call.
- Responses are cached (v3.13+) for 3 minutes by default; set `--external-data-provider-response-cache-ttl` (0 disables the cache).
- External data is enabled by default; `enableExternalData=false` in Helm (or `--enable-external-data=false`) turns it off, so do not disable it when using Ratify.
- Validation uses `ConstraintTemplate` and `Constraint` resources with `enforcementAction` (deny, warn, dryrun); mutators such as `AssignImage` change resources before validation. The sample tag-to-digest provider (not supported or maintained by the community) shows image tag-to-digest mutation.

## Verify
- [ ] An unsigned image is denied with a Ratify "failed verification" message and a signed image is admitted.
- [ ] Provider timeout and cache TTL are set deliberately and a registry slowdown does not block unrelated deploys.

## Checked
Method: docs-checked 2026-11-09 against the Ratify "What is Ratify" and Quick Start pages (v1.4), the Gatekeeper overview page and the Gatekeeper External Data page (v3.23.x).
Removed as unconfirmed: the manual Gatekeeper and Ratify Helm install flags (`validatingWebhookTimeoutSeconds`, `RATIFY_CERT_ROTATION`, `notationCerts`), the `RatifyVerification` constraint example, the Verifier and Policy CR descriptions (notation, cosign, sbom, vulnerabilityreport), the fail-open versus fail-closed advice, the "exempt system namespaces" advice, and the claim that Ratify caches results itself.
