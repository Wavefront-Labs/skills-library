---
id: computing-software.systems-network-administration.active-directory.try-next-closest-site-and-dc-locator-policy
name: try-next-closest-site-and-dc-locator-policy
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-sites, try-next-closest-site, dc-locator, site-coverage]
level: advanced
status: docs-checked
description: "Tune DC locator with Group Policy: Try Next Closest Site, site coverage, force rediscovery and SRV priority so clients fail over to the nearest site, not any DC."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/enabling-clients-to-locate-the-next-closest-domain-controller
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-r2-and-2008/cc772592(v=ws.10)
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/dc-locator
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Try Next Closest Site and DC locator policy

When every DC in a client's site is down, the default locator returns **any** DC in the domain, maybe on another
continent. Try Next Closest Site makes it pick the next site by site link cost.

## Enable
GPO: Computer Configuration > Administrative Templates > System > Net Logon > DC Locator DNS Records >
**Try Next Closest Site** = Enabled. Link it at domain level for all members, or edit the Default Domain Policy. The
setting is off by default.

Per-computer registry equivalent (DWORD): `HKLM\Software\Policies\Microsoft\Netlogon\Parameters\Try Next Closest Site` = 1
(a GPO is recommended instead because it is more consistent).

## Requirements
- Site link costs must reflect real network distance; the locator sums link costs to rank sites.
- Clients Windows Vista or later or Windows Server 2008 or later, and DCs Windows Server 2008 or later; a response from an older DC gives the default behaviour.
- By default, sites that contain an RODC are not considered when the next closest site is chosen.
- It works with automatic site coverage: if the next closest site has no DC, the locator uses the DC that covers that site.

## Related settings
The other DC locator policies live in the same Group Policy folder (DC Locator DNS Records): site coverage, SRV priority
and weight, and records a DC does not register. Check each setting's Explain text in your Windows version before using it.

## Test
```cmd
nltest /dsgetdc:corp.example.com /writable /try_next_closest_site
nltest /dsgetdc:corp.example.com /force
```
Stop Netlogon on the local DCs in a lab and check that the result is a DC in the expected next-closest site.

## Verify
- [ ] GPO applied (`gpresult /h`), Netlogon parameters show TryNextClosestSite.
- [ ] Failover test result recorded per site.

## Checked
2026-10-27, against the windowsserverdocs page "Enabling Clients to Locate the Next Closest Domain Controller" and the Learn page "Enable Clients to Locate a Domain Controller in the Next Closest Site" (Windows Server 2008/2008 R2). Confirmed: setting is off by default; algorithm (own site, next closest by site-link cost, then any DC); works with automatic site coverage; RODC sites not considered; OS requirements; GPO location (DC Locator DNS Records); registry value name `Try Next Closest Site` under HKLM\Software\Policies\Microsoft\Netlogon\Parameters; `NLTEST /DSGETDC: domain /WRITABLE /TRY_NEXT_CLOSEST_SITE` verification; `nltest /dsgetdc ... /force`. Removed as unconfirmed: the table of other locator settings with defaults (including the 12-hour rediscovery figure), nltest /dsgetsite and /site:, the CLOSE_SITE flag remark. Corrected: the registry value name contains spaces.

Method: documentation only; no commands were run.
