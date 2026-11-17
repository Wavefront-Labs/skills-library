---
id: computing-software.cybersecurity-defensive.suricata.suricata-update-enable-disable
name: suricata-update-enable-disable
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [enable-conf, disable-conf, rule-filtering, sid-selection]
level: practitioner
status: docs-checked
description: "Turn rules on or off with enable.conf and disable.conf using SIDs, group: file names and re: regexes."
sources: ["https://docs.suricata.io/en/latest/rule-management/suricata-update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# enable.conf and disable.conf

`enable.conf` turns on rules disabled by default; `disable.conf` turns rules off. Both take the same three entry formats:

- a SID, for example `2019401`
- a rule file group, for example `group:emerging-icmp.rules`
- a regex on rule text, for example `re:trojan` (or `re:heartbleed` in disable)

After editing either file rerun `suricata-update`, then restart Suricata.

The page documents these two files only; consult the suricata-update project docs for modify.conf, drop.conf and local rules.

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/rule-management/suricata-update.html (read in full); dropped the reload option, since the page only says restart.
