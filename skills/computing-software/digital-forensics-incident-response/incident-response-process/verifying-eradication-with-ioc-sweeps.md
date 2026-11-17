---
id: computing-software.digital-forensics-incident-response.incident-response-process.verifying-eradication-with-ioc-sweeps
name: verifying-eradication-with-ioc-sweeps
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [eradication-verification, eradication, ioc-sweep, velociraptor, yara, dfir]
level: advanced
status: draft
description: "Verify eradication across the estate: final IOC and YARA sweeps, persistence re-baselining, credential-use monitoring and exit criteria before recovery."
sources: ["https://docs.velociraptor.app/docs/hunting/", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://yara.readthedocs.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verifying eradication with IOC sweeps

**Goal:** prove, before declaring eradication complete, that no attacker artefact or access
remains anywhere - not just on the hosts you already knew about.

## Sweep package
Build from the incident's own findings plus intel on the actor:
- File hashes, names and paths of all malware/tools found.
- YARA rules for families (catches recompiled variants).
- Persistence: services, tasks, run keys, WMI subscriptions, IFEO, startup items by name/command line.
- Network: C2 domains/IPs (DNS cache, connections, proxy logs).
- Identity: attacker account names, OAuth app IDs, access key IDs.

## Run across all hosts, not just the known set
```text
Velociraptor hunts (examples):
  Windows.Detection.Yara.Process / Generic.Detection.Yara.Glob  (custom rule)
  Windows.Persistence.PermanentWMIEvents, Windows.System.TaskScheduler, Windows.System.Services
  Windows.Search.FileFinder (hash / path glob)
```
- Track coverage: hosts targeted vs responded; chase offline hosts until 100% or documented.
- Repeat the sweep after a delay (e.g. 72 h) to catch hosts that were off.

## Exit criteria (write them down)
- Zero hits on the sweep package, or every hit explained and remediated.
- No C2 traffic in proxy/DNS/firewall logs for N days after blocks.
- No use of revoked credentials, or each attempt attributed and blocked.
- Persistence baseline on servers matches known-good.
- IC and system owners sign off in the decision log.

## Gotchas
- Sweeping only for the exact hash the first sample had; actors recompile per victim.
- Treating EDR "remediated" status as proof; verify the artefact is gone.
- Restored backups can reintroduce persistence; sweep restored systems too.

## Verify
Coverage table plus clean results attached to the eradication sign-off.
