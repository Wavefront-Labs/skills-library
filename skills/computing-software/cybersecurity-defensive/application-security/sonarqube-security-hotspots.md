---
id: computing-software.cybersecurity-defensive.application-security.sonarqube-security-hotspots
name: sonarqube-security-hotspots
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [sonarqube, security-hotspots, sast, quality-gate, sonarcloud, code-review]
level: practitioner
status: docs-checked
description: "Review SonarQube security hotspots (To review, Acknowledged, Fixed, Safe), tell them from vulnerabilities, and note that hotspots are being phased out in 2026.5."
sources: ["https://docs.sonarsource.com/sonarqube-server/latest/user-guide/security-hotspots/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SonarQube security hotspots

## Hotspots versus vulnerabilities
A Security Hotspot highlights security-sensitive code a developer must review to decide if a fix is needed;
overall application security may not be affected. A Security Vulnerability (Standard Experience) or Security
issue (MQR Mode) is a problem that impacts security and needs fixing immediately. SonarQube's example is
RSPEC-2092, the cookie `secure` flag: HTTPS is the main protection, and a tracking cookie may be designed to
be sent everywhere.

## Phase-out (important)
The Managing Security Hotspots page for SonarQube Server 2026.5 says hotspots are being phased out: rules that
raised hotspots now raise vulnerabilities (Standard Experience) or security issues (MQR Mode), and existing
hotspot findings must be converted (see "Migrating security hotspots to vulnerabilities"). Check your
server version before building process around hotspots.

## Lifecycle statuses
- **To review**: default for new hotspots.
- **Acknowledged**: reviewed, resolution pending (fix in progress or time needed to decide).
- **Fixed**: reviewed and a fix applied.
- **Safe**: reviewed, no change needed (for example other protections are in place).
Statuses can be changed, commented on and assigned. The Activity tab keeps the history.

## Review workflow
Hotspots are listed by review priority, high to low. Priority comes from the rule's security category: high
for categories ranked high in OWASP Top 10 and CWE Top 25, otherwise Medium or Low. For each hotspot:
read the "What's the risk?" tab, use "Assess the risk" (Ask Yourself Whether), follow "How can I fix it?" if
unsafe, then set Acknowledged, Fixed or Safe (or leave To review for another reviewer). The "Open in IDE"
button opens it in a connected IDE (SonarQube for IntelliJ 4.13+, Visual Studio 4.29+, VS Code 1.20+,
Eclipse 5.7+).

## Gotchas
- Teams mark everything Safe to pass a gate: spot-check Safe statuses and require a comment with the reason.

## Checked
2026-11-01. Confirmed against the SonarQube Server "Managing Security Hotspots" page. Removed: quality gate
conditions and the "100% reviewed" default, scanner commands and properties, edition feature matrix, PR
decoration, exclusions and token advice, and the test case; those pages were not read in detail.
Method: documentation only; no commands were run.
