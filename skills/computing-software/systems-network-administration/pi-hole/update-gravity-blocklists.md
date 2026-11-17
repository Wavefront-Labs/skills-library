---
id: computing-software.systems-network-administration.pi-hole.update-gravity-blocklists
name: update-gravity-blocklists
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [gravity-update, adlist-subscriptions, list-status-codes]
level: practitioner
status: draft
description: "Rebuild the blocking database from subscribed lists with pihole -g and read the per-list status codes."
sources: ["https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Update gravity (blocklists)

Gravity retrieves your subscribed lists and consolidates them into one unique list for the DNS server. It also completes manual allowlisting, denylisting and wildcard updates. It runs automatically each week and can be run any time:

```bash
pihole updateGravity    # or: pihole -g
```

**What it does**

1. Checks internet connectivity.
2. Reads the URLs from the `adlist` table in `/etc/pihole/gravity.db`.
3. Downloads each list; `curl` uses the `Last-Modified` header so unchanged lists are not fetched again.
4. Parses files into domains-only form, merges them, removes comments and sorts uniquely.
5. Stores the result in the `gravity` table, cleans up and reloads the DNS server.

**Status per list** (`adlist.status`):

| Value | Meaning |
| --- | --- |
| 1 | Download successful |
| 2 | Unchanged upstream, local copy used |
| 3 | Unavailable, local copy used |
| 4 | Unavailable, no local copy |

`date_updated` does not change when the download was unchanged. The `invalid_domains` column counts rejected entries.

**Invalid IDN warnings.** DNS stores only punycode, so gravity complains about names such as `rëddït.com`. Ask the list maintainer to convert them to punycode.

Use `pihole query -exact example.com` to see which lists contain a domain.
