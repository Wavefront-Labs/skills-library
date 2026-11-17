---
id: computing-software.digital-forensics-incident-response.incident-response-process.pre-deploying-ir-agents-and-collection-access
name: pre-deploying-ir-agents-and-collection-access
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [agent-predeployment, ir-preparation, incident-readiness, velociraptor, edr, dfir]
level: advanced
status: draft
description: "Pre-deploy EDR, Velociraptor and collection access before an incident: coverage targets, credentials, firewall rules, offline collectors and tests."
sources: ["https://docs.velociraptor.app/docs/deployment/", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://ericzimmerman.github.io/KapeDocs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pre-deploying IR agents and collection access

**Goal:** when the call comes, responders can query and collect from every host within minutes,
instead of spending the first two days negotiating software installs and firewall changes.

## Coverage targets
- EDR on 100% of Windows, macOS and Linux servers and endpoints, including domain controllers,
  hypervisor management hosts, jump boxes and build servers. Track coverage gaps weekly from the
  CMDB vs EDR console diff.
- A DFIR agent (Velociraptor, or the EDR's live-response feature) for artefact collection at scale.

## Velociraptor readiness
- Server built (cloud VM or on-prem), TLS cert, SSO or local users, MSI/deb/pkg clients signed
  and stored in the software deployment tool, not yet necessarily installed everywhere.
- Pre-approved change: "deploy DFIR agent to all hosts during a declared incident".
- Test quarterly: deploy to a pilot group, run `Generic.Client.Info` and `Windows.KapeFiles.Targets`
  on one host, confirm upload.
- Build offline collectors (`velociraptor gui` > Server Artifacts > Build Offline Collector) for
  air-gapped or agentless hosts and keep them in the jump kit.

## Access and plumbing
- Firewall rules allowing agents to reach the server on 443/8000 (or the chosen port) from all segments.
- Break-glass admin accounts for EDR and Velociraptor stored in a vault outside SSO.
- A collection bucket (S3/Azure blob) with write-only SAS/keys for KAPE `--s3`/`--asu` uploads.
- Cloud: pre-created forensic IAM role/account for snapshot sharing and log access.

## Gotchas
- EDR in "detect only" with live response disabled by policy; enable RTR / Live Response for IR roles in advance.
- Agents blocked by application control (WDAC/AppLocker) or tamper protection on golden images.
- Collector binaries flagged by AV; pre-agree exclusions with the endpoint team.

## Verify
A timed drill: from declaration to first artefact collection on a random server is under 30 minutes.
