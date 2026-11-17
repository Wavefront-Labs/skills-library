---
id: computing-software.cryptography-implementation.secure-implementation.static-analysis-for-crypto-misuse
name: static-analysis-for-crypto-misuse
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, crypto-code-review, crypto-static-analysis, cwe-327, gosec, bandit]
level: advanced
status: docs-checked
description: "Detect crypto API misuse automatically with Bandit and gosec: the cryptography rule IDs, suppression with justification, and CI triage."
sources: ["https://cwe.mitre.org/data/definitions/327.html", "https://github.com/securego/gosec", "https://bandit.readthedocs.io/en/latest/plugins/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static analysis for crypto misuse

Many crypto bugs in application code are API misuse with recognisable patterns. CWE-327 defines
the weakness as the product using a broken or risky cryptographic algorithm or protocol.
Static analysis finds such patterns cheaply in CI.

## Bandit (Python)

Bandit groups its test IDs: B5xx are cryptography tests (B3xx and B4xx are call and import
blacklists, B1xx misc, B2xx framework misconfiguration, B6xx injection, B7xx XSS). Relevant
plugins from the listing:

| ID | Plugin |
|---|---|
| B324 | hashlib |
| B501 | request_with_no_cert_validation |
| B502 | ssl_with_bad_version |
| B503 | ssl_with_bad_defaults |
| B504 | ssl_with_no_version |
| B505 | weak_cryptographic_key |
| B507 | ssh_no_host_key_verification |
| B105-B107 | hardcoded password string, function argument, default |

Bandit config files are optional from 1.0; custom tests are plugins registered through the
`bandit.plugins` entry point.

## gosec (Go)

gosec can restrict rules: `-include=G101,G203,G401` runs only those, and `-exclude-rules`
excludes rules per path pattern. Suppress a finding with a `#nosec` comment on the offending
line, naming the rule and optionally a justification:
`#nosec [RuleList] [-- Justification]`, for example `// #nosec G402` or
`//#nosec G101 G102 -- This is a false positive`. The alternative `//gosec:disable` directive
works similarly. `-nosec=true` ignores the annotations, and `-nosec-require-rules` and
`-nosec-require-justification` reject naked or unjustified directives.

## Triage and gating

- Start in report-only mode, triage findings, then gate new findings on pull requests.
- Require a justification on every suppression and enforce it with the gosec flags above.
- Static analysis does not replace human review of design (key hierarchy, nonce handling).

## Verify

- [ ] Bandit B5xx and gosec crypto rules run on every PR in the relevant languages.
- [ ] Suppressions carry rule names and justifications.

## Checked

Method: docs-checked 2026-11-09 against CWE-327 (description), Bandit plugin index page (ID groupings and full plugin listing), gosec README (rule selection and #nosec sections; the page lists suppression syntax but not the meaning of individual G-rules). Removed: the Semgrep and CodeQL rows and their pack and query names, SpotBugs, CryptoGuard and CogniCrypt, gosec rule meanings (G401, G402, G404, G505), Bandit IDs B303, B311 and B413 (not in the current listing), the sample Semgrep custom rules, and the claim that MD5/SHA-1 for cache keys is a common false positive.
