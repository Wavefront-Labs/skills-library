---
id: computing-software.digital-forensics-incident-response.evidence-handling.ios-sysdiagnose-collection-and-analysis
name: ios-sysdiagnose-collection-and-analysis
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [sysdiagnose, ios-forensics, mobile-forensics, unified-logs, dfir]
level: advanced
status: docs-checked
description: "Analyse iOS sysdiagnose archives with the EC-DIGIT-CSIRC Sysdiagnose Analysis Framework: case creation, parsers, analysers, unified logs on Linux, Timesketch and YARA."
sources: ["https://developer.apple.com/bug-reporting/profiles-and-logs/", "https://github.com/EC-DIGIT-CSIRC/sysdiagnose", "https://docs.mvt.re/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iOS sysdiagnose collection and analysis

**Goal:** turn an Apple sysdiagnose archive into structured, timeline-ready data with the
Sysdiagnose Analysis Framework (SAF). Apple lists sysdiagnose instructions per OS on its Profiles
and Logs page; follow the page for your iOS version to generate the archive (the cached copy of
that page is an index of links, so the trigger steps are not restated here).

## Install SAF
Needs Python 3.11 or higher. Create a venv, `pip install .`, and install graphviz (`sudo apt
install graphviz`, or on macOS `brew install graphviz libmagic`). README lists tested iOS
versions 15 to 18 and 26 (13 and 14 "to be confirmed").

## Workflow
1. Create a case: `saf create <sysdiagnose>.tar.gz` prints a Case ID. `saf cases` lists them
   with acquisition date, serial number, unique device ID and iOS version. Cases live in the
   current folder unless `SYSDIAGNOSE_CASES_PATH` is set.
2. Parse: `saf -c 1 parse ps` writes `cases/1/parsed_data/ps.json`; omit the case or use `-c all`
   for every case; `saf list parsers` shows them. Examples: `ps`, `psthread`, `shutdownlogs`,
   `logarchive`, `mobileinstallation`, `appinstallation`, `crashlogs`, `wifinetworks`,
   `wifi_known_networks`, `powerlogs`, `lockdownd`, `networkextension`, `taskinfo`, `uuid2path`,
   `security_sysdiagnose`.
3. Analyse (run `parse all` first): `saf -c 1 analyse timesketch`. Analysers: `apps`,
   `ps_everywhere`, `ps_matrix` (compares ps, psthread, taskinfo), `timesketch`,
   `wifi_geolocation` (GPX), `wifi_geolocation_kml`, `yarascan`.
4. Output sits in `<cases>/<case_id>/parsed_data` as JSON or JSONL; JSONL events carry a unixtime
   timestamp and an ISO datetime.

## Timesketch and YARA
- Timesketch expects microsecond timestamps, hence the `timesketch` analyser. The README suggests
  Ubuntu 20.04+, 128 GB RAM, 4-8 vCPUs, at least 64 GB disk for Timesketch data, and SSDs.
- `yarascan` reads `.yar` rules from `./yara` or `SYSDIAGNOSE_YARA_RULES_PATH`.

## Unified logs
On macOS SAF uses Apple's own log tool. On Linux it expects the Mandiant `unifiedlog_iterator`
(built from mandiant/macos-UnifiedLogs with cargo, then copied into the path).

## Troubleshooting
Each parse or analyse run writes a JSONL log in the case's `logs` folder; add `-l DEBUG` to see it
on screen.

## Related
MVT (Mobile Verification Toolkit) from Amnesty International Security Lab does consensual forensic
analysis of Android and iOS devices to find traces of compromise; its docs cover `mvt-ios`.

## Verify
Case created, `parse all` finishes without errors, and the case logs show each parser finishing.

## Checked

Date 2026-11-08. Pages read: Apple Profiles and Logs (index of links only), EC-DIGIT-CSIRC sysdiagnose README, MVT docs home. Removed as not on the pages: the button combination and timing, retrieval steps and idevicecrashreport, the contents table of archive files, the example `log show` command, the claim that generation alters the device, log retention advice, and the shutdown.log spyware statement. The skill no longer teaches collection, only SAF analysis.

Method: docs-only read of cited pages, 2026-11-08
