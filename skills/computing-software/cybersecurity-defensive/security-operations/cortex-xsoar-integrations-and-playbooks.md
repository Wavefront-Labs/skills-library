---
id: computing-software.cybersecurity-defensive.security-operations.cortex-xsoar-integrations-and-playbooks
name: cortex-xsoar-integrations-and-playbooks
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [cortex-xsoar, soar-automation, playbooks, integrations, incident-mapping, content-packs, palo-alto]
level: practitioner
status: draft
description: "Build Cortex XSOAR integrations and playbooks: integration instances, incident types and mappers, playbook tasks and sub-playbooks, war room, and content packs."
sources: ["https://docs-cortex.paloaltonetworks.com/r/Cortex-XSOAR/8/Cortex-XSOAR-Administrator-Guide", "https://xsoar.pan.dev/docs/integrations/integrations-and-incidents-fetch", "https://xsoar.pan.dev/docs/playbooks/playbooks-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cortex XSOAR integrations and playbooks

## Integrations
- Install content packs from Marketplace (e.g. Microsoft Defender, CrowdStrike, ServiceNow).
- Configure an **instance** per integration (credentials, fetch incidents option, classifier and
  mapper, incident type). Use engines for on-prem reachability.
- **Fetch incidents**: integration pulls alerts on interval; **classifier** picks incident type,
  **mapper** maps raw fields to incident fields.

## Incident types and layouts
Define per use case (Phishing, Malware, Impossible Travel) with custom fields, layout, default
playbook, SLA timers.

## Playbooks
- Visual editor; task types: standard (run command), conditional, data collection (ask user),
  manual tasks, sub-playbooks, loops.
- Inputs/outputs via context (`${incident.field}`, `${File.SHA256}`); `!command arg=value` in war room
  for ad hoc actions.
- Use generic sub-playbooks for enrichment ("Entity Enrichment - Generic v3") and response
  ("Block Indicators - Generic v3") instead of re-implementing.
- Error handling: per-task "on error" paths; quiet mode for noisy tasks.

## Scripts and automation
Python scripts (Docker images) for transformations; register as automations used by tasks.

## War room
Per incident chat and command log; every analyst and playbook action recorded (audit trail).

## Dev lifecycle
- Develop in a dev tenant; use `demisto-sdk` to `download`, `validate`, `lint`, `format`, `upload`
  content; keep custom content in git; XSOAR 8 supports remote repositories for content promotion.

## Gotchas
- Modifying out-of-the-box playbooks blocks updates; copy and detach, or wrap with your own.
- Context bloat from large outputs slows incidents; set `extend-context` carefully.
- Fetch interval too short hits API limits.

## Verify
A test alert fetches, classifies to the correct type, runs the playbook to completion in a dev
tenant, and `demisto-sdk validate` passes on the custom pack.
