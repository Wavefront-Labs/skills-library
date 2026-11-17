---
id: computing-software.digital-forensics-incident-response.log-analysis.edr-live-response-and-remediation-actions
name: edr-live-response-and-remediation-actions
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [edr-live-response, live-response, defender-for-endpoint, remediation, evidence-collection, dfir]
level: practitioner
status: docs-checked
description: "Use Defender for Endpoint live response and response actions to collect evidence and remediate: commands, library scripts, limits and the command log."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/live-response", "https://learn.microsoft.com/en-us/defender-endpoint/respond-machine-alerts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EDR live response and remediation actions (Defender for Endpoint)

**Goal:** collect evidence and contain or remove threats remotely through the EDR, keeping a record of every action.

This skill covers Microsoft Defender for Endpoint only (live response applies to Plan 2). Other EDR products need their own documentation.

## Prerequisites
- Live response must be enabled under Advanced features (admins or users with "Manage Portal Settings"). Unsigned PowerShell script execution is a separate optional setting; the page warns it increases exposure, and signature checks apply only to PowerShell.
- Basic and advanced command sets are controlled by RBAC roles. Uploading a file to the library from a session needs "Manage Security Settings" permission; the Library management page does not.
- Check the device OS and agent version against the supported list on the page. Live response can be restricted on high-value assets by their selective response actions.

## Commands useful for evidence
- Basic: `processes`, `connections` (Windows), `services`, `scheduledtasks`, `persistence`, `startupfolders`, `registry`, `drivers` (Windows), `fileinfo`, `findfile`, `getfile <path>`, `jobs`, `status`.
- Advanced: `collect` (forensics package; macOS and Linux), `run` (a script from the library), `putfile`, `library`, `analyze` (Windows), `remediate`, `undo` (Windows), `scan` (macOS, Linux), `isolate` and `release` (macOS).
- `remediate` acts by entity: file delete; process stop and delete image; service stop and delete image; registry entry delete; scheduled task remove; startup item delete. It has a prerequisite command; `-auto` runs it.
- Output can be `-output json` (more fields) or table, and can be redirected to a file with `>`.
- `getfile <path> &` downloads in the background; `fg <command ID>` brings it forward.

## Device response actions (device page)
- Collect investigation package: captures current device state; the contents table is on the page and a `CollectionSummaryReport.xls` lists data points, commands, status and errors. Collection can fail on low battery or metered connections.
- Isolate device: blocks network access to limit attacker control, exfiltration and lateral movement while keeping the Defender service connection. Full and selective isolation exist; with web proxies (PAC, WPAD, static) devices may fail to recover from full isolation, so use selective isolation.
- Run antivirus scan, restrict app execution (Windows), stop and quarantine a file. Actions are tracked in the Action center.

## Order of work
1. Decide on isolation, weighing containment against tipping off the attacker.
2. Collect volatile data first (processes with `processes`, `connections`, services, tasks, persistence), then files with `getfile` or a package.
3. Only then remediate; stopping a process before collecting loses its evidence unless damage is ongoing.
4. Verify afterwards and keep the session records.

## Limits and traps
- 50 sessions at once; 5 concurrent sessions per user; one session per device; 30-minute inactivity timeout.
- Commands time out at 10 minutes, except `getfile`, `findfile` and `run` at 30 minutes.
- Size limits: `getfile` 3 GB, `fileinfo` 30 GB, library 250 MB (5 MB default in US Government cloud), `putfile` 300 MB on Windows and 10 MB elsewhere. Large transfers on slow links may time out; split files.
- Ctrl+C cancels a command only in the portal; changing operations such as `remediate` may continue on the device.
- `putfile` files go to a working folder and are deleted at restart by default.
- Live response actions started from the Device page are not available in the MachineActions API.
- Command log: each command is tracked with ID, command line, duration, status and input/output. Session dashboard shows who created the session, when it started and its duration. Reference these in case notes.

## Verify
For each host you can show what was collected (with hashes you computed), what was changed, by whom and when, from the command log and Action center.

## Checked
Confirmed against the live response page (prerequisites, command tables, library, remediate entity actions, limits, command log, output options) and the respond-to-machine-alerts page (investigation package, isolation, antivirus scan, restrict app execution, Action center). Removed unconfirmed content: CrowdStrike Falcon RTR and SentinelOne comparisons (the cited CrowdStrike product page was marketing and not relied on), memory-imaging tool names, KAPE and Velociraptor steps, hash-handling claims, and the generic eviction advice.

Method: docs-only read of cited pages, 2026-11-09
