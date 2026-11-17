---
id: computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology
name: threat-hunting-methodology
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, soc, hypothesis-driven-hunting, mitre-attack, pivoting, hunt-team, proactive-detection, tactical-hunting, baseline, prevalence-analysis, structured-analytic-techniques, siem, edr, detection-engineering]
level: advanced
status: draft
description: "Run a hypothesis-driven threat hunt: scope it, pick data sources by ATT&CK technique, pivot methodically, and turn every finding into a detection or a documented gap."
sources: ["MITRE ATT&CK Enterprise matrix", "SANS FOR508/Threat Hunting and IR courses (public course outlines)", "The Pyramid of Pain (David Bianco)", "Sqrrl / David Bianco - A Simple Hunting Maturity Model"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat hunting methodology — hypothesis, not a fishing expedition

**Goal:** run a time-boxed hunt that either finds something real, strengthens a
detection, or proves a hypothesis false with evidence — never "we looked around and
saw nothing," which is unfalsifiable and wastes the next hunter's time.

## 1. Pick a hypothesis, not a tool
Bad hunt: "look for weird PowerShell." Good hunt: "if an adversary is doing
credential dumping (T1003) on domain controllers, LSASS will be opened by a process
other than the known AV/EDR agent, and we have Sysmon Event ID 10 coverage on all 6
DCs to detect it." A hypothesis names the technique, the expected artefact, and
confirms the data exists before you start. Sources for hypotheses: ATT&CK gaps in
your detection coverage matrix, recent intel (a new CVE exploited in the wild,
an ISAC bulletin), and prior incident post-mortems ("we were only lucky to catch that
by accident — would a hunt have caught it?").

## 2. Scope and time-box
Write: asset scope (which hosts/segments), time window, data sources, and a hard
stop (half a day to two days for a tactical hunt). Open-ended hunts die from scope
creep. Log the hunt like a mini-project: hypothesis, scope, start/end, findings,
outcome — future hunters reuse this record instead of re-deriving it.

## 3. Baseline before you hunt for the rare
Most hunts are really "what's rare in a population." Pull the population first
(e.g. all parent→child process pairs across the fleet for 30 days), then look for
outliers (`stats count by ...` sorted ascending) rather than eyeballing one host.
A process seen on 1 of 4,000 endpoints, signed by nobody, run from a temp path, is
interesting regardless of hash reputation — prevalence beats reputation, because
reputation lags novel tooling.

## 4. Pivot methodically (don't follow every rabbit hole)
Standard pivot chain once something looks odd: process → parent process → command
line → network connections from that process → the user who ran it → other hosts
where that user has logged on recently → other hosts running the same
process/hash/path. Note each pivot and its result even when it's a dead end — a
documented dead end prevents the next hunter re-walking it. Use structured analytic
techniques (e.g. analysis of competing hypotheses) when the picture is ambiguous:
force yourself to list what evidence would exist if the benign explanation were true,
and check for it, before escalating.

## 5. Convert the result
- **Confirmed malicious:** hand off to IR/triage immediately — a hunt is not an
  investigation, don't quietly keep digging past the point of confirmation.
- **Benign but previously unseen pattern:** add to the allowlist/baseline with an
  owner, so it stops looking anomalous.
- **Hypothesis true but tooling too weak to detect reliably in general:** the real
  deliverable is a new or tuned detection (link the SIEM saved search/correlation rule
  you wrote), not just the one-off finding — this is what separates hunting from
  one-time investigation.
- **Hypothesis false, with good evidence:** still a win — write it up; it retires a
  gap from the coverage matrix and stops the same hunt being re-run blind next quarter.

## Gotchas
- Hunting on unlogged or short-retention data gives false confidence — check log
  coverage and retention for the scope *before* writing the hypothesis, not after a
  null result.
- Survivorship bias: hunting only where EDR is deployed finds nothing where EDR isn't
  deployed, which is often where an adversary already is.
- A hunt that keeps "following interesting things" past its time box becomes an
  unbounded investigation with no decision point — re-scope or hand off instead.
- Treat your own hunt tooling (custom scripts, notebooks) as code: version it, or the
  next hunter can't repeat or audit what you did.

## Verify
- [ ] Hypothesis names a specific technique, actor behaviour, or weak spot, and the
      expected artefact.
- [ ] Data source coverage and retention were confirmed before the hunt started.
- [ ] A baseline/population query ran before anomaly hunting began.
- [ ] Every pivot and its outcome (including dead ends) is recorded.
- [ ] The hunt ended in one of: incident handoff, allowlist update, new/tuned
      detection, or a documented disproven hypothesis — not a shrug.

Related: computing-software.cybersecurity-defensive.security-operations.alert-triage,
computing-software.cybersecurity-defensive.splunk.spl-detection-searches,
computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling
