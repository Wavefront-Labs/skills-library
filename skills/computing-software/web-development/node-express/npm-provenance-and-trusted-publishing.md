---
id: computing-software.web-development.node-express.npm-provenance-and-trusted-publishing
name: npm-provenance-and-trusted-publishing
category: computing-software
field: web-development
product: node-express
tags: [npm-provenance, trusted-publishing, sigstore, npm-audit-signatures, oidc-publishing, supply-chain]
level: practitioner
status: docs-checked
description: "Publishing npm packages without long-lived tokens: trusted publishing via OIDC from CI, provenance attestations, verifying with npm audit signatures, and token hygiene."
sources:
  - https://docs.npmjs.com/trusted-publishers
  - https://docs.npmjs.com/generating-provenance-statements
  - https://docs.npmjs.com/about-access-tokens
  - https://docs.npmjs.com/cli/v11/commands/npm-audit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# npm provenance and trusted publishing

Long-lived npm tokens are a credential attackers can steal. Remove the token.

## 1. Trusted publishing (OIDC)
1. On npmjs.com > package > Settings > Trusted publisher: add GitHub Actions (org, repo, workflow file name, optional environment), GitLab CI/CD or CircleCI. Self-hosted runners are not supported. Each configuration also selects the allowed publish action (`npm stage publish` is always allowed; direct `npm publish` is optional).
2. Workflow:
```yaml
permissions: { contents: read, id-token: write }
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: npm-release
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, registry-url: "https://registry.npmjs.org" }
      - run: npm ci && npm test && npm run build
      - run: npm publish --access public      # npm CLI 11.5.1+ and Node 22.14+; exchanges the OIDC token, no NPM_TOKEN
```
Packages published this way get provenance automatically. Then disallow token publishing in package settings ("Require two-factor authentication and disallow tokens").

## 2. Provenance with tokens (older setups)
`npm publish --provenance` from GitHub Actions/GitLab with `id-token: write` creates an attestation, signed by Sigstore public good servers and logged in a public transparency ledger, that links the package to its source and build instructions.

## 3. Consumers: verify
```bash
npm audit signatures      # verifies registry signatures and provenance attestations for installed deps
```
Prefer dependencies with provenance; a version suddenly published without provenance (when earlier ones had it) is a red flag.

## 4. Token hygiene where tokens remain
- Granular access tokens scoped to specific packages, read-only where possible, short expiry; legacy tokens were removed in November 2025.
- 2FA on every maintainer account (security keys over TOTP).
- Protect the release workflow: required reviewers on the `npm-release` environment, tag protection, pinned actions by SHA.

## Verify
- [ ] Package page shows provenance; repo secrets contain no `NPM_TOKEN`; publishing from a laptop fails.

## Checked

2026-10-25 against the npm documentation repository (npm/documentation, 2026-10-24) and the npm CLI docs. Confirmed: trusted publishing needs npm CLI 11.5.1+ and Node 22.14+ and supports GitHub Actions, GitLab CI/CD and CircleCI cloud; provenance is generated automatically for trusted publishing without the --provenance flag; publishing access setting is named "Require two-factor authentication and disallow tokens"; provenance is signed by Sigstore public good servers and logged in a public transparency ledger; legacy (classic) tokens were removed in November 2025 and only granular access tokens remain.

Method: documentation only; no commands were run.
