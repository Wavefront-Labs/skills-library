---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.golden-and-silver-ticket-detection
name: golden-and-silver-ticket-detection
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [golden-ticket, silver-ticket, kerberos, credential-theft, krbtgt, active-directory, dfir]
level: advanced
status: draft
description: "Detect forged Kerberos golden and silver tickets: TGS without TGT, anomalous ticket lifetimes and fields, nonexistent accounts, PAC validation and memory evidence."
sources: ["https://attack.mitre.org/techniques/T1558/001/", "https://attack.mitre.org/techniques/T1558/002/", "https://adsecurity.org/?p=1515"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Golden and silver ticket detection

**Goal:** determine whether forged Kerberos tickets were used, which implies theft of the
KRBTGT key (golden) or a service account/computer key (silver).

## Golden ticket (forged TGT, T1558.001)
Indicators:
- DC 4769 service ticket requests for an account **with no preceding 4768** TGT issuance
  from that host within ticket lifetime.
- Account names that do not exist, or fake RIDs, or mismatched domain fields
  (Mimikatz default domain field quirks in older versions) in 4624/4769.
- Ticket lifetime anomalies: Mimikatz default 10 years; seen in `klist` on hosts or in
  memory (`kerberos::list`, Volatility/MemProcFS ticket parsing).
- 4769 with `TicketEncryptionType` RC4 when domain uses AES, from privileged accounts.
- Prerequisite evidence: DCSync (4662 with replication GUIDs from non-DC), NTDS.dit theft.
Microsoft Defender for Identity has specific alerts (forged authorisation data, encryption
downgrade, suspected golden ticket usage with nonexistent account or time anomaly).

## Silver ticket (forged TGS, T1558.002)
Forged with a service/computer account key; **no DC traffic** at all, so DC logs show
nothing. On the target: 4624 type 3 Kerberos logons with no corresponding 4769 on any DC;
PAC not validated by default for many services. Enabling PAC validation and auditing
logons helps detection.

## Response
Golden: KRBTGT double reset (see the KRBTGT reset skill) and full tier-0 credential rotation.
Silver: reset the affected computer/service account password (computer accounts: `Reset-ComputerMachinePassword`).

## Gotchas
- Absence of 4768 can also be log gaps (DC logs rolled, multiple DCs not collected); collect
  all DCs before concluding.
- Diamond and sapphire tickets (modified real tickets) evade the "no TGT" heuristic.

## Verify
Correlate every suspect 4769/4624 against all DCs' 4768 events for the window; confirm
forged-ticket conclusions with memory or MDI evidence where available.
