---
id: computing-software.systems-network-administration.cisco-networking.persistent-logging-to-flash
name: persistent-logging-to-flash
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, syslog, logging-persistent, logging-buffered, crashinfo, log-retention, flash-logging]
level: practitioner
status: draft
description: "Keep IOS XE logs across reloads with logging persistent to flash, size and rotation settings, and how to read the files after a crash."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-sys-msg-log.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/command/esm-cr-book/esm-cr-l1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Persistent logging to flash

## Problem
`logging buffered` lives in RAM: a crash or reload wipes exactly the messages you need.
Remote syslog may miss them too (link down, UDP loss).

## Configure
```
logging buffered 1000000 informational
logging persistent url flash:/syslog size 10000000 filesize 1000000
logging persistent batch 4096           ! write in batches to reduce flash wear
logging persistent notify               ! log when a file rotates
```
- `size` = total space for all log files; `filesize` = each file; oldest files are deleted on rotation.
- The directory is created automatically; files named `log_<date>` style.
- On some releases `logging persistent immediate` writes each message at once (more flash writes).

## Reading after an event
```
dir flash:/syslog
more flash:/syslog/<FILE>
show logging persistent                 ! on releases that support it
show logging onboard                    ! hardware OBFL: temperature, voltage, resets (Catalyst)
dir crashinfo:                          ! crash files
```

## Gotchas
- Flash wear and space: keep size modest (10-50 MB) and use batch mode.
- On stacks, each member has its own flash; persistent logging writes on the active member.
- Includes only messages at or above the buffered/console level you configured.
- Config archive and logs on the same flash: monitor free space (`show flash: | include free`).

## Verify
- [ ] After `reload`, messages from before the reload are in `flash:/syslog`.
- [ ] `show logging | include Persistent` shows enabled with the expected URL.
