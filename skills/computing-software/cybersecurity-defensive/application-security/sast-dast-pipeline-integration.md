---
id: computing-software.cybersecurity-defensive.application-security.sast-dast-pipeline-integration
name: sast-dast-pipeline-integration
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sast, dast, iast, ci-cd-security, shift-left, security-gate, false-positive-rate, breaking-build, semgrep, codeql, owasp-zap, pipeline-security, developer-experience]
level: advanced
status: draft
description: "Wire SAST/DAST/IAST into CI/CD so it actually gets fixed: tool placement, gate thresholds that don't get bypassed, triage ownership, and keeping developer trust."
sources: ["OWASP DevSecOps Guideline (public)", "OWASP ZAP and Semgrep/CodeQL public documentation", "NIST SP 800-218 - Secure Software Development Framework (SSDF)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SAST/DAST pipeline integration — a scanner nobody acts on is a cost centre, not a control

**Goal:** get static (SAST), dynamic (DAST), and where applicable interactive
(IAST) scanning running automatically in the development pipeline in a way
developers actually fix findings from, instead of becoming a report nobody opens
or a gate everyone routes around.

## 1. Placement: different tools answer different questions at different speed
- **SAST** (source-code analysis — Semgrep, CodeQL, SonarQube, language-specific
  linters with security rules) runs fastest, on every commit/PR, catching
  injection patterns, hardcoded secrets, unsafe deserialization, and known
  anti-patterns before the code even merges. Cheap enough to gate PRs on.
- **SCA/dependency scanning** (see the companion skill) runs alongside SAST at
  the same cadence — different tool, same pipeline stage conceptually.
- **DAST** (dynamic scanning against a running instance — OWASP ZAP, Burp
  Suite-driven automation) needs a deployed environment, so it runs later —
  nightly or per-release against staging, not per-commit; it finds runtime/config
  issues SAST structurally can't (misconfigured headers, actual auth bypass
  behaviour, server-side issues only visible at runtime).
- **IAST** (instrumented in a running app during QA/test execution) sits between
  the two, catching what SAST misses due to framework/dynamic dispatch, with
  less noise than DAST because it has code-level context.
Don't run DAST against production unless it's been scoped, authorised, and
rate-limited — an aggressive scanner can functionally DoS a fragile endpoint or
trigger real side effects (test accounts created, emails sent, data mutated) if
pointed at prod without care.

## 2. Gate thresholds that survive contact with reality
A gate that blocks the PR on **any** finding gets bypassed via override/force-merge
within weeks once developers hit the first false positive on a deadline — this
destroys the gate's authority for every future real finding too. Gate on
severity + confidence: block merge on high-confidence critical/high findings in
new or changed code (not the whole codebase's existing debt — see below); let
medium/low findings surface as PR comments that don't block, tracked but not
gating. Revisit the threshold quarterly against actual false-positive rate data,
not opinion.

## 3. New/changed code vs. existing debt — don't conflate them
Turning a scanner on for the first time against a mature codebase surfaces
thousands of pre-existing findings — gating full build-breaking on all of them
instantly makes every PR impossible to merge and burns developer trust on day
one. Baseline the existing findings as tracked backlog (triaged, prioritised,
owned, same discipline as the exception-and-exposure-tracking pattern), and gate
only on **newly introduced** findings in the diff going forward. This is the
single most common reason a SAST/DAST rollout fails or succeeds.

## 4. Triage ownership and developer experience
Security doesn't scale to triage every finding for every team — train
and resource each engineering team to triage their own tool's findings with
security as an escalation/consult path for ambiguous or high-severity cases.
Findings need to appear where developers already work (PR comments, IDE
integration) with a clear remediation example, not just a CVE/CWE ID and a link
to a wall of documentation. A tool whose fix guidance is "upgrade" or "sanitise
input" with no concrete code example gets ignored more than one with a one-line
suggested diff.

## 5. Measure the program, not just scan counts
Track: mean time to remediate by severity, percentage of findings triaged within
SLA, false-positive rate per rule (tune or disable rules that are chronically
wrong rather than letting them erode trust in the whole tool), and — the metric
that actually proves value — whether the same vulnerability class recurs release
over release (if SQL injection keeps appearing despite the gate, the gate isn't
reaching the team or the rule coverage has a gap).

## Gotchas
- A scanner with default rulesets straight out of the box has a meaningfully
  higher false-positive rate than one tuned for your frameworks/languages —
  budget time for tuning before trusting gate decisions to it.
- DAST crawling behind authentication needs valid test credentials and a realistic
  app state; a DAST scan that can't log in silently covers almost nothing while
  reporting "scan complete."
- Secrets found by SAST in git history (not just the current commit) need
  separate handling — removing a secret from the latest commit doesn't remove it
  from history; it must be rotated regardless.
- A gate bypass/override mechanism with no required justification or follow-up
  ticket becomes the default path the moment it's used once under deadline
  pressure.

## Verify
- [ ] Each tool (SAST/SCA/DAST/IAST) runs at the pipeline stage matched to its
      speed and data needs.
- [ ] The merge gate blocks on new high-confidence critical/high findings only,
      not the full pre-existing backlog.
- [ ] Existing findings are tracked as an owned, prioritised backlog, not ignored
      or all gated at once.
- [ ] False-positive rate per rule is measured and acted on (tune/disable),
      not left to erode trust silently.
- [ ] Gate overrides require a logged justification and follow-up ticket.

Related: computing-software.cybersecurity-defensive.application-security.secure-code-review,
computing-software.cybersecurity-defensive.application-security.dependency-and-sbom-management,
computing-software.cybersecurity-defensive.vulnerability-management.risk-based-prioritisation
