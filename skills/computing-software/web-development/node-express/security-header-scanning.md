---
id: computing-software.web-development.node-express.security-header-scanning
name: security-header-scanning
category: computing-software
field: web-development
product: node-express
tags: [mozilla-observatory, zap-baseline, security-headers-scan, owasp-zap, dast, security]
level: practitioner
status: docs-checked
description: "Scanning deployed sites for header and config weaknesses with MDN HTTP Observatory, securityheaders.com and OWASP ZAP baseline in CI, plus tuning rules and triaging results."
sources:
  - https://developer.mozilla.org/en-US/observatory
  - https://github.com/mdn/mdn-http-observatory
  - https://www.zaproxy.org/docs/docker/baseline-scan/
  - https://github.com/zaproxy/action-baseline
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security header scanning

## 1. Quick external checks
- **MDN HTTP Observatory** (developer.mozilla.org/en-US/observatory): tests CSP, HSTS, cookies, redirection, SRI, CORS, Referrer-Policy, X-Content-Type-Options, X-Frame-Options and the Cross-Origin Opener/Embedder/Resource policies.
- `curl -sI https://example.com | grep -iE "strict-transport|content-security|x-content-type|referrer-policy|permissions-policy|cross-origin"` in a smoke test.

## 2. ZAP baseline (passive) in CI
```bash
docker run --rm -v "$PWD:/zap/wrk:rw" -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://staging.example.com -r zap-report.html -c zap-rules.conf -I
```
- Spiders for 1 minute by default (`-m` changes it), waits for passive scanning and performs no attacks.
- `zap-rules.conf` sets each rule to `FAIL`, `WARN` or `IGNORE`: generate a starting file with `-g zap-rules.conf`.
- `-I` do not fail on warnings; drop it once rules are tuned. `-j` adds the modern (Ajax) spider for SPAs.
GitHub Actions: `zaproxy/action-baseline` with `rules_file_name` and an issue-writing option.

## 3. Active scanning
`zap-full-scan.py` (attacks) only against environments you own and can break, never production without agreement; API scans with `zap-api-scan.py -f openapi`.

## 4. Triage
- False positives: CSP "unsafe-inline" in `style-src` for frameworks that need it, cookies without `Secure` on localhost scans. Ignore with a reason in the rules file.
- Fix at the edge (CDN/proxy) or framework middleware so every route is covered, including error pages and static assets.
- Track grade over time; alert when a deploy drops the Observatory score.

## Verify
- [ ] CI job fails when a deploy removes HSTS or CSP from staging.

## Checked

2026-10-25 against the ZAP website docs (zaproxy/zaproxy-website), zaproxy/action-baseline action.yml and mdn/mdn-http-observatory source. Confirmed: zap-baseline.py spiders for 1 minute by default, then waits for passive scanning and does not attack; zap-baseline options -t, -r, -c, -g (generate config, all WARN), -I and -j (modern spider, Ajax by default); zap-full-scan.py performs actual attacks; zap-api-scan.py -f takes openapi, soap or graphql; zaproxy/action-baseline inputs include rules_file_name and allow_issue_writing; MDN Observatory test modules: CSP, HSTS, cookies, redirection, SRI, CORS, Referrer-Policy, X-Content-Type-Options, X-Frame-Options and the three Cross-Origin policies.

Method: documentation only; no commands were run.
