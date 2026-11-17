---
id: computing-software.systems-network-administration.zabbix.external-checks
name: external-checks
category: computing-software
field: systems-network-administration
product: zabbix
tags: [external-check, externalscripts, script-key, wrapper-script, external, script, checks]
level: advanced
status: docs-checked
description: "Run scripts or binaries from the server's ExternalScripts directory as items, and know their cost and limits."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/external
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An external check runs a shell script or binary on the Zabbix server (or proxy for proxied hosts). No agent is needed on the monitored host.

Key syntax: script[<parameter1>,<parameter2>,...]. Use script[] or plain script when there are no parameters. Example: check_oracle.sh["-h","{HOST.CONN}"] runs check_oracle.sh '-h' '192.168.1.4' when the host uses an IP interface.

Rules from the docs:
- Only commands inside the directory set by the ExternalScripts parameter in the server or proxy configuration can run.
- The process runs as the same user as the Zabbix server or proxy. Handle permissions and environment variables in a wrapper script, and make the file executable by that user.
- The return value is standard output together with standard error, limited to 16 MB. Text, character and log items do not become unsupported just because of stderr output.
- A timeout makes the item unsupported with an error, and the process forked for the script is terminated.

Performance: each check forks a process, so many external checks can slow the server noticeably. Prefer agent items, HTTP agent items, script items or trapper items when they can do the job, and keep external check intervals long.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/items/itemtypes/external): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: the default ExternalScripts path and the missing-script error claim (not on the page).

Method: documentation only; no commands were run.
