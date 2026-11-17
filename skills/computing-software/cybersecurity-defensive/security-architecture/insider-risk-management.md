---
id: computing-software.cybersecurity-defensive.security-architecture.insider-risk-management
name: insider-risk-management
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [insider-risk-management, insider-threat, purview-insider-risk, ueba, departing-employee, data-exfiltration-detection, hr-integration]
level: practitioner
status: draft
description: "Run an insider risk programme: governance with HR/legal, risk indicators and policies (departing users, data theft), privacy safeguards, triage and case handling."
sources: ["https://learn.microsoft.com/en-us/purview/insider-risk-management", "https://www.cisa.gov/topics/physical-security/insider-threat-mitigation", "https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Insider risk management

## Governance first
- Charter signed by HR, Legal, Privacy, Security; defines who may see what, works council/union consultation where required, and proportionality.
- Pseudonymise user names in the triage view; reveal only when a case escalates.
- Investigations led by HR/Legal, with security providing evidence.

## Indicators (CERT / Purview style)
| Category | Examples |
|---|---|
| Trigger events | Resignation/termination date (HR connector), poor performance review, PIP |
| Exfiltration | Mass download from SharePoint, copy to USB, upload to personal cloud, emailing to personal address, printing volume |
| Obfuscation | Renaming file extensions, encrypting archives, deleting large volumes |
| Privilege misuse | Accessing records outside role, disabling security tools |

## Purview Insider Risk Management setup
1. Turn on audit and the HR data connector (CSV of resignation/termination dates).
2. Enable indicators (Office, device via Defender for Endpoint onboarding, browser).
3. Create policies from templates: "Data theft by departing users", "Data leaks", "Security policy violations".
4. Tune thresholds after 30 days; use priority user groups for privileged roles.

## Case handling
Alert -> triage (pseudonymised) -> case with timeline -> escalate to HR/Legal -> preserve evidence
(eDiscovery hold) -> outcome recorded. Keep chain of custody if termination or litigation is possible.

## Gotchas
- Monitoring without a legal basis and notice creates more risk than it removes.
- Departing-user windows matter: activity in the 30-90 days before a resignation date is the peak.
- High false positives on power users (data engineers, legal) - use user groups and thresholds.

## Verify
- [ ] HR connector delivering events.
- [ ] Test user copying labelled files to USB generates an alert.
- [ ] Access to de-anonymised data restricted and audited.
