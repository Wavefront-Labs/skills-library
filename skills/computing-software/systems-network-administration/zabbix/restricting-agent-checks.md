---
id: computing-software.systems-network-administration.zabbix.restricting-agent-checks
name: restricting-agent-checks
category: computing-software
field: systems-network-administration
product: zabbix
tags: [allowkey, denykey, agent-security, system-run, restrict]
level: advanced
status: docs-checked
description: "Control which item keys an agent may run with ordered AllowKey and DenyKey rules, and how system.run is handled."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/restrict_checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agent and agent 2 accept any number of AllowKey=<pattern> and DenyKey=<pattern> lines (and AllowKeyRegexp / DenyKeyRegexp for regular expressions). Each pattern holds a single item key. For AllowKey and DenyKey, * matches any number of any characters; exact keys are preferred over wildcards. Rules are evaluated top to bottom, and the first match decides and stops evaluation.

Order matters. This allows the check:
AllowKey=vfs.file.contents[/etc/passwd]
DenyKey=vfs.file.*[*]
while the reverse order denies it, because the deny rule matches first.

Other rules from the docs:
- All system.run items are disabled by default, as if DenyKey=system.run[*] were the last rule, so you can allow specific system.run keys without denying the rest.
- Denied items become unsupported without hints or error messages; for example the agent -t option returns "Unsupported item key." for them.
- Prefer allowlisting only what is needed and denying everything else. Some keys can be abused for path traversal such as vfs.file.contents with ../ segments, and new agent versions can add keys your DenyKey rules do not cover.
- The rules do not apply to the HostnameItem, HostMetadataItem or HostInterfaceItem parameters.

The rules cover item checks, remote commands and scripts.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Restricting agent checks (current): the four parameters, wildcard and single-key pattern rules, unlimited rule count, top-to-bottom first-match order and the example, system.run default denial, allowlist advice and path traversal warning, HostnameItem/HostMetadataItem/HostInterfaceItem exemption, silent unsupported result. Removed the unconfirmed agent-will-not-start rule and the zabbix_get verification step.

Method: documentation only; no commands were run.
