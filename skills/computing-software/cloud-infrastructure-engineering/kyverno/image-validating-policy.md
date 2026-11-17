---
id: computing-software.cloud-infrastructure-engineering.kyverno.image-validating-policy
name: image-validating-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [imagevalidatingpolicy, cosign, keyless, attestors, attestations, verifyimagesignatures, notary]
level: advanced
status: docs-checked
description: "Write Kyverno ImageValidatingPolicy: matchImageReferences, cosign and notary attestors, attestations, credentials and the verify CEL functions."
sources:
  - https://kyverno.io/docs/policy-types/image-validating-policy/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ImageValidatingPolicy` (stable since v1.19) extends ValidatingPolicy; `NamespacedImageValidatingPolicy` has identical fields within its namespace.

- `images`: Pods and pod templates are extracted automatically. For custom resources or JSON set `evaluation.mode: JSON` and a CEL `expression` under `images`.
- `matchImageReferences`: needs `glob` or a CEL `expression`.
- `attestors` (named): `cosign.key` (`expression`, `kms`, `hashAlgorithm`, `data`), `cosign.keyless` (`identities` with `subject`, `issuer`, `subjectRegExp`, `issuerRegExp`; `trustedRoot`; `roots`, system roots if omitted), `cosign.ctlog` (`url`, `rekorPubKey`, `ctLogPubKey`, `tsaCertChain`, `insecureIgnoreTlog`, `insecureIgnoreSCT` for testing only), `cosign.certificate`, `cosign.source`, `cosign.tuf`, and `notary` (`certs`, optional `tsaCerts`).
- `attestations`: named, with `referrer.type` (OCI artifact type) or `intoto.type` (predicate type URI).
- `validationConfigurations`: `mutateDigest`, `verifyDigest`, `required` (examples set all true).
- `credentials`: `allowInsecureRegistry`, `providers` (`default`, `google`, `azure`, `amazon`, `github`), `secrets` (must be in the Kyverno namespace).

CEL: `images.containers`; `verifyImageSignatures(image, [attestors.X])` returns a count (check `> 0`); `verifyAttestationSignatures(image, attestations.X, [attestors.Y])`; `extractPayload(image, attestations.X)` errors unless `verifyAttestationSignatures()` ran first.

Caveats: attestation names with special characters need bracket syntax, so prefer camelCase or snake_case. The namespaced example calls `imageverify.verify(...)`, which is not in the function table; check it. Bypass resources with PolicyException.

## Checked

2026-11-08. Claims were read against: https://kyverno.io/docs/policy-types/image-validating-policy/.

Method: documentation only; no commands were run.
