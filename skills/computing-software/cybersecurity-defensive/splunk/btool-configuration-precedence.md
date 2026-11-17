---
id: computing-software.cybersecurity-defensive.splunk.btool-configuration-precedence
name: btool-configuration-precedence
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-architecture, btool, configuration-precedence, conf-files, troubleshooting, app-context, local-vs-default]
level: practitioner
status: draft
description: "Troubleshoot Splunk configuration with btool: global vs app/user precedence, --debug to find which file wins, and fixing settings that silently do not apply."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Admin/Wheretofindtheconfigurationfiles", "https://docs.splunk.com/Documentation/Splunk/latest/Troubleshooting/Usebtooltotroubleshootconfigurations", "https://docs.splunk.com/Documentation/Splunk/latest/Admin/Configurationfileprecedence"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# btool and configuration precedence

Most "my props.conf does nothing" problems are precedence problems.

## Commands
```
$SPLUNK_HOME/bin/splunk btool props list WinEventLog:Security --debug
$SPLUNK_HOME/bin/splunk btool inputs list --debug | grep -v "default/"
$SPLUNK_HOME/bin/splunk btool savedsearches list "My Rule" --app=my_detections --debug
$SPLUNK_HOME/bin/splunk btool check            # syntax/typo check across all conf files
```
`--debug` prefixes each line with the file that supplied it: the answer to "which copy wins".

## Precedence rules
**Global context** (index-time: inputs, outputs, props/transforms at parse time, indexes, server):
1. `etc/system/local`
2. `etc/apps/<app>/local` (apps in ASCII order, A beats Z... uppercase before lowercase)
3. `etc/apps/<app>/default`
4. `etc/system/default`
On indexer cluster peers, `etc/peer-apps` (formerly slave-apps) beats all of these.

**App/user context** (search-time: eventtypes, tags, field extractions, savedsearches):
1. current user `etc/users/<user>/<app>/local`
2. current app local, then default
3. other apps' exports (`export = system` in metadata) by ASCII order
4. system
So a search-time extraction in app B is invisible in app A unless exported.

## Fix patterns
- Never edit `default/`; put overrides in `local/`.
- A setting in `etc/system/local` overrides every app: remove stray copies left by old admins.
- Stanza names: `[source::...]` beats `[host::...]` beats `[sourcetype]` for props.conf, regardless of file.
- Changes to index-time settings need a restart (or `debug/refresh` for some search-time ones);
  `splunk reload deploy-server` for deployment server classes.

## Distributed gotchas
- Settings must exist on the tier where they apply: props for parsing on HF/indexers, search-time
  extractions on search heads.
- Search head cluster: deploy via deployer; local edits on a member are replicated only for
  runtime-changed knowledge objects.
- `btool` reads disk, not running config: after editing without restart, btool shows the new
  value while splunkd still runs the old one.

## Verify
`splunk btool <conf> list <stanza> --debug` shows your file path on the setting line, and the
behaviour changes after restart/reload.
