---
id: computing-software.cloud-infrastructure-engineering.google-cloud.binary-authorization-policy-configuration
name: binary-authorization-policy-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, binauthz-policy-config, binauthz-policy-yaml, attestors, dry-run]
level: advanced
status: docs-checked
description: "Write Binary Authorization project policies in YAML: default and cluster-specific rules, attestors with KMS keys, exempt image patterns, dry-run enforcement, and breakglass."
sources: ["https://cloud.google.com/binary-authorization/docs/policy-yaml-reference", "https://cloud.google.com/binary-authorization/docs/creating-attestors-cli", "https://cloud.google.com/binary-authorization/docs/using-breakglass", "https://cloud.google.com/binary-authorization/docs/enabling-dry-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary Authorization policy configuration

## 1. Attestor backed by Cloud KMS
```bash
gcloud container binauthz attestors create built-by-cloud-build-prod \
  --attestation-authority-note=projects/<P>/notes/build-note --attestation-authority-note-project=<P>
gcloud container binauthz attestors public-keys add --attestor=built-by-cloud-build-prod \
  --keyversion-project=<P> --keyversion-location=global --keyversion-keyring=binauthz \
  --keyversion-key=attestor-key --keyversion=1
```
An attestation records the registry path and **digest** of the image, signed with the signer's key. The `sign-and-create` command exists only in the beta track (`gcloud beta container binauthz attestations sign-and-create --artifact-url=<AR>/app@sha256:... --attestor=... --keyversion=...`).

## 2. Policy YAML
```yaml
globalPolicyEvaluationMode: ENABLE          # allow Google-maintained system images (GKE)
admissionWhitelistPatterns:
- namePattern: europe-docker.pkg.dev/<P>/base/*
defaultAdmissionRule:
  evaluationMode: REQUIRE_ATTESTATION
  enforcementMode: DRYRUN_AUDIT_LOG_ONLY
  requireAttestationsBy:
  - projects/<P>/attestors/built-by-cloud-build-prod
clusterAdmissionRules:
  europe-west1-b.dev-cluster:           # location.name
    evaluationMode: ALWAYS_ALLOW
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
```
```bash
gcloud container binauthz policy export > policy.yaml
gcloud container binauthz policy import policy.yaml
```
Start with `DRYRUN_AUDIT_LOG_ONLY`, read the audit logs for would-be denials, then switch to `ENFORCED_BLOCK_AND_AUDIT_LOG`.

## 3. Breakglass
Add the label `image-policy.k8s.io/break-glass: "true"` to the Pod spec to deploy an image the policy would block.
A breakglass event is always written to Cloud Audit Logs; alert on it. The older annotation
`alpha.image-policy.k8s.io/break-glass` still works but is no longer recommended.

## Gotchas
- Grant the `containeranalysis.notes.occurrences.viewer` role on the Artifact Analysis note to the attestor project's service account.
- `globalPolicyEvaluationMode: ENABLE` (the default) already allows Google-managed system images; Google advises against allowlisting them in `admissionWhitelistPatterns`.
- Wildcards are valid only at the end of a pattern. `*` matches images in the same directory only; `**` also matches subdirectories and can match other projects whose IDs share a prefix (`gcr.io/my-project**` also matches `my-project-exploit`).

## Verify
- [ ] Deploying an unattested image produces a dry-run audit log entry, or a block when enforced; an attested digest deploys.

## Checked
Date: 2026-10-28. Confirmed against the Binary Authorization policy YAML reference, Creating attestors (CLI), Using breakglass and Enabling dry-run pages: policy field names, enforcement modes, `location.name` cluster key format, wildcard rules, IAM role on the note, breakglass label and legacy annotation, audit logging. `sign-and-create` is beta-only per the CLI reference. Removed: the claim that tag-only references are always denied and the `imagePolicyWebhook` log detail (not on the pages), the claim that Cloud Build attestations come from a specific named attestor, and the service-agent wording for the IAM grant.
Method: documentation only; no commands were run.
