---
id: computing-software.digital-forensics-incident-response.incident-response-process.responding-to-external-notification-of-compromise
name: responding-to-external-notification-of-compromise
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [external-notification, incident-triage, incident-declaration, law-enforcement-engagement, dfir]
level: practitioner
status: draft
description: "Handle a third-party, researcher or law-enforcement notice that you are compromised: verify, preserve, scope from their indicators, and respond safely."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/report", "https://www.ic3.gov/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responding to external notification of compromise

**Goal:** many intrusions are first detected by someone else - FBI/CISA, a partner, a security
researcher, a customer seeing fraud, or a dark-web listing. Turn the tip into a scoped case
without tipping off the attacker or falling for a scam.

## 1. Verify the notifier
- Call back law enforcement via a number from the agency's public website, not the one in the
  email. Treat "pay us to tell you" researchers as possible extortion.
- Record exact wording, indicators supplied, time received, contact details.

## 2. Ask for actionable detail
- IPs/domains with timestamps (and time zone), victim-side IPs or hostnames, accounts, file
  names or data samples, how they observed it (sinkhole, seized server, leak site).
- Agree what can be shared back and under what TLP.

## 3. Preserve before you look
- Extend log retention immediately (firewall, proxy, DNS, VPN, cloud audit) for the window given.
- Snapshot / image the named hosts before anyone logs in interactively.

## 4. Scope from their indicators
- Search proxy/DNS/firewall/EDR for the indicators over the full retention window, not just the
  date given; attackers usually arrived earlier.
- Pivot from the matched internal host to its accounts, then those accounts' other logons.
- For data-sample notices, identify the source system from schema, file paths or record IDs.

## 5. Decide and declare
- If indicators match: declare per the severity matrix (external notification of data exposure
  is often an automatic Sev-1). If no match: document the searches and data gaps and keep the case open.

## Gotchas
- Blocking the supplied IPs immediately can alert the attacker and destroy monitoring
  opportunities; decide containment deliberately.
- Notifications reference NAT'd public IPs; map them through firewall NAT logs to the internal host.
- Legal should be informed at once; the notice itself may start a regulatory clock.

## Verify
The case shows notifier verification, preserved data, the searches run, and a recorded declaration decision.
