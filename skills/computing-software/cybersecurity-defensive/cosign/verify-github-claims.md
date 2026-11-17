---
id: computing-software.cybersecurity-defensive.cosign.verify-github-claims
name: verify-github-claims
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, github-workflow, github-actions, certificate-github-workflow-repository, workflow-sha]
level: advanced
status: docs-checked
description: "Tighten keyless verification of GitHub Actions signatures with the certificate-github-workflow-* flags for name, ref, repository, sha and trigger."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub workflow certificate claims

Fulcio certificates issued from GitHub Actions OIDC tokens carry workflow claims. cosign verify can match them:

- `--certificate-github-workflow-name` the workflow name
- `--certificate-github-workflow-ref` the git ref the run was based on
- `--certificate-github-workflow-repository` the repository
- `--certificate-github-workflow-sha` the commit SHA
- `--certificate-github-workflow-trigger` the `event_name` that triggered the run

```
cosign verify \
  --certificate-identity-regexp '^https://github.com/ORG/REPO/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-github-workflow-repository ORG/REPO \
  --certificate-github-workflow-trigger push \
  $IMAGE
```

The flags appear on `verify`, `verify-attestation`, `verify-blob` and `verify-blob-attestation`. The help lists no regexp variants for them. Keyless verification still needs `--certificate-identity` (or `-regexp`) and `--certificate-oidc-issuer` (or `-regexp`).

## Checked

2026-11-04. Confirmed against the cosign verify, verify-attestation, verify-blob and verify-blob-attestation reference pages: all five `--certificate-github-workflow-*` flags with their claim descriptions on each command, the issuer example https://token.actions.githubusercontent.com, and that identity plus issuer must be set for keyless flows. Removed: the rationale paragraph, the claim that values are matched exactly and the claim about the owner/name repository format (none stated on the pages).

Method: documentation only; no commands were run.
