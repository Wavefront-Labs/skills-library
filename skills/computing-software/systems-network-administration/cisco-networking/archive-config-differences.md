---
id: computing-software.systems-network-administration.cisco-networking.archive-config-differences
name: archive-config-differences
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, config-diff, archive-config, incremental-diffs, change-logger, config-audit, change-management]
level: practitioner
status: docs-checked
description: "Diff IOS configurations on the box: show archive config differences and incremental-diffs, running vs startup, archive log config change history, and reading +/- output."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/config-mgmt/configuration/xe-16/config-mgmt-xe-16-book/cm-config-diff.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/config-mgmt/configuration/xe-16/config-mgmt-xe-16-book/cm-config-logger.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing configurations on IOS

The Contextual Configuration Diff Utility compares any two configuration files reachable through the IOS File
System (IFS) line by line and reports added, modified and deleted lines and the configuration mode each sits in.

## Unsaved changes: running vs startup
```
show archive config differences nvram:startup-config system:running-config
```
Syntax is `show archive config differences [file1 [file2]]`. Read the output relative to the order given:
`-` means the line is in file1 but not file2, `+` means it is in file2 but not file1, and `!` with a comment marks
an order-sensitive line (for example `ip access-list` or community lists) whose position differs between the files.

## Against a pre-change snapshot
Save the running configuration to a file on the device's file system before the change, make the change, then
compare the snapshot with the running configuration:
```
show archive config differences <snapshot-file> system:running-config
show archive config incremental-diffs <snapshot-file>
```
`incremental-diffs file` compares the named file with the running configuration and prints only the lines that
appear in the named file and not in the running configuration, without `+`/`-` symbols (`!` still marks
order-sensitive lines that moved). It is not a ready-made back-out script: it lists lines of the OLD file that
the running config lacks.

## Requirements and limits
- Both files must follow standard indentation: top-level commands unindented, one space per submode level.
- The device needs a contiguous block of memory larger than the two files combined, or the diff fails.

## Who changed what: config change logger
```
archive
 log config
  logging enable
  logging size 500
  hidekeys
  notify syslog
show archive log config 1 20
show archive log config all provisioning
show archive log config statistics
```
- The log records, per command: the command, the configuration mode, the user, the time, a sequence number and
  parser return codes. It tracks changes made through the CLI or HTTP; partial commands and syntax errors are not logged.
- `logging size` takes 1 to 1000 entries (default 100); `hidekeys` suppresses password information in the log;
  `notify syslog` sends configuration-change notifications to syslog so the history is kept off the device.
- `show archive log config number [end-number]` lists entries by record number (range 1 to 2147483647), `all provisioning`
  shows the log as it would appear in a configuration file, and `statistics` shows memory use.

## Verify
- [ ] The diff before `write memory` matches the change ticket exactly.
- [ ] `show archive log config` shows the change under the expected user.

## Checked
Date: 2026-11-07. Both cited pages (Contextual Configuration Diff Utility, about 17k characters; Configuration
Change Notification and Logging, about 15k) were read section by section (concepts, prerequisites, steps, both sample
outputs, show commands); the long sample configuration tables and feature-history tables were skimmed.
Confirmed: `show archive config differences [file1 [file2]]` and `show archive config incremental-diffs file`, the
`+`, `-` and `!` symbols, incremental-diff semantics, indentation and contiguous-memory requirements, logged fields,
`logging enable`, `logging size` range and default, `hidekeys`, `notify syslog`, and the three `show archive log config`
forms with their ranges.
Removed or corrected: the claim that `incremental-diffs` lists commands to reach the running config (it lists lines
only in the named file); the `!Contextual Config Diffs:` header, `notify syslog contenttype plaintext`,
`show archive log config user admin`, `%PARSER-5-CFGLOG_LOGGEDCMD`, the `copy running-config bootflash:` command,
the `| exclude` filter, `show running-config all` and `configure replace` gotchas (none on these pages), and the
`show archive log config all` form (the page has `all provisioning`).
Method: documentation only; no commands were run.
