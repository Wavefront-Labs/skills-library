---
id: computing-software.systems-network-administration.pi-hole.troubleshoot-common-pihole-oddities
name: troubleshoot-common-pihole-oddities
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-faq, chrome-random-queries, suite-change-error]
level: intro
status: draft
description: "Explain three frequent surprises: random-string queries from Chrome, IDN warnings in gravity, and apt Suite changes blocking updates."
sources: ["https://docs.pi-hole.net/main/faq/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Common Pi-hole surprises

**Random strings in the query log**

Three queries of 7 to 15 random characters (for example `yfjmdpisrvyrnq`), sometimes with the local domain suffix, come from Chrome-based browsers. Chrome probes with random names to detect DNS servers that answer wildcards. A normal setup returns "No such name", so nothing is wrong. No fix is needed.

**Gravity complains about invalid IDN domains**

A sample such as `rëddït.com` or `test.中国` is printed during a gravity run. DNS servers only see punycode, so ask the list maintainer to convert entries to punycode.

**Update fails after an OS upgrade**

After a manual major OS upgrade on deb-based systems you may see:

```text
Repository ... changed its 'Suite' value from 'stable' to 'oldstable'
```

Fix:

```bash
sudo apt-get update --allow-releaseinfo-change
```

Then rerun `pihole -up`.

**Checklist**

1. Match the symptom to one of the three cases.
2. Apply the fix or leave the Chrome probes alone.
3. Run `pihole debug` if the symptom is something else.
