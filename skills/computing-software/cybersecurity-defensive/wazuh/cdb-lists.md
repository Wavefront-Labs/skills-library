---
id: computing-software.cybersecurity-defensive.wazuh.cdb-lists
name: cdb-lists
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [cdb-list, lookup, match-key, address-match-key, ruleset-list, threat-intelligence]
level: practitioner
status: docs-checked
description: "Create Wazuh CDB lists: key:value file format, quoting keys with colons, subnet dot notation, registering in ruleset, and the rule list lookup options."
sources:
  - https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Format: a plain text file with one entry per line as `key:value` (value optional). Keys must be unique; values may repeat.
- Keys containing a colon, such as MAC addresses, must be quoted: `"a0:a0:a0:a0:a0:a0":`
- IP lists use dot notation for subnets: `192.168.:` matches 192.168.0.0 to 192.168.255.255.
- The page recommends storing lists in `/var/ossec/etc/lists`.

Register each list in the `<ruleset>` block of `/var/ossec/etc/ossec.conf` with a relative path, for example `<list>etc/lists/list-IP</list>`.

Lists are built and loaded automatically when the analysis engine starts; no separate compile command is described. Restart the manager after adding or changing a list: `systemctl restart wazuh-manager`.

Use in a rule:

```xml
<list field="user" lookup="match_key">etc/lists/list-user</list>
```

Lookups: `match_key` (default), `not_match_key`, `address_match_key`, `not_address_match_key`, `match_key_value` and `address_match_key_value` (the last two take a `check_value` regex).

Gotchas:
- For IP address fields such as `srcip`, the page says to use the `address_*` lookups.
- Changes have no effect until the manager restarts.
- Quote any key that contains a colon.

## Checked

2026-11-03. Confirmed against the Wazuh page "Using CDB lists": key:value format and uniqueness, quoted keys with colons, dot-notation subnet keys, /var/ossec/etc/lists recommendation, the `<ruleset><list>` relative path, automatic build on engine start and manager restart, and all six lookup types with `check_value`. Removed: the unsupported "subnet entries will not match" consequence.

Method: documentation only; no commands were run.
