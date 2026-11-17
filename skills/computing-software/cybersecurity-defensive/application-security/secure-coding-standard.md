---
id: computing-software.cybersecurity-defensive.application-security.secure-coding-standard
name: secure-coding-standard
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secure-sdlc, secure-coding-standard, owasp-asvs, coding-guidelines, cert-coding-standards, enforceable-rules, linters]
level: practitioner
status: draft
description: "Write and enforce a secure coding standard: scope it to your stacks, derive requirements from ASVS, make each rule testable and back it with linters or SAST rules."
sources: ["OWASP Application Security Verification Standard 4.0.3 / 5.0", "OWASP Secure Coding Practices Quick Reference Guide", "SEI CERT Coding Standards"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure coding standard

**Goal:** a short, stack-specific standard developers can follow and tooling can check, instead
of a 60-page PDF nobody reads.

## Build it
1. **Scope:** list languages and frameworks actually in use (e.g. Java/Spring, TypeScript/React, Python/Django).
2. **Source requirements** from OWASP ASVS: pick a target level (L1 for all apps, L2 for apps handling sensitive data).
   ASVS chapters map naturally to standard sections: authentication, session, access control, validation and encoding,
   cryptography, error handling and logging, data protection, communications, configuration.
3. **Write each rule as an enforceable statement with a code example**, for example:
   - "All SQL uses parameter binding; string concatenation into queries is forbidden." Good/bad snippet per stack.
   - "Templates use auto-escaping; `|safe`, `dangerouslySetInnerHTML`, `th:utext` require a security review label."
   - "Passwords hashed with Argon2id or bcrypt via the shared library; no direct calls to MessageDigest/hashlib for passwords."
   - "Secrets never in source; loaded from the secrets manager client."
4. **Map each rule to a check:** Semgrep/CodeQL rule id, linter rule (e.g. ESLint `no-eval`, Bandit B608), or
   manual review checklist item. Rules with no check get a review checklist entry.
5. **Exceptions process:** documented waiver with owner, reason, expiry.

## Roll-out
- Publish as Markdown in a repo; changes via PR reviewed by AppSec and a champion.
- Train with the rules your SAST already flags most often.
- Version the standard; tag rules with the ASVS requirement id for traceability.

## Gotchas
- Copying generic guidance (validate all input) without saying how in your framework.
- Rules that tooling cannot see and nobody reviews are decoration; either automate or drop them.
- Language-specific traps: Java deserialisation, Python `pickle`/`yaml.load`, JS prototype pollution, PHP `unserialize`; include them for the stacks you have.

## Verify
- [ ] Each rule has an example, a check, and an ASVS reference.
- [ ] SAST config in CI contains the rule ids the standard cites.
- [ ] Waivers have expiry dates and are reviewed.
