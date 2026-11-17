---
id: computing-software.cybersecurity-defensive.application-security.secure-code-review
name: secure-code-review
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [application-security, appsec, secure-code-review, code-review, owasp-asvs, sources-and-sinks, data-flow, broken-access-control, idor, injection, sast, owasp-cheat-sheets]
level: practitioner
status: docs-checked
description: "Review code for security bugs: choose baseline or diff review, trace sources to sinks, check authorisation, and use SAST output to focus human effort."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure code review — follow the data, check the authorisation

**Goal:** find the security bugs that automated tools miss (business logic,
authorisation logic, race conditions, cryptographic misuse) and use tooling for the
repeatable ones.

## 1. Pick the review type
- **Baseline review:** the whole codebase. Use for new applications or major releases,
  onboarding legacy systems, compliance requirements and post-incident analysis.
- **Diff-based review:** code changes only. Use for pull requests, feature completion
  and continuous validation; also hotfixes, which need a rapid review.
- **Hybrid:** baseline-review high-risk components and diff-review routine changes;
  escalate from diff to baseline when a significant concern appears.

## 2. Prepare
All reviews: understand the architecture and business requirements, gather threat
models and earlier findings, identify critical assets and high-risk functions, read the
security requirements. Baseline reviews also map application boundaries and
dependencies, review incident history and audit third-party libraries. Diff reviews
identify the modified files and affected components, the impact on existing security
controls, and the purpose of the change.

## 3. Review process
- **Baseline steps:** architecture anti-patterns, entry points and input validation,
  authentication and authorisation, data flow tracing, business logic, cryptography,
  error handling, configuration and deployment.
- **Diff steps:** impact on existing controls, new attack vectors, security at modified
  trust boundaries, new integrations, and regression of existing protections.

## 4. Techniques
- **Code pattern analysis:** focus on input handling, query construction and ORM use,
  file and path handling, authentication and session logic, access checks, cryptographic
  operations and key management, error handling and logging, configuration loading.
- **Data flow analysis:** identify sources (user input, uploads, API calls, database
  reads, environment variables), follow processing (validation, transformation, caching),
  check sinks (queries, file writes, output rendering, logging, external APIs), and
  verify validation and output encoding at each trust boundary.
- **Threat-based review:** align with the OWASP Top 10, STRIDE, attack trees and abuse
  cases.
- **Business logic:** check state transitions, race conditions and time-of-check versus
  time-of-use gaps, transaction integrity and rollback, resource limits, authorisation
  at each workflow step, and ways to skip steps.

## 5. Checklist highlights (from the cheat sheet)
- All input validated server-side, allowlists over blocklists, context-appropriate
  output encoding.
- SQL via parameterised queries (or safely implemented stored procedures) with user data
  passed as parameters, never concatenated.
- Access control enforced server-side, default deny, centralised decisions, IDOR
  prevented, administrative functions protected, roles not manipulable.
- Session tokens with at least 128 bits of entropy, invalidated on logout and timeout,
  cookies with HttpOnly, Secure and SameSite.
- Cryptography: cryptographically secure random generation, certificate validation
  including hostname checks, IV and nonce handling that follows the chosen mode (CBC needs
  unpredictable IVs; GCM needs IV uniqueness under each key).
- No hardcoded secrets; no sensitive data in logs or error messages.
- Security events (authentication failures, authorisation violations) logged.

## 6. Use tools to support, not replace, the human
Run SAST and dependency scanning before the manual pass to prioritise areas, then
validate the findings with human judgment (false-positive filtering) and spend manual
time on what tools cannot analyse. The cheat sheet suggests tracking manual review
coverage, finding quality (valid findings over total), review efficiency and trend.

## 7. Report
A finding record in the cheat sheet carries: title, severity, CWE, location, description,
impact, reproduction, recommendation, references, status, assignee and due date. A
review summary lists application, version or commit, reviewers, date, scope, counts by
severity, key recommendations and overall risk.

## Verify
- [ ] Review type chosen and scope recorded.
- [ ] Entry points listed, each with its authentication and object-level authorisation
  check noted.
- [ ] Each untrusted source reaching a sink was traced and validated or encoded at the
  boundary.
- [ ] Tool findings triaged by a person; business-logic paths reviewed manually.
- [ ] Findings filed with location, impact and fix guidance.

Related: computing-software.cybersecurity-defensive.threat-modelling.stride-threat-modelling

## Checked
Method: docs-checked 2026-11-09 against the OWASP Secure Code Review Cheat Sheet (read in full). Removed as unconfirmed by that page: OWASP Top 10 ranking claim, the sink-to-safe-pattern table (SSRF DNS-rebinding, deserialisation loaders), password hashing algorithm names, JWT algorithm pinning, named CI tools and flags (Semgrep, CodeQL, osv-scanner, gitleaks, Dependabot), Orient time box, the Rails IDOR example and grep helpers.
