---
id: computing-software.digital-forensics-incident-response.log-analysis.deploying-and-tuning-sysmon
name: deploying-and-tuning-sysmon
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-config, sysmon, endpoint-telemetry, logging-baseline, dfir]
level: practitioner
status: docs-checked
description: "Deploy and tune Sysmon: install and update switches, config entries, include/exclude rules, rule groups and rule names for controlling volume."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying and tuning Sysmon

**Goal:** high-value endpoint telemetry in the Windows event log at an acceptable volume.
Sysmon is a Windows service and device driver that stays resident across reboots; it does not
analyse events and does not hide itself from attackers. Collect its events with Windows Event
Collection or a SIEM agent.

## Install and update
```
sysmon64 -accepteula -i sysmonconfig.xml     # install with a config
sysmon64 -c sysmonconfig.xml                 # update the config of an installed Sysmon
sysmon64 -c                                  # dump the current config
sysmon64 -c --                               # revert to default settings
sysmon64 -s                                  # print the config schema
sysmon64 -m                                  # install the event manifest
sysmon64 -u [force]                          # uninstall
```
- Neither install nor uninstall requires a reboot. `-accepteula` skips the EULA prompt.
- The driver installs as a boot-start driver so activity early in boot is captured.
- Sysmon reloads its configuration automatically if changed in the registry.
- Events are in Applications and Services Logs/Microsoft/Windows/Sysmon/Operational (Vista and
  higher) with UTC timestamps. Event 4 is a service state change and 16 a configuration change.
- A default install hashes process images with SHA1 and does no network monitoring.

## Config structure
The `Sysmon` tag has a `schemaversion` attribute (independent of the binary version;
`-? config` shows the current one). Entries sit directly under it, filters under `EventFiltering`.
Config entries include `HashAlgorithms` (MD5, SHA1, SHA256, IMPHASH, `*`; default none),
`CheckRevocation` (default True), `DnsLookup` (default True), `DriverName`, `ArchiveDirectory`,
and the `CopyOnDelete*` entries.
```xml
<Sysmon schemaversion="4.82">
  <HashAlgorithms>*</HashAlgorithms>
  <EventFiltering>
    <RuleGroup name="" groupRelation="or">
      <ProcessCreate onmatch="exclude">
        <Image condition="end with">\vendor\agent.exe</Image>
      </ProcessCreate>
    </RuleGroup>
  </EventFiltering>
</Sysmon>
```
Rules:
- `onmatch="include"` logs only matches; `onmatch="exclude"` logs everything except matches.
  You may have both for one event; excludes take precedence.
- Same field name rules are ORed, different field names ANDed. A `RuleGroup` with
  `groupRelation` set to `and` or `or` overrides how rules combine.
- Conditions (case insensitive) include is, is any, is not, contains, contains any/all,
  excludes, begin with, end with, less than, more than, and image.
- Add a `name` attribute to a rule to make Sysmon report which rule matched.
- Events 4 and 16 cannot be filtered.

## Tuning loop
Deploy to a pilot group, measure events per host by Event ID, add exclusions for expected noise
using precise conditions (the image condition accepts a full path), and re-measure. Event 7
(image load) and Event 10 (process access) warn of heavy volume.

## Verify
Generate known activity for the events you rely on and confirm they appear with the expected
fields on a pilot host and in the SIEM.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full): switches, no reboot, boot-start driver, automatic reload, log location, UTC, config entries and defaults, include/exclude semantics, rule groups, conditions, rule names, unfilterable events 4 and 16. Removed: SwiftOnSecurity and sysmon-modular claims (repos not read), `wevtutil` log-size command, registry config path, ATT&CK rule-name example, Atomic Red Team test, advice that attackers can unload Sysmon.
Method: documentation only; no commands were run.
