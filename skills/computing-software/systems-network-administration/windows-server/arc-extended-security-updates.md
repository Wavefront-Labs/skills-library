---
id: computing-software.systems-network-administration.windows-server.arc-extended-security-updates
name: arc-extended-security-updates
category: computing-software
field: systems-network-administration
product: windows-server
tags: [azure-arc, arc-esu, extended-security-updates, windows-server-2012, licensing]
level: practitioner
status: docs-checked
description: "Enroll Windows Server 2012/2012 R2 and 2016 in Extended Security Updates through Azure Arc: agent versions, licences, linking, tagging exemptions and end dates."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/prepare-extended-security-updates
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/deliver-extended-security-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended Security Updates via Azure Arc

Windows Server 2012/2012 R2 reached end of support on 10 October 2023. The three-year ESU period ended on 13 October
2026 and the 13 October 2026 update was the last; at midnight UTC on 14 October 2026 Arc-enabled 2012 ESU licences
were deactivated. Windows Server 2016 reaches end of support on 12 January 2027; its ESUs (up to three years,
through 2030) can be configured in the portal from 3 August 2026 and Arc billing begins 13 January 2027. ESU through
Arc is keyless (no MAK activation) and billed monthly.

## Prerequisites
- Arc Connected Machine agent onboarded and connected: agent 1.34 or higher for Windows Server 2012 ESUs, 1.62 or
  higher for Windows Server 2016 ESUs.
- Download both the licensing package and the servicing stack update named in the Microsoft KB article (for Windows
  Server 2012: KB5031043) and install them.
- Standard and Datacenter editions are supported (2012 Storage is not). To buy ESUs you need Software Assurance
  (EA, EAS, EES, SCE or Open Value), or licensing via SPLA or a Server Subscription; you attest to this when creating
  a licence.
- Network: public endpoint, proxy, or private link/ExpressRoute; an ESU-only deployment can use the smaller endpoint
  subset listed on the prepare page (for example download.microsoft.com at install time, Entra ID endpoints).
- Do not deliver ESUs through Arc to VDI virtual machines: use MAK. AVS machines and VMs on Azure Local get free
  ESUs and should not enrol through Arc.

## Licences
Azure portal > Azure Arc > Licenses > Windows Server ESU licenses (or the 2016 offering) > Create:
- SKU Standard or Datacenter, number of cores, and for 2012 the core type (Physical or vCore). For 2016 you choose
  the core type later, when you enable ESUs on the machine.
- A licence can be created deactivated so it neither bills nor works until activated.

## Link servers
Eligible resources > select servers > Enable ESUs > choose core type and licence. At scale, use the built-in Azure
Policy definitions (enable ESU licence, and deny ESU licence creation or modification, both preview). A server can
receive ESUs once linked to an activated licence.

## Exemptions (2012/2012 R2)
Dev/Test (Visual Studio subscriptions) and Disaster Recovery (Software Assurance DR benefit) machines can use ESUs at
no extra cost only if you already have an activated production licence. Tag the licence and the non-production
servers with `ESU Usage` = `WS2012 VISUAL STUDIO DEV TEST`, `WS2012 DISASTER RECOVERY` or `WS2012 MULTIPURPOSE`
(licence only), then link the production licence to them. Never provision a licence only for these machines; you pay
for every provisioned core.

## Verify
- [ ] Portal shows the ESU status for the server; the policy "Extended Security Updates should be installed on
  Windows Server 2012 Arc machines" reports compliance for 2012 machines.
- [ ] Upgraded machines (to 2016 or later) are unlinked from the licence manually.
- [ ] Decommission or upgrade plan exists for 2012 machines, now past the end of ESU.

## Checked
Date 2026-10-27. Documentation: Azure Arc "prepare" and "deliver" Extended Security Updates pages. Confirmed: end
dates, agent minimums, licence fields, eligibility, exemption tag values, VDI and AVS notes, policy names.
Method: documentation only; no commands were run.
