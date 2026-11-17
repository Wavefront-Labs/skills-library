---
id: computing-software.systems-network-administration.cisco-networking.aaa-command-authorization-and-accounting
name: aaa-command-authorization-and-accounting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, aaa, aaa-authorization, aaa-accounting, tacacs-plus, command-authorization, audit-trail]
level: practitioner
status: docs-checked
description: "Enforce per-command authorization and record every command with TACACS+ accounting on IOS, including config-mode coverage and safe fallback."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_aaa/configuration/xe-16/sec-usr-aaa-xe-16-book/sec-cfg-authorizatn.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_aaa/configuration/xe-16/sec-usr-aaa-xe-16-book/sec-cfg-accountg.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/config-mgmt/configuration/xe-16/config-mgmt-xe-16-book/cm-config-logger.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AAA command authorization and accounting

Builds on TACACS+ authentication (see tacacs-plus-device-administration).

## Authorization: who may run what
```
aaa authorization commands 1 default group tacacs+ local if-authenticated
aaa authorization commands 15 default group tacacs+ local if-authenticated
```
- The `commands level` type authorizes EXEC commands, including global configuration commands, at the given
  privilege level (0 to 15); the command set itself lives on the TACACS+ server.
- Configuration-mode commands are covered by the same `commands` method list. The authorization chapter
  documents `no aaa authorization config-commands` as the way to STOP configuration-command authorization, so do
  not enter it unless you mean to exempt config mode.
- Method lists are tried in order, and the next method is tried only when the previous one does not respond.
  If the server (or local database) answers with a denial, authorization stops and no later method is tried.
- `if-authenticated` as the last method grants every requested function to an authenticated user when the
  earlier methods did not respond. The `local` method consults the local `username` database, which controls
  only a limited set of functions.
- Test with a non-admin account first and keep a console session open: a wrong command set on the server can
  block the commands you need to fix it.
- By default AAA authorization is disabled on the console; `no aaa authorization console` is the command the
  chapter gives to keep it off if it was enabled.

## Accounting: what was done
```
aaa accounting exec default start-stop group tacacs+
aaa accounting commands 1 default start-stop group tacacs+
aaa accounting commands 15 default start-stop group tacacs+
aaa accounting connection default start-stop group tacacs+
aaa accounting system default start-stop group tacacs+
```
- `start-stop` sends a record at the start and another at the end of the event; `stop-only` is the minimal option.
- Command accounting records the commands executed at that privilege level, the date and time of each, and the
  user who ran it. EXEC accounting covers user EXEC terminal sessions, connection accounting covers outbound
  connections (Telnet, rlogin and similar), and system accounting covers system-level events. System accounting
  uses only the default list.
- A server group named `tacacs+` is the built-in TACACS+ group keyword; a custom name needs a matching
  `aaa group server tacacs+ NAME` definition.

Local supplement that does not depend on the server: the configuration change logger
```
archive
 log config
  logging enable
  logging size 500
  hidekeys
  notify syslog
```
`logging size` accepts 1 to 1000 entries (default 100); when the log is full the oldest entry is deleted.
`hidekeys` suppresses password information in the log.

## Verify
```
show accounting
show archive log config statistics
```
- [ ] `show accounting` lists the active accountable events; `show archive log config statistics` reports the
  configuration log's memory use (`show archive log config number` lists entries).
- [ ] Both permitted and denied commands of a test user show in the TACACS+ server's accounting log.

## Checked
Date: 2026-11-07. Pages: the Configuring Authorization and Configuring Accounting chapters (xe-16 AAA book) and the
Configuration Change Notification and Logging page, all fetched and searched for each claim (the accounting chapter is
67k characters and was searched by keyword and read around the hits, not cover to cover).
Confirmed: `aaa authorization {... commands level ...}` syntax, ordered method fallback and denial-stops rule,
`if-authenticated` and `local` descriptions, `no aaa authorization config-commands`, console default, accounting
types and `start-stop`/`stop-only`, command-accounting record contents, `logging size` range and default, `hidekeys`,
`notify syslog`, `show accounting`.
Removed or changed: the claim that config-mode commands are not authorized by default (the page implies the opposite);
`group TACACS` replaced by the `group tacacs+` keyword; the invented `Command authorization failed` message, the
`show aaa sessions` Verify step, the `notify syslog contenttype plaintext` option and the ISE Live Logs menu path (none
on these pages); the accounting source URL was a 404 and was replaced by the live `sec-cfg-accountg.html` page.
Method: documentation only; no commands were run.
