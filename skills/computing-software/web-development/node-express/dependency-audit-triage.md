---
id: computing-software.web-development.node-express.dependency-audit-triage
name: dependency-audit-triage
category: computing-software
field: web-development
product: node-express
tags: [vulnerable-dependencies, npm-audit, pip-audit, bundler-audit, sca, supply-chain]
level: practitioner
status: gated
description: "Triaging dependency vulnerability reports from npm audit, pip-audit and bundler-audit: reachability, dev vs prod, overrides, fix strategies and CI gating without alert fatigue."
sources:
  - https://docs.npmjs.com/cli/commands/npm-audit
  - https://github.com/pypa/pip-audit
  - https://github.com/rubysec/bundler-audit
  - https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency audit triage

Ran with npm 11.21.1, pnpm 10.34.7, pip-audit and audit-ci against `minimist@1.2.0` (prod) and `lodash@4.17.20` (dev): `npm audit --omit=dev` reported only the minimist critical prototype-pollution advisories and exited non-zero with `--audit-level=high`; `npm audit --json` has keys `auditReportVersion`, `vulnerabilities`, `metadata` (counts per severity); `pnpm audit --prod` needs a `pnpm-lock.yaml` (`ERR_PNPM_AUDIT_NO_LOCKFILE` otherwise); `pip-audit -r` reported `requests 2.19.0` with `PYSEC-2018-28`.

## 1. Run
```bash
npm audit --omit=dev                 # production deps only
npm audit --json > audit.json
pnpm audit --prod ; yarn npm audit --environment production   # yarn not run (gated: unconfirmed, source is paywalled or blocked)
pip-audit -r requirements.txt        # PyPI advisory DB + OSV
bundle exec bundler-audit check --update   # not run (gated: unconfirmed, source is paywalled or blocked)
osv-scanner scan -r .                # multi-ecosystem, uses lockfiles; not run here (gated: unconfirmed, source is paywalled or blocked)
```

## 2. Triage each finding
1. **Is it shipped?** Dev-only (test runner, bundler plugin) findings rarely matter for runtime; still fix build-time RCE in CI tooling.
2. **Is the vulnerable function reachable?** ReDoS in a parser you only call with trusted config is low risk; prototype pollution in a body parser handling user JSON is high.
3. **Severity in context** - CVSS is generic; network-exposed + user input = raise, offline CLI = lower.
4. Record the decision (ticket or an ignore file with reason + expiry).

## 3. Fix options in order
- Upgrade the direct dependency (`npm update pkg`, `npm install pkg@^x`).
- Transitive stuck behind an unmaintained parent: `overrides` (npm), `resolutions` (yarn), `pnpm.overrides`:
```json
"overrides": { "semver": "^7.5.4" }
```
  Test - forced versions can break parents. Ran: `mkdirp@0.5.1` pulls a vulnerable `minimist`; with `"overrides": { "minimist": "^1.2.8" }` npm installed 1.2.8 and `npm audit` reported 0 vulnerabilities.
- Replace abandoned packages.
- Temporary ignore with expiry: `audit-ci` allowlist (ran: allowlisted GHSA ids were dropped from the failure list and reported as "Found vulnerable allowlisted advisories"), `pip-audit --ignore-vuln ID` (flag confirmed in `--help`), `bundler-audit --ignore CVE-xxxx` (gated: unconfirmed, source is paywalled or blocked).
- Avoid `npm audit fix --force` - it installs semver-major changes blindly (npm itself warned "Will install minimist@1.2.8, which is outside the stated dependency range").

## 4. CI gating
`npx audit-ci --high --skip-dev --config audit-ci.jsonc` fails builds on high/critical prod findings not allowlisted (ran: without `--skip-dev`, audit-ci also failed on the dev-only lodash advisories; the option is `skip-dev` in the config file, default false). Run nightly too - new advisories appear without code changes. GitHub Dependabot alerts / `dependency-review-action` block PRs introducing vulnerable versions.

## 5. Noise control
npm audit flags many dev-tool ReDoS issues - scope to prod, set a severity threshold, and require reasons for ignores so the list does not become permanent.

## Verify
CI shows audit step green with an allowlist where every entry has a reason and expiry date; re-run after upgrades shows the advisory resolved.
