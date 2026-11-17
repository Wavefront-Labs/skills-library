---
id: computing-software.cybersecurity-defensive.threat-intelligence.adversary-emulation-mapping
name: adversary-emulation-mapping
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [adversary-emulation, mitre-attack, atomic-red-team, caldera, purple-team, detection-coverage-gap-analysis, ttp-mapping, attack-flow, breach-and-attack-simulation, red-team-vs-purple-team]
level: advanced
status: draft
description: "Map detection coverage against a real adversary's known TTPs and emulate them (Atomic Red Team/purple team) to find and close gaps before a real actor does."
sources: ["MITRE ATT&CK Enterprise matrix and MITRE ATT&CK Navigator (public)", "Atomic Red Team (Red Canary, public GitHub project)", "MITRE Center for Threat-Informed Defense - CALDERA and coverage mapping guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adversary emulation and coverage mapping — test against a real actor's playbook, not a generic checklist

**Goal:** know, with evidence rather than assumption, which techniques a relevant
threat actor uses that your detection stack would actually catch — and close the
specific gaps, instead of running a generic penetration test that doesn't reflect
how your real adversaries operate.

## 1. Pick the adversary profile deliberately
Not every org needs to emulate every ATT&CK technique equally — a retailer's
relevant adversary set (POS malware, card-skimming, commodity ransomware
affiliates) differs from a defence contractor's (targeted APT groups with
specific, documented TTPs). Use threat intel (your own incidents, ISAC
reporting, published actor profiles mapped to ATT&CK) to select a realistic
subset of techniques for your sector and exposure, rather than attempting to
cover the entire matrix — that's thousands of techniques/sub-techniques and
most orgs will never face most of them.

## 2. Build the coverage matrix before you test
In ATT&CK Navigator (or an internal equivalent), mark each relevant technique
with your current detection confidence: **no visibility** (no data source
covers it), **visibility but no detection** (data exists, no alert built),
**detected** (an alert exists), or **detected and validated** (the alert has
actually fired on a true positive or passed a controlled test). Most
organisations discover the matrix is full of "assumed detected" cells that are
really "visibility but no detection" — the gap only shows up once you test.

## 3. Emulate with Atomic Red Team (or equivalent) technique by technique
Atomic Red Team provides small, single-technique test scripts mapped directly
to ATT&CK technique IDs — run the specific atomic test for a technique in a
controlled environment (never production without explicit authorisation and a
rollback plan) and check whether the expected detection fired. This is **purple
teaming**: red (offense) and blue (detection) working together in real time,
immediately confirming or denying detection, which is faster and cheaper than a
full red-team engagement for coverage-gap discovery — reserve a full red team
(more info in the companion application-security/network skills) for testing the
end-to-end chain and human response, not individual technique coverage.

## 4. For larger-scale automated testing, use a C2 framework like CALDERA
For testing multi-step attack chains or running repeatable, scheduled coverage
regression (confirm detections that worked last quarter still work after a SIEM
or EDR config change), an adversary emulation platform (CALDERA, or a commercial
breach-and-attack-simulation product) automates sequences of techniques and
reports pass/fail against expected detections. Treat detection regression
testing as a CI-like discipline — a SIEM content update or EDR policy change can
silently break a previously-working detection, and without scheduled re-testing
you won't know until a real incident shows the gap.

## 5. Close the loop: every gap becomes a tracked action
A coverage gap found in testing and not acted on is just documentation of a risk
you knew about and left open. Route each gap to the owner who can close it:
no visibility → log onboarding (see data-onboarding-and-cim-mapping); visibility
but no detection → a new SPL/KQL/EQL rule (see spl-detection-searches); detected
but didn't fire in test → tune the existing rule. Track time-to-close on gaps the
same way vulnerability management tracks remediation SLAs.

## Gotchas
- Running atomic tests in production without a named approver and rollback plan
  can trigger real containment actions (EDR auto-isolating a "malicious" test
  process) — coordinate with the SOC and get it explicitly whitelisted/expected
  for the test window, or you'll generate a real incident response to your own test.
- A technique marked "detected" based on a vendor's marketing claim for their
  product, never actually tested in your environment, is not evidence —
  only a confirmed fired-alert from your own test counts.
- Over-indexing on ATT&CK technique IDs alone misses technique *variations* —
  an adversary can achieve the same tactic with a slightly different procedure
  that your specific detection logic doesn't catch; test more than one atomic per
  technique where available.
- Purple-teaming cadence that only happens once a year leaves most of the year
  with unknown detection drift from config/content changes — prioritise
  retesting your highest-value techniques more frequently.

## Verify
- [ ] A coverage matrix exists distinguishing no-visibility / visibility-only /
      detected / validated, built from a realistic adversary profile.
- [ ] Atomic/technique-level tests were run in a controlled, authorised window
      with the SOC aware in advance.
- [ ] Every gap found has an owner, a remediation type (onboarding, new
      detection, tuning), and a tracked close date.
- [ ] High-value technique detections are re-tested on a recurring cadence, not
      just once.

Related: computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling,
computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology
