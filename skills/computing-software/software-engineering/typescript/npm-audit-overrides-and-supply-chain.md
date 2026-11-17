---
id: computing-software.software-engineering.typescript.npm-audit-overrides-and-supply-chain
name: npm-audit-overrides-and-supply-chain
category: computing-software
field: software-engineering
product: typescript
tags: [npm, npm-audit, npm-overrides, supply-chain-security, ignore-scripts, pnpm-overrides, dependabot, socket, malicious-packages, minimum-release-age]
level: practitioner
status: verified
description: "Triage npm audit findings, patch transitive vulnerabilities with overrides, and harden installs against malicious packages (lifecycle scripts, release-age delays)."
sources: ["https://docs.npmjs.com/cli/commands/npm-audit", "https://docs.npmjs.com/cli/configuring-npm/package-json#overrides", "https://pnpm.io/settings#minimumreleaseage", "https://docs.npmjs.com/cli/using-npm/scripts#ignoring-scripts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# npm audit, overrides and supply-chain hygiene

**Goal:** fix the vulnerabilities that matter, without breaking the build, and reduce
the chance that a compromised package runs code on dev machines or CI.

## Triage npm audit
```bash
npm audit --omit=dev            # runtime deps first; dev-only vulns rarely ship (needs a lockfile: without one it fails with ENOLOCK)
npm audit --json > audit.json
npm audit fix                   # semver-compatible upgrades only
```
- Avoid `npm audit fix --force`: npm docs say `--force` is needed when a fix requires changing dependency ranges, i.e. typically a MAJOR bump of a direct dep.
- Many advisories are ReDoS in build-time tools or unreachable code. Decide per finding:
  reachable at runtime with attacker input? If not, document and defer.
- Use `npm explain <pkg>` (or `pnpm why`) to see which direct dep pulls it in.

## Overrides for transitive fixes
```json
"overrides": {
  "semver": "^7.5.4",
  "some-lib": { "minimist": "1.2.8" }     // only under some-lib
}
```
pnpm 12.14: top-level `overrides:` in `pnpm-workspace.yaml` (tested; the `"pnpm": { "overrides" }` field in package.json was ignored there, though it is the older location); yarn: `resolutions`.
npm refuses an override that conflicts with a direct dependency range (tested: `EOVERRIDE`, "Override for semver@^6.0.0 conflicts with direct dependency"); reference the direct spec with `"$semver"` or leave the package out of `dependencies`.
Overrides force versions the parent never tested: run the tests, and remove the
override when the parent updates (leave a comment with the advisory id).

## Hardening against malicious packages
- Lifecycle scripts (`postinstall`) run arbitrary code at install. Disable by default:
  `npm config set ignore-scripts true` or `.npmrc ignore-scripts=true`; pnpm 10+ blocks
  dependency build scripts unless allowlisted (pnpm 12.14: `allowBuilds`; `onlyBuiltDependencies` no longer worked and an unreviewed build fails the install with `ERR_PNPM_IGNORED_BUILDS`; tested).
- Release-age delay: most malicious versions are pulled within days. pnpm
  `minimumReleaseAge: 1440` (minutes; the pnpm docs give 1440 as the default) refuses brand-new versions.
- Use `npm ci` with a committed lockfile (integrity hashes) so tampered tarballs fail.
- Typosquats: review new dependency names in PRs; tools like Socket or
  `npm view <pkg>` (age, maintainers, downloads) help.
- Automate updates with Dependabot/Renovate but group and delay non-security bumps.
- Prefer packages with npm provenance; `npm audit signatures` verifies registry
  signatures and provenance attestations (ran: "2 packages have verified registry signatures").

## Verify
- [ ] CI runs `npm audit --omit=dev --audit-level=high` (or a scanner) and fails on new highs.
- [ ] Every override has a comment and an issue to remove it.
- [ ] Install scripts are disabled or allowlisted.
