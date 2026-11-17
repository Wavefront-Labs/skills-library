---
id: computing-software.systems-network-administration.pi-hole.privacy-levels
name: privacy-levels
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [privacy-level, anonymous-mode, hide-domains]
level: practitioner
status: docs-checked
description: "Pick a Pi-hole privacy level 0 to 3 and know which statistics and logging each level disables."
sources: ["https://docs.pi-hole.net/ftldns/privacylevels/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Privacy levels

Set `misc.privacylevel` (default `0`) from the dashboard Settings page or the FTL config. The level can be changed at any time without restarting the DNS resolver. Details already hidden cannot be disclosed by later lowering the level.

| Level | Behaviour | Disabled features |
| --- | --- | --- |
| 0 | Show everything | None |
| 1 | Domains stored and shown as `hidden` | Top Domains, Top Ads |
| 2 | Domains hidden and clients stored as `0.0.0.0` | Top Domains, Top Ads, Top Clients, Clients over time |
| 3 | Anonymous mode | All of level 2, plus Query Log and long-term database logging |

The config reference adds that at level 3 you will lose most regex features, and that changing the setting triggers an FTL restart in the reference documentation, while the privacy page says no restart of the DNS resolver is needed.

**Apply**

```bash
sudo pihole-FTL --config misc.privacylevel 1
```

**Related logging.** `dns.queryLogging` controls whether queries are written to `pihole.log`; `webserver.api.excludeClients` and `excludeDomains` exclude matching clients or domains from the query log and top clients or top domains API responses (regex arrays).

**Checklist**

1. Choose the lowest detail you need.
2. Remember data hidden earlier stays hidden.
3. Level 3 removes the query log.

## Checked

2026-11-03. Read the Privacy levels page and the FTL configuration reference (`misc.privacylevel` default 0, restart note, level 3 regex note, `dns.queryLogging`, `webserver.api.excludeClients` and `excludeDomains`). Reworded the exclude options to the endpoints the reference names (query log, top clients, top domains). The `pihole-FTL --config` form is the reference's own CLI example.

Method: documentation only; no commands were run.
