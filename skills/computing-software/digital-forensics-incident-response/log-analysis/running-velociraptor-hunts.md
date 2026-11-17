---
id: computing-software.digital-forensics-incident-response.log-analysis.running-velociraptor-hunts
name: running-velociraptor-hunts
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [velociraptor-hunts, velociraptor, threat-hunting, fleet-collection, ioc-sweep, dfir]
level: practitioner
status: docs-checked
description: "Run Velociraptor hunts across the fleet: label targeting, expiry, testing on a few endpoints first, and analysing combined results in the hunt notebook."
sources: ["https://docs.velociraptor.app/docs/hunting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Velociraptor hunts

**Goal:** sweep every endpoint for an indicator or collect triage data at scale, safely and
with traceable results.

## Create a hunt
GUI: open the Hunt Manager from the sidebar, then New Hunt (the New Hunt Wizard).
- Enter a description and an expiration date. Default expiry is one week; clients that appear after expiry do not receive the hunt, and each client receives it once.
- Target by label: include a Label Group, or exclude machines with a label.
- Choose the artifact(s) and parameters from the artifact list in the wizard; check each artifact's page in the artifact reference for its parameters.
- New hunts start Paused. Test the artifact on one or two endpoints first, then click Start.

## Monitor
Offline endpoints that come back online during the hunt period are collected. Check errored clients individually.

## Analyse
- Each hunt gets a Notebook for VQL over the results, e.g.
  `SELECT * FROM hunt_results(hunt_id="H.123", artifact="Windows.System.Pslist")`.
- Stack counts by value to spot rare entries; keep exports with the case record.

## Gotchas
- Broad file searches with hashing on file servers can run for hours; scope paths and sizes. Look up the artifact's resource-limit settings before launching.
- Results only cover clients that ran it; report coverage (completed / total enrolled).

## Verify
Coverage number recorded with the results, a positive-control host (planted indicator) shows a hit, and errored clients are listed for follow-up.

## Checked
2026-11-01. Confirmed on docs.velociraptor.app hunting page: Hunt Manager, New Hunt wizard, description and expiry (default one week), label include/exclude, Paused start and test-on-one-or-two advice, offline clients, per-hunt notebook, `hunt_results` example. Removed: specific artifact names (artifact reference index lists none), resource-limit fields, OS condition, pilot label, zip download, other VQL columns; the page does not state them.
Method: documentation only; no commands were run.
