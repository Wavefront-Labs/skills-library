---
id: computing-software.cybersecurity-defensive.endpoint-security.cloud-delivered-protection-and-block-at-first-sight
name: cloud-delivered-protection-and-block-at-first-sight
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [antimalware, cloud-delivered-protection, block-at-first-sight, maps, cloud-block-level, sample-submission, zero-day-malware]
level: practitioner
status: docs-checked
description: "Enable and tune cloud-delivered protection and Block at First Sight so new malware is blocked within seconds, with correct sample submission and network requirements."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/configure-block-at-first-sight-microsoft-defender-antivirus", "https://learn.microsoft.com/en-us/defender-endpoint/configure-cloud-block-timeout-period-microsoft-defender-antivirus", "https://learn.microsoft.com/en-us/powershell/module/defender/set-mppreference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud-delivered protection and Block at First Sight

**Goal:** never-before-seen malware is analysed in the cloud and blocked on first execution,
instead of waiting hours for signatures.

## How it works
When a file is suspicious and unknown, the client holds it and queries the cloud service (MAPS)
with metadata; the cloud uses ML, detonation and global telemetry to return a verdict, often
within seconds. **Block at First Sight (BAFS)** extends this for new executables downloaded
from the internet: the file is locked until the cloud verdict arrives.

## Requirements for BAFS
- Cloud-delivered protection on (`MAPSReporting` Advanced).
- Sample submission: `SubmitSamplesConsent` = Send safe samples (1) or all samples (3).
- Real-time protection on.
- Network access to the Defender cloud endpoints.

## Tuning
- **Cloud protection level**: set with `-CloudBlockLevel`; higher levels block more aggressively and raise false-positive risk. Choose from the levels listed on the Microsoft cloud protection level page.
- **Extended cloud check timeout**: `-CloudExtendedTimeout` takes 0 to 50 and adds that many seconds to the default 10-second period, so the cloud has time for deeper analysis.

## Privacy
Choose between `SendSafeSamples` and `SendAllSamples` for `SubmitSamplesConsent` to match your data policy.

## Gotchas
- Proxy and TLS inspection breaking MAPS connections silently disables cloud protection; validate on each network.
- Air-gapped networks get no cloud protection: compensate with frequent signature updates and application control.
- Users report "delays" when opening new downloads: that is BAFS working; explain rather than disable.

## Checked
2026-10-28. Confirmed in the block at first sight, cloud block timeout and Set-MpPreference pages: `MAPSReporting Advanced`, `SubmitSamplesConsent` values, `-CloudBlockLevel`, `-CloudExtendedTimeout` (0-50, added to a 10-second default). Removed: the named cloud protection level list, the `MpCmdRun.exe -ValidateMapsConnection` command, the downloaded-files scan setting name and the sample privacy description.
Method: documentation only; no commands were run.

## Verify
- [ ] Cloud protection connectivity verified on sample devices in each network zone.
- [ ] Microsoft's BAFS test file (from the Defender demo site) is blocked.
