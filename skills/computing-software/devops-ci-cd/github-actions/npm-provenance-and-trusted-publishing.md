---
id: computing-software.devops-ci-cd.github-actions.npm-provenance-and-trusted-publishing
name: npm-provenance-and-trusted-publishing
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, npm-provenance, npm-trusted-publishing, npm-publish-oidc, npm-audit-signatures]
level: practitioner
status: docs-checked
description: "Publish npm packages from Actions with provenance and OIDC trusted publishing (no NPM_TOKEN): permissions, CLI versions, package.json requirements and verification."
sources: ["https://docs.npmjs.com/generating-provenance-statements", "https://docs.npmjs.com/trusted-publishers", "https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-nodejs-packages"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# npm provenance and trusted publishing

## 1. Trusted publishing (OIDC, no long-lived token)
On npmjs.com → package → Settings → **Trusted Publisher**: GitHub Actions, org/user, repository,
workflow **filename** (e.g. `release.yml`), optional environment.
```yaml
on: { release: { types: [published] } }
permissions: { contents: read, id-token: write }
jobs:
  publish:
    runs-on: ubuntu-latest          # GitHub-hosted runners only
    environment: npm
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, registry-url: https://registry.npmjs.org }
      - run: npm install -g npm@latest      # trusted publishing needs npm CLI >= 11.5.1 and Node >= 22.14.0
      - run: npm ci && npm run build
      - run: npm publish --access public
```
With trusted publishing from GitHub Actions or GitLab CI/CD, provenance is generated automatically (no
`--provenance` flag), for public packages published from public repositories.

## 2. Provenance with a token (older setups)
```yaml
- run: npm publish --provenance --access public
  env: { NODE_AUTH_TOKEN: "${{ secrets.NPM_TOKEN }}" }
```
Still needs `id-token: write`. Or set `"publishConfig": { "provenance": true }` in package.json.

## 3. Requirements and failures
- `package.json` `repository.url` must exactly match the GitHub repository.
- Self-hosted runners are not currently supported for trusted publishing.
- GitHub Actions needs `id-token: write`; a missing one, or a workflow filename that differs from the npm
  setting (include `.yml`; fields are case-sensitive), shows as `ENEEDAUTH` "Unable to authenticate".
  npm does not verify the configuration when you save it, so errors appear only at publish.
- A new trusted publisher must complete a first successful publish within 2 days or it expires; a
  package can have up to 10 trusted publishers.
- Provenance is not generated for private repositories, even for public packages.
- After switching to trusted publishing, revoke the old automation token and set package
  "Require two-factor authentication and disallow tokens".

## 4. Verify consumers
```bash
npm audit signatures            # verifies registry signatures and provenance attestations of installed deps
```

## Verify
- [ ] Publishing works with no NPM_TOKEN secret present.

## Checked

2026-10-31. Confirmed against the npm "Trusted publishing" and "Generating provenance statements" pages: Trusted Publisher settings and GitHub fields (organization, repository, workflow filename with extension, optional environment), npm CLI 11.5.1 and Node 22.14.0 minimums, GitHub-hosted runners only, id-token: write, automatic provenance conditions, --provenance and publishConfig for token-based publishing, ENEEDAUTH troubleshooting, repository.url match, private-repository provenance limitation, 2-day first-publish expiry, 10 publisher limit, "Require two-factor authentication and disallow tokens", and npm audit signatures.
Removed: the E422 and id-token error strings, the claim that private-repo provenance is rejected (the docs say it is not generated), the npm view attestations command and the provenance badge verify step.

Method: documentation only; no commands were run.
