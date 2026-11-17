---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-processaccess-event-10
name: sysmon-processaccess-event-10
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-process-access, sysmon, lsass-dumping, credential-theft, dfir]
level: advanced
status: docs-checked
description: "Use Sysmon Event ID 10 (ProcessAccess) to detect credential-stealing reads of LSASS: what the event records, filter rules and volume control."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon ProcessAccess (Event ID 10)

**Goal:** Event 10 reports when a process opens another process, an operation often followed by
information queries or reading and writing the target's address space. Per the Sysmon
documentation this enables detection of hacking tools that read the memory of processes such as
LSASS (Lsass.exe) to steal credentials for use in Pass-the-Hash attacks.

## Volume warning
The documentation warns that enabling it can generate significant logging when diagnostic
utilities repeatedly open processes to query their state, so it should generally be enabled
only with filters that remove expected accesses.

## Config
Filter tag is `ProcessAccess`. Include only the target you will review, then exclude known
good sources:
```xml
<RuleGroup name="" groupRelation="or">
  <ProcessAccess onmatch="include">
    <TargetImage condition="image">lsass.exe</TargetImage>
  </ProcessAccess>
  <ProcessAccess onmatch="exclude">
    <SourceImage condition="end with">\example-agent.exe</SourceImage>
  </ProcessAccess>
</RuleGroup>
```
- The `image` condition matches a full path or only the image name (a bare image name
  such as lsass.exe matches the full path to that image).
- Exclude matches take precedence over includes. Rules on the same field are ORed, on
  different fields ANDed; conditions are case insensitive.
- Run `sysmon -s` to print the schema with the exact field names for your Sysmon version, then
  filter on those names; the page does not list this event's fields.
- Name rules (`name` attribute) so the event records which rule matched.

## Reviewing events
For each hit identify the source process via its ProcessGuid and process creation event
(command line, parent, hashes), and decide whether it is an expected security or management
tool or an unknown binary. Build the exclude list from tools you have verified in your
environment, not from public lists.

## Verify
Test in a lab with a known benign access to the target process and confirm the event appears
and your filters behave as intended before relying on the detection.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full): Event 10 purpose, LSASS credential-theft note, volume warning, ProcessAccess filter tag, `image` condition, include/exclude precedence, AND/OR rules, rule naming. Removed: GrantedAccess mask table, CallTrace analysis, PPL/RunAsPPL claim, Mimikatz/procdump/comsvcs specifics, procdump lab test, the Win32 access rights and SwiftOnSecurity sources (not read).
Method: documentation only; no commands were run.
