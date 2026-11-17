---
id: computing-software.networking-hardware-and-wireless.check-point.licensing-and-contracts-cplic
name: licensing-and-contracts-cplic
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cplic, licenses, contract-verification]
level: practitioner
status: draft
description: "View and install Check Point licenses with cplic, find the CK, attach licenses in SmartUpdate, and verify contracts."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Licensing and contracts with cplic

```
cplic print                         # licenses installed: features, expiry, signature
cplic print -x                      # include signature details
cplic put 10.1.1.1 -k -l <license string>   # (confirm syntax) per-gateway local license
cplic put -o ...                    # install local
cplic del <signature>
cplic check -p fw1 -v R81.20 -c     # check a feature
cplic contract -help
```
- Licences are tied to the gateway or management IP (central license) or the host (local license). The UserCenter (portal) issues licenses against the primary IP; after changing the IP, request a new licence there.
- In SmartConsole, **Gateways & Servers > select > Licenses/Contract** shows status; Eval licences last 15 days and "NG" contract status affects Updates (IPS, App Control).
- A central license installs on the management and pushes to gateways (SmartUpdate legacy; today mostly through the **Gateways & Servers > Licenses & Contracts** page).
- **Contract verification**: `cplic contract` (or the "Contracts" tab) checks whether updates and support contracts are valid; an expired contract disables downloads of updates (e.g. URL Filtering, AV) at the gateway.
- Capacity limits (e.g. number of cores or IPs) are enforced; a gateway with more cores than its license shows "Licensing: Limit exceeded" warnings (confirm).
- Gotcha: cluster members need individual licences, plus a licence for Management HA; with VSX licensing is per VS count.

Verify: `cplic print` shows `Expiration` in the future (or `never`); `cpstat -f licensing ...` and SmartConsole shows green; blades enabled in the gateway object appear in the `Features` list.
