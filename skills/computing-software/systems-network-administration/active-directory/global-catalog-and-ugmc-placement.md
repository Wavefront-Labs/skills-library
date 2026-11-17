---
id: computing-software.systems-network-administration.active-directory.global-catalog-and-ugmc-placement
name: global-catalog-and-ugmc-placement
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-sites, global-catalog-placement, universal-group-membership-caching, ugmc, global-catalog, set-addomaincontroller, isglobalcatalog, exchange, branch-office]
level: practitioner
status: docs-checked
description: "Decide where global catalogs live and when to use universal group membership caching at small sites; enable or disable the GC and verify it advertises."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/planning-global-catalog-server-placement
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-add-gc
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-remove-gc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Global catalog placement and UGMC

## Why it matters
In multiple-domain forests, GCs facilitate user logon requests and forest-wide searches (a user can belong to a
universal group in another domain). Only DCs designated as GCs answer GC queries on port 3268. Searches such as
"Find People" and expanding universal groups go to a GC. Exchange, Message Queuing and some DCOM applications perform
poorly over latent WAN links and need a highly available GC.

## Placement rules (Microsoft's planning guidance)
- Single-domain forest: make **every DC a GC**; it costs no extra disk, CPU or replication, and it avoids deciding which
  DCs can answer GC queries.
- Multiple domains: in most cases include the GC when you install a new DC. Exceptions: limited WAN bandwidth in a remote
  site (use universal group membership caching there), and the infrastructure master (do not put the GC on the
  infrastructure master DC unless every DC in the domain is a GC or the forest has one domain).
- Place GCs at locations with more than 100 users, and where applications need low query latency (for example Exchange).
  Locations with fewer than 100 users, no GC-dependent apps and no large roaming population can use UGMC. Roaming users
  contact a GC at their first logon at any location.
- RODCs can be GCs, but some directory-enabled applications do not support that.

## Toggle GC
GUI: Sites and Services > site > server > NTDS Settings > Properties > **Global Catalog** check box. Command line,
from the forest recovery guide:
```cmd
repadmin /options <DC_NAME> +IS_GC
repadmin /options <DC_NAME> -IS_GC
```
New DCs: `Install-ADDSDomainController -NoGlobalCatalog` leaves the GC off.

## Universal Group Membership Caching
Enable it per site in Sites and Services (the site's NTDS Site Settings), for locations with fewer than 100 users. The
DC caches users' universal group memberships. Keep the GCs no more than one replication hop from the DC that has
caching enabled so the cache can refresh.
- Users logging on for the first time while the WAN is down still fail.
- Not useful when apps need full GC queries; it only covers logon.

## Verify
- [ ] `nltest /dsgetdc:<domain> /gc` from a branch client returns a local GC (or the site uses UGMC by design).
- [ ] `dcdiag /test:advertising` passes: it checks that each DC advertises itself in the roles it should perform.

## Checked

Date: 2026-10-27. Documentation: Planning Global Catalog Server Placement (updated 2025-05), AD Forest Recovery
add/remove GC pages, Install-ADDSDomainController (Windows Server 2025 module page), nltest reference (Windows Server
2008 R2 archive page).
Confirmed: single-domain and multi-domain rules, the 100-user figure, exceptions and the infrastructure master rule,
port 3268, UGMC one-hop condition, the `repadmin /options +IS_GC/-IS_GC` commands and GUI path, `nltest /dsgetdc /gc`,
`-NoGlobalCatalog`.
Removed unconfirmed claims: port 3269 and UPN-logon detail, the `options` bit-flag script, the 8-hour cache refresh,
Directory Service event 1119 as the advertising signal, and any claim about what the Advertising test prints.

Method: documentation only; no commands were run.
