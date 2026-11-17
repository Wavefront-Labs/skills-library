---
id: computing-software.cybersecurity-defensive.nessus.scan-scheduling-and-blackouts
name: scan-scheduling-and-blackouts
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, scan-policy, scan-scheduling, blackout-windows, maintenance-windows, scan-frequency, tenable-sc]
level: practitioner
status: draft
description: "Schedule vulnerability scans: frequency by asset class, scan windows and blackout periods, staggering, and handling scans that overrun their window."
sources: ["https://docs.tenable.com/nessus/Content/ScanSchedule.htm", "https://docs.tenable.com/security-center/Content/BlackoutWindows.htm", "https://www.cisecurity.org/controls/continuous-vulnerability-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scan scheduling and blackout windows

**Goal:** every asset is scanned as often as policy requires, inside windows the business
accepts, and scans never run during freezes.

## Frequency by asset class (typical, align to your VM policy)
- Internet-facing: weekly authenticated + continuous external, CIS Control 7.6 asks for
  at least monthly external scans.
- Servers: weekly authenticated.
- Workstations: agent-based continuous (Nessus Agents) rather than network scans; laptops
  are rarely online during a scheduled window.
- Discovery sweeps: weekly across all ranges.
- Ad hoc: after major changes and for new critical CVEs (targeted scan with specific plugins).

## Schedules
Nessus: scan > Settings > Schedule: frequency (once, daily, weekly, monthly, yearly),
start time, timezone. Set the timezone explicitly per scan; the default follows the
scanner, which surprises global teams.
Tenable Security Center: schedules plus **blackout windows** (Scanning > Blackout Windows)
that block or pause scans for given ranges and times (month-end processing, trading hours).
Nessus Manager/Tenable VM: scan windows on agent groups control when agents scan.

## Staggering
- Split large ranges into multiple scans by site or subnet so each finishes in its window.
- Limit *max scan time* (Advanced > General > max scan run time) or scan window duration;
  on Tenable platforms, choose whether the scan resumes next window or stops.
- Avoid many scans starting at the same minute on one scanner; spread starts.

## Change freezes
Keep a calendar of business freezes and maintenance windows in sync with blackout windows;
notify the NOC/service desk of scan schedules so alerts from scanning are recognised.

## Gotchas
- Scans that overrun into business hours lose goodwill fast; measure duration per scan and
  re-split when it exceeds 80% of the window.
- Paused or stopped scans leave hosts unassessed; report on assessment age per host, not
  only on scan job completion.
- DST changes shift local-time schedules; review twice a year.

## Verify
A report of last-authenticated-scan date per asset (scan coverage) shows no asset older
than its class's required interval.
