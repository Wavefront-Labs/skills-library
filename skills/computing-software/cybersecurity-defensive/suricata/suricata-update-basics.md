---
id: computing-software.cybersecurity-defensive.suricata.suricata-update-basics
name: suricata-update-basics
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [suricata-update, emerging-threats, rule-updates, rule-sources]
level: intro
status: docs-checked
description: "Update rules with suricata-update: first run, the merged suricata.rules output, rule-files configuration, and the sources commands."
sources: ["https://docs.suricata.io/en/latest/rule-management/suricata-update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# suricata-update

Bundled with Suricata 4.1 and later. `suricata-update` downloads the Emerging Threats Open ruleset by default and merges all rules into `suricata.rules` in the rules directory. Point `default-rule-path` there and list `suricata.rules` under `rule-files`, then restart Suricata. Run it often.

## Sources
- `update-sources`: fetch the index from OISF.
- `list-sources`: available rulesets, named vendor/set such as `oisf/trafficid`.
- `enable-source <name>`: enable one; rerun `suricata-update`, then restart.
- `list-enabled-sources`: show active sources.

Suricata-Update also works with Suricata older than 4.1 if installed separately.

## Checked

Method: docs-checked 2026-11-09 against https://docs.suricata.io/en/latest/rule-management/suricata-update.html (read in full); replaced the live-reload pointer, which is not on this page.
