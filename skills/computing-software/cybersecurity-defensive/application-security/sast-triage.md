---
id: computing-software.cybersecurity-defensive.application-security.sast-triage
name: sast-triage
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sast-triage, sast, false-positives, code-scanning, semgrep, finding-triage]
level: practitioner
status: docs-checked
description: "Triage SAST findings with GitHub code scanning and Semgrep: check source-to-sink paths, pick a status and reason, record why, and fix noisy rules."
sources: ["https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/triaging-code-scanning-alerts-in-pull-requests", "https://semgrep.dev/docs/semgrep-code/triage-remediation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAST finding triage

Both tools offer the same three outcomes: fix the code, triage the finding, or remove the
rule or code that produced it.

## GitHub code scanning in a pull request
- Results appear as check results and annotations; new alerts on changed lines are annotated.
  The check fails for severity `error`, `critical` or `high`; lower severities are warnings or
  notes and the check succeeds. Repository settings can override which severities fail.
- With write permission, annotations from tools such as CodeQL link to the source (where
  untrusted data enters) and Show paths shows the full source-to-sink path. Use it to decide
  whether the data is untrusted or whether the analysis missed a sanitization step.
- The alert page shows severity, type and CWE tags and the commit that introduced it. Its
  status reflects the default branch; other branches appear in Affected branches.
- Fixing: push a commit; if it fixes the problem the alert closes and the annotation goes.
- Dismissing: for example code used only for testing, or when the fix effort exceeds the
  benefit. You must choose a reason, which may affect whether a query continues to be used in
  future analysis. Add a comment: it goes into the alert timeline and serves as audit
  justification, and is readable through the REST API as `dismissed_comment`.
- If you dismiss a CodeQL alert as a false positive because of an unsupported sanitization
  library, GitHub suggests contributing to the CodeQL repository.
- Copilot Autofix suggestions must be assessed and tested before commit.

## Semgrep triage statuses
Open (default), Reviewing, To fix, Fixed, Ignored, and Provisionally ignored (set by
Multimodal autotriage; confirm to Ignored or reopen as To fix). Ignored reasons: False
positive, Acceptable risk, No time, No triage reason, Duplicate, Ignored via nosemgrep. Triage
is prioritisation by criteria your team sets, such as severity and coding standards.
- Ignoring handles a false positive without changing the rule or code; pick a reason and add a
  comment. A `nosemgrep` code comment also ignores a finding.
- Reopen an ignored finding at any time.
- Disabling a rule or ruleset on the Policies page stops it scanning; its existing findings
  stay open until a re-scan. Files can instead be added to the ignore list.
- A finding is Removed when its rule is disabled or changed, or its file path is gone or
  ignored. Removed findings do not count toward fix rate.
- Triage applies across branches and refs; at full scan a finding previously triaged on
  another branch takes the same state, but diff-aware scans do not auto-triage.
- Triage by PR or MR comment where enabled: `/fp <COMMENT>`, `/ar <COMMENT>`,
  `/other <COMMENT>` and `/open <REASON>`; not available in public repositories (except
  GitLab.com, GitLab Self-Managed and GitHub Enterprise Server).
- A bulk triage API accepts `new_triage_state` of open, reviewing, fixing, ignored or fixed;
  `new_triage_reason` requires state ignored.

## Verify
- [ ] Every dismissal or ignore has a reason and a comment saying why.
- [ ] A source-to-sink path was checked before calling a finding a false positive.
- [ ] Repeated false positives from one rule are handled by rule or path change, not bulk ignore.

## Checked
Confirmed 2026-11-09 against the GitHub Docs page on triaging code scanning alerts in pull requests and the Semgrep triage and remediation page (both read in full).
Removed as unconfirmed: the generic per-finding procedure (reachability, int() parsing, parameterised queries, severity rating factors), CodeQL custom sanitizer and Semgrep pattern-not tuning, the who-triages roles, the monthly sample of 10 dismissals, the CWE source, and the example nosemgrep rule id.
Method: docs-checked 2026-11-09 against docs.github.com triaging code scanning alerts in pull requests and semgrep.dev triage-remediation
