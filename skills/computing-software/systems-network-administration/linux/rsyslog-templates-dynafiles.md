---
id: computing-software.systems-network-administration.linux.rsyslog-templates-dynafiles
name: rsyslog-templates-dynafiles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rsyslog, rsyslog-templates, dynafile, property-replacer, json-logs, log-format, omfile, rfc5424, logging, sysadmin]
level: advanced
status: docs-checked
description: "Shape rsyslog output with templates: string, list and JSON templates, property replacer options, dynaFile paths per host/date/program, dynaFileCacheSize, and safe directory creation."
sources:
  - https://www.rsyslog.com/doc/configuration/templates.html
  - https://www.rsyslog.com/doc/configuration/property_replacer.html
  - https://www.rsyslog.com/doc/configuration/modules/omfile.html
  - https://www.rsyslog.com/doc/configuration/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rsyslog templates and dynafiles

**Goal:** control exactly what each log line looks like (including JSON for shippers) and
write to file paths built from message properties.

## 1. Template types
```
# string: quick, uses %property:options%
template(name="ShortFmt" type="string" string="%timegenerated:::date-rfc3339% %HOSTNAME% %syslogtag%%msg:::sp-if-no-1st-sp%%msg:::drop-last-lf%\n")

# list: structured, escapes properly — use for JSON
template(name="JsonFmt" type="list" option.jsonf="on") {
    property(outname="@timestamp" name="timereported" format="jsonf")
    property(outname="host"       name="hostname"     format="jsonf")
    property(outname="severity"   name="syslogseverity-text" format="jsonf")
    property(outname="facility"   name="syslogfacility-text" format="jsonf")
    property(outname="program"    name="programname"  format="jsonf")
    property(outname="message"    name="msg"          format="jsonf")
}
```
`option.jsonf` makes rsyslog emit `{...}` and handle commas/escaping; hand-built JSON strings break on quotes in messages.
Built-ins: `RSYSLOG_FileFormat` (high-precision timestamps), `RSYSLOG_TraditionalFileFormat`, `RSYSLOG_SyslogProtocol23Format` (RFC 5424).

## 2. Property replacer cheatsheet
`%msg:1:40%` (characters 1–40), `%msg:R,ERE,1,FIELD:id=([0-9]+)--end%` (regex capture),
`%hostname:::lowercase%`, `%timereported:::date-year%`, `%timegenerated:::date-rfc3339%`, `%fromhost-ip%`; date options such as `date-rfc3339` belong to string templates (or to the property replacer options).

## 3. Dynamic file names
```
template(name="ByHostDay" type="string" string="/var/log/remote/%HOSTNAME%/%$year%-%$month%-%$day%.log")
action(type="omfile" dynaFile="ByHostDay" template="RSYSLOG_FileFormat"
       dynaFileCacheSize="200" createDirs="on" dirCreateMode="0750" fileCreateMode="0640"
       dirOwner="root" dirGroup="adm" asyncWriting="on" flushInterval="2" ioBufferSize="64k")
```
- `dynaFileCacheSize` = open file handles kept; set ≥ number of distinct active files, or rsyslog thrashes opening/closing.
- Date-based names give per-day files without logrotate; prune old ones with a scheduled job of your own.
- Use `%$year%` (system time at processing) or `%timereported:::date-year%` (sender's time) deliberately.

## 4. Apply templates
`action(type="omfile" file="/var/log/app.json" template="JsonFmt")`, or legacy `*.* /var/log/x;ShortFmt`.
Module-wide defaults for file actions go on `module(load="builtin:omfile" Template="RSYSLOG_FileFormat")`; the omfile docs recommend this or per-action parameters and say not to mix them with legacy selector actions.

## Gotchas
- Hostname from untrusted senders in a path: sanitise (`%hostname:::secpath-replace%` turns a slash into an underscore; `secpath-drop` removes slashes) to stop `../` path tricks. omfile also has a `dynafile.restrictTemplateType` module option that blocks rendered paths escaping the template's static prefix.
- Changing a template doesn't rewrite old lines; plan parsers for the transition.

## Verify
- [ ] `rsyslogd -N1` clean; a `logger` line appears in the expected dynafile path with the expected format.
- [ ] The JSON output parses with your JSON tool of choice for messages containing quotes and backslashes.

## Checked
Checked 2026-10-25 against the rsyslog documentation source on GitHub (rsyslog/rsyslog doc/source, main, release 8.2610.0 of 2026-10-20). Confirmed: template types `string` and `list`, `option.jsonf`, property `outname`/`name`/`format="jsonf"`, built-in names `RSYSLOG_FileFormat`, `RSYSLOG_TraditionalFileFormat`, `RSYSLOG_SyslogProtocol23Format`, property options `sp-if-no-1st-sp`, `drop-last-lf`, `date-rfc3339`, `date-year`, `lowercase`, `secpath-replace`/`secpath-drop`, regex extraction `R,ERE`, system property `$year`, message properties `fromhost-ip`, `syslogseverity-text`, `syslogfacility-text`, `programname`, `timereported`, omfile `dynaFileCacheSize` (default 10, open handles cached), `asyncWriting`, `flushInterval`, `ioBufferSize`, `dirOwner`, `dirGroup`, `createDirs`, `dirCreateMode`, `fileCreateMode`. Removed unconfirmed claims: the `dateFormat` property attribute, the `%$!%` shorthand, the first-load rule for omfile, config-order rule for templates and the find-based pruning example.

Method: documentation only; no commands were run.
