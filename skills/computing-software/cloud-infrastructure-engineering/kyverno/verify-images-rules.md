---
id: computing-software.cloud-infrastructure-engineering.kyverno.verify-images-rules
name: verify-images-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [verifyimages, imagereferences, mutatedigest, verifydigest, imageregistrycredentials, attestors, image-cache]
level: advanced
status: docs-checked
description: "Configure legacy Kyverno verifyImages rules: imageReferences, digest handling, required, registry credentials, attestors count and the verification cache."
sources:
  - https://kyverno.io/docs/policy-types/cluster-policy/verify-images/overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rule fields:
- `type`: Sigstore Cosign or Notary.
- `imageReferences` (static strings, no variables) and `skipImageReferences`.
- `required`: default true; the validation webhook expects an immutable annotation marking each matching image verified.
- `mutateDigest`: default true; converts tags to digests when none is given (mutation webhook).
- `verifyDigest`: default true; validation checks the image uses a digest.
- `repository`: alternate repository for signatures.
- `imageRegistryCredentials`: `helpers` (`default`, `google`, `azure`, `amazon`, `github`) and `secrets` (Kyverno namespace; from 1.18 `namespace/name` can reference other namespaces). Falls back to global credentials if empty.
- `attestors`: one or more checks (public keys, certificates, keyless). `attestors.count` is how many `entries` must verify; unset means all.
- `attestations`: signed metadata; nested `attestors` verify its signature and `conditions` check its JSON.

Behaviour: runs in the mutation phase after other mutation rules and before the validation webhook; can be combined with autogen. From 1.18 a Pod's `spec.imagePullSecrets` are used automatically. Cross-namespace secrets need `get`, `list`, `watch` on secrets through a Role and RoleBinding in each target namespace for the admission and background controllers.

Static values are required in `imageReferences`, `match.resources.kinds`, `exclude.resources.kinds` and preconditions.

Cache, set on the admission controller: `imageVerifyCacheEnabled` true, `imageVerifyCacheMaxSize` 1000, `imageVerifyCacheTTLDuration` 60m. Entries persist until TTL or a policy change, so remote signature changes are not seen sooner. The page documents no `useCache` field.

## Checked

2026-11-03. Identifiers, flags, Helm values, defaults and version gates in this skill were checked against the official Kyverno documentation pages cited in `sources` (kyverno.io docs, fetched this batch). Where the pages did not document a field, the skill says so or the claim was left out.

Method: documentation only; no commands were run.
