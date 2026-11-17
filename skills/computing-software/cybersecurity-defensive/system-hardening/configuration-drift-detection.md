---
id: computing-software.cybersecurity-defensive.system-hardening.configuration-drift-detection
name: configuration-drift-detection
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [configuration-drift, compliance-monitoring, continuous-compliance, ansible, chef-inspec, osquery, auto-remediation, drift-alerting, baseline-enforcement, infrastructure-as-code-drift]
level: advanced
status: draft
description: "Detect when a hardened baseline silently drifts after deployment: continuous compliance scanning, IaC drift detection, auto-remediation trade-offs, and alerting on the right signal."
sources: ["Chef InSpec documentation (public)", "osquery documentation (public)", "CIS-CAT and CIS Benchmark continuous compliance guidance (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration drift detection — a hardened baseline decays the moment it ships

**Goal:** catch the gap between "we hardened this to the baseline at build time"
and "this is still compliant with the baseline today" — every manual change,
emergency fix, and skipped maintenance window erodes a baseline, and most of
that erosion is invisible without continuous checking.

## 1. Drift happens for legitimate reasons, not just mistakes
A firewall rule opened "temporarily" for a vendor support session and never
closed, a service re-enabled to troubleshoot an outage and left running, a
registry/sysctl setting changed by a well-meaning admin chasing a performance
issue — these are normal operational reality, not just carelessness, and a
compliance program that treats every drift as a violation to be punished rather
than a signal to investigate will train people to hide changes instead of
documenting them. Design the detection-and-response loop around "find it fast,
understand why, decide whether to revert or accept" rather than pure gotcha
enforcement.

## 2. Continuous scanning vs. point-in-time audit
A quarterly or annual compliance scan finds drift that's been present for
months by the time anyone looks — the exposure window is the gap between scans.
Run baseline compliance checks (Chef InSpec profiles, osquery scheduled queries,
CIS-CAT, or a cloud-native equivalent) on a short, automated cadence (daily is
common for security-relevant controls) rather than relying on periodic audits
alone. Point-in-time audits still have a role (independent verification, audit
evidence for a specific compliance framework) but shouldn't be the only
detection mechanism.

## 3. Infrastructure-as-code drift is a distinct, additional problem
Beyond OS-level config drift, cloud resources managed by Terraform/CloudFormation
can drift when someone makes a change directly in the console that the IaC state
doesn't know about — `terraform plan` showing unexpected changes on a routine
run is drift detection for free, if anyone's actually running and reading it
regularly rather than only at deployment time. Treat an unexpected `terraform
plan` diff found outside of an intentional change window as a security signal
worth investigating, not just an IaC hygiene issue.

## 4. Auto-remediation: know when it's right and when it's dangerous
Auto-reverting drift (a config management tool enforcing desired state on every
run) is appropriate for well-understood, low-risk settings (a registry key, a
sysctl value) where reverting can't plausibly break something a human
intentionally changed for an operational reason. It's dangerous for settings
that get legitimately and frequently adjusted for operational reasons (a
firewall rule opened for an active, approved maintenance task) — auto-reverting
those mid-task causes outages and teaches people to work around the compliance
tool. Classify controls by auto-remediation safety explicitly rather than
applying one global policy; the companion cis-benchmark-baselines skill's
control list is a reasonable starting point for which controls are safe to
auto-enforce.

## 5. Alert on the signal that matters, not every delta
A drift-alerting system that fires on every detected change (including
authorised, ticketed ones) trains recipients to ignore it. Suppress or
auto-close drift that correlates with an approved change ticket/window, and
reserve active alerting for drift with no matching authorisation — this mirrors
the alert-fatigue lesson from SOC alert triage and is just as real a failure
mode here.

## Gotchas
- A drift-detection tool that only checks the settings it was configured to
  check at rollout time misses new baseline controls added later — keep the
  check definitions synced with the current baseline, not frozen at initial setup.
- Config management tools can themselves be the drift source if their own
  policy/cookbook/playbook repo isn't change-controlled — review changes to the
  enforcement logic with the same rigor as the systems it enforces on.
- Drift found and silently "fixed" by auto-remediation with no logging leaves no
  record that a potentially suspicious change happened at all — log every
  detected drift and every remediation action, even auto-applied ones.
- Treating 100% compliance as the only acceptable state pressures teams to
  disable the scanner on systems that can't realistically comply (a legacy
  system with a documented exception) rather than tracking the exception
  properly — route those through the same exception process as vulnerability
  management risk acceptance.

## Verify
- [ ] Compliance checks run on an automated, short cadence (not quarterly audit
      alone), covering the current baseline's full control set.
- [ ] IaC drift (`terraform plan`-style diffs) is checked outside of deployment
      windows, not only during planned changes.
- [ ] Auto-remediation is applied only to controls explicitly classified as safe
      to auto-revert.
- [ ] Alerting suppresses drift matched to an approved change and highlights
      unauthorised drift distinctly.
- [ ] Every detected drift and remediation action (including automated ones) is logged.

Related: computing-software.cybersecurity-defensive.system-hardening.cis-benchmark-baselines,
computing-software.cybersecurity-defensive.system-hardening.golden-image-pipeline,
computing-software.cybersecurity-defensive.vulnerability-management.exception-and-exposure-tracking
