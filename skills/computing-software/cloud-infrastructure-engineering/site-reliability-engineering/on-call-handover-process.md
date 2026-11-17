---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.on-call-handover-process
name: on-call-handover-process
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [handover-process, handover-checklist, on-call, shift-handoff, follow-the-sun]
level: practitioner
status: docs-checked
description: "Run a clean on-call shift handover: written handover note template, open incidents and their owners, ongoing risks, explicit acknowledgement and paging-tool override checks."
sources: ["https://sre.google/workbook/on-call/", "https://sre.google/sre-book/managing-incidents/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# On-call handover process and checklist

Every rotation boundary is a chance to drop context. The Workbook's example team guidelines have the on-call read the previous shift's handoff at the start of a shift and email a handoff to the next on-call at the end; for incidents in flight the SRE Book requires an explicit handoff of the incident commander
role ("you're now the incident commander, okay?") with acknowledgement.

## Handover note template
```
On-call handover  <service/team>  <from> -> <to>  <date time UTC>
Open incidents:   INC-512 (sev2, mitigated, IC=<name>, next step: verify backfill at 09:00 UTC)
Pages this shift: 4 (2 actionable). Noisy alert: DiskFillingFast on node pool b (ticket T-881)
Ongoing risks:    region eu-west capacity at 62%; CDN vendor maintenance 02:00-04:00 UTC
Changes in flight: release 2026.10.3 at 50% canary, owner <name>; DB migration step 2 Thursday
Silences active:  alertname=CertExpiry env=staging, expires 18:00 UTC (why: renewal in progress)
Follow-ups:       update runbook for Kafka lag alert (T-884)
```
Post it in the team channel and the handover log (searchable history).

## Checklist
- [ ] Paging tool shows the incoming person as on-call (check overrides and time zones).
- [ ] Incoming tests a page to their device (your paging tool's test notification).
- [ ] Open incidents have a named owner after handover; IC role transferred explicitly.
- [ ] Active silences reviewed: still needed? expiry set?
- [ ] Laptop, VPN, credentials, hardware tokens working for the incoming person.
- [ ] Incoming acknowledges in writing ("ack, I have it").

## Live handover call
Keep it short. Use for busy shifts or open sev1/sev2 incidents. Walk the note, show dashboards, answer questions. Quiet
shifts can do written-only.

## Gotchas
- Follow-the-sun handovers across languages and time zones need the written note more, not less.
- Overrides set in the paging tool silently expire; double-check the next 24 h schedule.
- Leaving incidents "with the team" means no one; every open item needs a name.

## Verify
- [ ] Handover log entry exists for each shift change.
- [ ] No pages went unacknowledged at boundaries (paging tool report).

## Checked
2026-11-01. Confirmed in SRE Workbook On-Call (example guidelines: read the previous handoff at shift start, send a handoff email at shift end) and SRE Book Managing Incidents (explicit incident-commander handoff phrase, handoffs tracked by the planning role). Removed the `pd trigger` command and the call length, which the sources do not give. The template values are examples.
Method: documentation only; no commands were run.
