---
id: computing-software.digital-forensics-incident-response.log-analysis.sentinelone-deep-visibility-investigation
name: sentinelone-deep-visibility-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sentinelone-deep-visibility, sentinelone, edr, s1ql, storyline, dfir]
level: practitioner
status: draft
description: "Investigate with SentinelOne Deep Visibility / Event Search: Storyline IDs, S1QL and PowerQuery syntax, process, network and file event fields, threat pages and remote shell collection."
sources: ["https://www.sentinelone.com/blog/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SentinelOne Deep Visibility investigation

Review note: the field names, `contains:anycase` modifier and legacy field names below are from practitioner knowledge; no official S1QL reference could be fetched, and the listed sources are marketing/community pages. Validate each query in your console's autocomplete before relying on it.

Deep Visibility (now Event Search on Singularity Data Lake in newer consoles) holds SentinelOne endpoint telemetry. Its distinctive concept is the **Storyline**: an ID that ties together all processes and events descended from one root process, so one query returns an attack chain.

## Starting from a threat
The threat page shows the detection engine, file details and hash, the Storyline visualisation (process tree with events), mitigation status, and analyst verdicts. Copy the Storyline ID (`src.process.storyline.id` / legacy `SrcProcStorylineId`) and pivot into Event Search to see all related events.

## Query languages
**S1QL 2.0** (field.dot.notation, used in current Event Search):
```text
event.type = "Process Creation" AND src.process.name contains:anycase "powershell" AND src.process.cmdline contains:anycase "-enc"
src.process.storyline.id = "ABCDEF0123456789"
event.dns.request contains:anycase "bad-update.example"
dst.ip.address = "203.0.113.50"
```
**PowerQuery** adds pipes for aggregation:
```text
event.type = "Process Creation" src.process.name = "rundll32.exe"
| group count = count() by endpoint.name, src.process.cmdline
| sort -count
```
**Legacy S1QL 1.0** used CamelCase fields (`EventType = "Process Creation" AND SrcProcName ContainsCIS "powershell"`); older saved hunts and many community queries use it. Check which your console accepts.

## Useful fields (2.0 naming)
`endpoint.name`, `src.process.name/cmdline/image.path/image.sha256/user`, `src.process.parent.name`, `tgt.process.*` (for cross-process events), `tgt.file.path`, `event.network.direction`, `dst.ip.address`, `dst.port.number`, `event.dns.request`, `event.login.type`, `indicator.name` (behavioural indicators).

## Collection and response
- **Remote Shell** (permission-gated, requires 2FA in console) for live commands; **Fetch Files** to retrieve files (password-protected zip); **Remote Script Orchestration** for scripted collection (e.g. KAPE, memory capture) across many endpoints.
- Mitigation actions: kill, quarantine, remediate (reverse changes tracked in the Storyline), rollback (VSS-based, Windows), network quarantine.

## Gotchas
- Retention depends on licence (often 14 to 365 days); export Storyline events for long cases.
- Event types are sampled or deduplicated for some high-volume categories; absence is not proof.
- "Remediate" and "rollback" change the endpoint: collect evidence first.

## Verify
Each finding cites endpoint, event type, timestamp, Storyline ID and query used, and fetched files have recorded hashes.
