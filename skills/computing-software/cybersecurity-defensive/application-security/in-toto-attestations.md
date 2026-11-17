---
id: computing-software.cybersecurity-defensive.application-security.in-toto-attestations
name: in-toto-attestations
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [in-toto, attestations, slsa-provenance, supply-chain-security, provenance]
level: advanced
status: docs-checked
description: "Understand and consume in-toto attestations: layers, statement fields, the SLSA provenance v1 predicate and what verifiers must check."
sources: ["https://github.com/in-toto/attestation/blob/main/spec/README.md", "https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md", "https://slsa.dev/spec/v1.0/provenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in-toto attestations

An **in-toto attestation** is authenticated metadata about one or more software artifacts, intended for automated
policy engines such as in-toto-verify and Binary Authorization. It is compatible with the SLSA Attestation Model.

## Four layers
- **Predicate**: arbitrary metadata about the subject with a type-specific schema.
- **Statement**: binds the attestation to a subject and identifies the predicate type.
- **Envelope**: authentication and serialisation.
- **Bundle**: groups multiple attestations.

## Statement
```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "subject": [{"name": "...", "digest": {"<ALGORITHM>": "<HEX_VALUE>"}}],
  "predicateType": "<URI>",
  "predicate": {}
}
```
- `subject` is a required array of ResourceDescriptors; each element represents one artifact and MUST have `digest`
  set. Artifacts are matched purely by digest, so `name` and `uri` should be unique within the subject and are not what
  a verifier trusts.
- `predicateType` is a required TypeURI. The Statement `_type` stays `https://in-toto.io/Statement/v1` across spec
  1.x releases; a v2 spec would change it to `.../Statement/v2`.
- Consumers following the spec must ignore unrecognised predicate fields unless noted.

## SLSA provenance v1 predicate
`"predicateType": "https://slsa.dev/provenance/v1"` (always use this string, not the URL bar). Its purpose: consumers
can verify the artifact was built according to expectations, and others can rebuild it. Fields:
- `buildDefinition` (required for SLSA Build L1): `buildType`, `externalParameters`, `internalParameters` (optional),
  `resolvedDependencies`.
- `runDetails` (required for Build L1): `builder` (`id`, `builderDependencies`, `version`), `metadata`
  (`invocationId`, `startedOn`, `finishedOn`), `byproducts`.
- `builder.id` identifies the build platform: the transitive closure of everything trusted to run the build faithfully
  and record the provenance.
- `externalParameters` are untrusted, MUST be in the provenance and MUST be verified downstream; they MUST be complete
  at SLSA Build L3. Verifiers SHOULD reject unrecognised or unexpected fields in them.
- `internalParameters` are set by the trusted platform and need not be verified.
- `resolvedDependencies` records fetched inputs, for example the git commit a repository URI resolved to; completeness
  is best effort through Build L3.
- Note: the SLSA v1.0 spec page is marked Status: Retired; consult the current SLSA spec for new work.

## Practice
- Verify who produced the attestation (the builder identity), not merely that a signature exists; its value depends on
  the builder's isolation.
- Reference subjects by digest, since tags are mutable.
- Have an explicit expectation of what good provenance looks like (expected builder, build type and parameters).

## Verify
A verifier given an artifact finds a statement whose subject digest matches, the expected `predicateType`, a trusted
`builder.id`, and only expected `externalParameters`.

## Checked
Method: docs-checked 2026-11-09 against the in-toto attestation spec README, `v1/statement.md` (field list) and the
SLSA v1.0 provenance page (model, schema and field tables). Removed unconfirmed claims and sources not read: the
in-toto.io docs landing page and the Sigstore cosign page, so all cosign, `gh attestation`, `slsa-verifier`, Witness,
`actions/attest-build-provenance`, Kyverno and policy-controller commands, the DSSE envelope detail, and the CNCF
status.
