---
id: computing-software.devops-ci-cd.secrets-management.witness-and-archivista-attestations
name: witness-and-archivista-attestations
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, witness, archivista, in-toto, attestation-policy, supply-chain-security, slsa]
level: practitioner
status: gated
description: "Record in-toto attestations for every CI step with witness, store and query them in Archivista, and verify artifacts against a signed witness policy before deploy."
sources:
  - https://witness.dev/docs/
  - https://github.com/in-toto/witness
  - https://github.com/in-toto/archivista
  - https://in-toto.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# witness and archivista

witness (in-toto project) wraps any command, observes it (materials, products, environment, git state, CI context) and emits a signed in-toto attestation. Archivista stores attestations in a graph you can query by artifact digest. A witness **policy** says which steps must have happened, by whom, before an artifact is trusted.

## Wrap CI steps
```bash
witness run --step build \
  --signer-file-key-path build.key \                # or --signer-fulcio-url for keyless Sigstore
  --attestations environment,git,github,material,product \
  --enable-archivista --archivista-server https://archivista.example.com \
  -o build.attestation.json -- make build
witness run --step test -k build.key -a git,material -- go test ./...
```
Run on witness v0.12.0 with an ed25519 key from `openssl genpkey -algorithm ed25519`: `witness run --step build -k build.key -a environment,git,material,product -o out.json -- ...`
wrote a DSSE envelope (`application/vnd.in-toto+json`) whose collection statement lists the environment, git, material, command-run and product attestations
(`material`, `product` and `command-run` always run; the `git` attestor fails with `repository does not exist` outside a git repository).
GitHub Action: `testifysec/witness-run-action` with `step:` and `command:` inputs; it can sign keylessly with the workflow's OIDC token.
Archivista upload, Fulcio keyless signing and the Action were not run (gated: unconfirmed, no server or OIDC token). `witness attestors list` shows the available attestors (e.g. `slsa`, `sbom`, `vex`, `secretscan`, `lockfiles`, `oci`, `docker`, `command-run`).
Attestors worth knowing: `material`/`product` (file digests in/out), `git`, `github`/`gitlab` (CI run identity), `sbom`, `slsa` (provenance), `command-run`, `secretscan`.

## Policy
```json
{
  "expires": "2027-01-01T00:00:00Z",
  "steps": {
    "build": {
      "name": "build",
      "functionaries": [{ "type": "root", "certConstraint": { "uris": ["https://github.com/org/repo/.github/workflows/release.yml@refs/heads/main"], "roots": ["fulcio"] } }],
      "attestations": [{ "type": "https://witness.dev/attestations/github/v0.1" }, { "type": "https://witness.dev/attestations/material/v0.1" }]
    },
    "test": { "name": "test", "artifactsFrom": ["build"], "attestations": [{ "type": "https://witness.dev/attestations/command-run/v0.1",
      "regopolicies": [{ "name": "exit-zero", "module": "<base64 rego: deny if exitcode != 0>" }] }] }
  }
}
```
Sign it: `witness sign -f policy.json -k policy.key -o policy-signed.json` (run: worked; a key-based policy uses `functionaries: [{type: publickey, publickeyid}]` plus a `publickeys` map instead of `certConstraint`).

## Verify before deploy
```bash
witness verify -f dist/app -p policy-signed.json -k policy.pub \
  --enable-archivista --archivista-server https://archivista.example.com
```
(gated: unconfirmed: `witness verify -f dist/app -p policy-signed.json -k policy.pub -a build.att.json` printed `policy signature verified` here but then failed with `predicate type  is not a collection predicate type` on Windows, so the full verify path was not confirmed; flags `-f -p -k -a -s --directory-path` exist in `verify --help`.)
witness looks up all attestations whose products include the artifact digest, checks signatures, functionaries, the step chain (`artifactsFrom`) and Rego rules. Non-zero exit = block the deploy.

## Archivista
Run with a MySQL/Postgres backend and blob storage; query via GraphQL:
```graphql
{ dsses(where: { hasStatementWith: { hasSubjectsWith: { hasSubjectDigestsWith: { value: "sha256..." } } } }) { edges { node { gitoidSha256 } } } }
```
Use it to answer: which pipeline built this image, from which commit, which tests ran.

## Pitfalls
- Policy expiry is mandatory; an expired policy fails all verifications - automate renewal.
- Material attestors hash the working directory: large repos slow builds; scope with `--dirhash-glob`.
- Keyless signing requires `id-token: write` permission in GitHub Actions.

## Verify
- [ ] Tampering with the binary after build makes `witness verify` fail.
- [ ] Archivista returns the attestation chain for the released digest.
