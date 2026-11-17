---
id: computing-software.software-engineering.typescript.publishing-npm-packages
name: publishing-npm-packages
category: computing-software
field: software-engineering
product: typescript
tags: [npm, npm-publish, npm-provenance, trusted-publishing, package-json, files-field, exports-field, changesets, dist-tags, publint]
level: practitioner
status: verified
description: "Publish TypeScript packages to npm correctly: files/exports/types fields, checking the tarball, provenance and trusted publishing from CI, dist-tags and versioning."
sources: ["https://docs.npmjs.com/cli/commands/npm-publish", "https://docs.npmjs.com/generating-provenance-statements", "https://docs.npmjs.com/trusted-publishers", "https://publint.dev/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing npm packages

**Goal:** a package that installs and type-checks for consumers in both ESM and CJS
setups, contains only what it should, and is published from CI with provenance.

## package.json essentials
```json
{
  "name": "@acme/util",
  "version": "1.4.0",
  "type": "module",
  "files": ["dist"],
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js", "require": "./dist/index.cjs" },
    "./package.json": "./package.json"
  },
  "main": "./dist/index.cjs",
  "types": "./dist/index.d.ts",
  "sideEffects": false,
  "publishConfig": { "access": "public" }
}
```
- `files` is an allowlist; without it you ship tests, sources, maybe `.env`.
- `types` must come first inside each exports condition.
- `exports` blocks deep imports not listed; adding it to an existing package is a
  breaking change.

## Check before publishing
```bash
npm pack --dry-run                 # list files in the tarball
npx publint                         # exports/types/format mistakes
npx @arethetypeswrong/cli --pack .  # types resolution under node16/bundler/CJS
```

## Publish from CI with provenance / trusted publishing
Configure the package on npmjs.com as a trusted publisher for your GitHub repo and
workflow (npm docs: requires npm CLI 11.5.1+ and Node 22.14.0+), then:
```yaml
permissions: { id-token: write, contents: read }
steps:
  - run: npm ci && npm run build && npm test
  - run: npm publish --provenance --access public
```
Trusted publishing uses OIDC instead of a long-lived `NPM_TOKEN`, and provenance links
the tarball to the commit and workflow that built it. Per the npm docs, publishing via trusted publishing from GitHub Actions or GitLab CI generates provenance automatically, so `--provenance` is optional there.

## Versioning and dist-tags
- SemVer strictly: removing an export or raising the minimum Node version is MAJOR.
- Pre-releases: `npm publish --tag next` so `npm install pkg` still gets `latest`.
  Publishing a beta without `--tag` makes it `latest` (the npm-publish docs give the `tag` default as `latest`).
- Changesets (`@changesets/cli`) or semantic-release automate version bumps and changelogs.
- `npm unpublish` is restricted (npm policy): within 72 hours if nothing depends on the package; after that only if no dependents, under 300 downloads in the last week and a single owner. A used `name@version` can never be republished. Prefer `npm deprecate pkg@1.4.0 "use 1.4.1"`.

## Verify
- [ ] `npm pack` tarball contains only `dist`, README, LICENSE, package.json.
- [ ] A scratch project imports it via ESM and CJS and type-checks.
- [ ] npm package page shows the provenance badge.
