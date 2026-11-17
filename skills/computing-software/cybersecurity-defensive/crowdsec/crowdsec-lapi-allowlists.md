---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-lapi-allowlists
name: crowdsec-lapi-allowlists
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [allowlists, cscli-allowlists, lapi-allowlist, ip-range, allowlist-expiry]
level: practitioner
status: docs-checked
description: "Manage centralised IP and range allowlists on the Local API with cscli allowlists and see how they affect alerts, blocklists and AppSec."
sources: ["https://raw.githubusercontent.com/crowdsecurity/crowdsec-docs/main/crowdsec-docs/docs/local_api/allowlists.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
AllowLists live at LAPI level and affect:

| Area | Effect |
| --- | --- |
| Local alerts | alert dropped, action logged |
| Blocklists | IP removed before database insertion |
| WAF (AppSec) and bot detection | request bypasses them entirely; refreshed every minute |
| cscli | decision refused unless a special flag is given |

They are IP or range only. For rules on log elements such as URLs use parser whitelists or profile rules. An allowlisted IP skips AppSec entirely, so it is also never served the bot-detection challenge.

## Commands (create, add, remove and delete must run on the LAPI)

```console
cscli allowlists create my_allowlist --description "test allowlist"
cscli allowlists add my_allowlist 1.2.3.4 -e 7d -d "office"
cscli allowlists remove my_allowlist 1.2.3.4
cscli allowlists inspect my_allowlist
```

The description on `create` is mandatory. Entries default to no expiry; `-e` sets one. You cannot add a value twice: remove and re-add to change it. `inspect` can run on the LAPI or any log processor machine. `cscli allowlists delete <name>` deletes an allowlist and all its content.

Premium users can manage allowlists centrally in the Console, which requires subscribing the engines afterward.

## Checked
2026-11-08. Confirmed against the AllowLists page source in the crowdsec-docs repository (the docs.crowdsec.net/docs/local_api/allowlists URL returned 404, so the raw source is cited): effect table, IP/range limit, create/add/remove/inspect/delete commands, mandatory description, expiry and duplicate rules, where each command runs, Premium note. Removed: the `check|list|import` subcommands and the `--bypass-allowlist` flag name (not on the page; it only says a special flag is needed).
Method: documentation only; no commands were run.
