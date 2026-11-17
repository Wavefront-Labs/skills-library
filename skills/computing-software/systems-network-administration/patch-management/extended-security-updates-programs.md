---
id: computing-software.systems-network-administration.patch-management.extended-security-updates-programs
name: extended-security-updates-programs
category: computing-software
field: systems-network-administration
product: patch-management
tags: [extended-security-updates, esu, azure-arc, ubuntu-pro, esm, rhel-els, eol-software]
level: practitioner
status: gated
description: "Keep end-of-life systems patched temporarily through extended security update programs: Microsoft ESU, Ubuntu Pro ESM and RHEL extended coverage, with limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/extended-security-updates-overview
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/prepare-extended-security-updates
  - https://ubuntu.com/pro
  - https://access.redhat.com/support/policy/updates/errata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended security updates programs

**Goal:** buy time to migrate off an end-of-life OS without running it unpatched.

## Microsoft ESU
- Covers Critical and Important security updates only for a fixed period after end of support; no new features or customer-requested non-security hotfixes. For Windows Server 2012 and 2012 R2 the ESU period is three years and ends 13 October 2026 (already past on 2026-10-27); check the ESU overview page for each product's dates.
- **Free** for servers hosted in Azure (the page includes the Azure Stack portfolio); available to purchase for servers not hosted in Azure.
- **Azure Arc**: Arc-enabled servers can enrol in ESU through the Azure portal or Azure Policy with a monthly pay-as-you-go subscription and keyless delivery. The Arc page also covers Windows Server 2016: configurable from 3 August 2026, billing from 13 January 2027.
- **Purchased product key**: after purchase you get a product key and install it on each applicable server; follow Microsoft's "How to get Extended Security Updates" steps for the exact activation commands (gated: unconfirmed, source is paywalled or blocked). Install the prerequisite licensing package and servicing stack update first, as the Arc documentation directs for Arc-enabled servers.
- Updates then flow through WSUS/ConfigMgr/Windows Update as normal.

## Ubuntu Pro ESM
```bash
sudo pro attach <token>
sudo pro enable esm-infra esm-apps
pro status
```
Per Canonical, Expanded Security Maintenance gives 10 years of fixes for critical, high and selected medium vulnerabilities across the whole Ubuntu archive (main and universe), and 15 years with the Legacy add-on. The `pro` client commands above are from memory of the Pro client and are not confirmed here (gated: unconfirmed, source is paywalled or blocked).

## RHEL extended coverage
Red Hat lists Extended Life-cycle Support (ELS) among legacy offerings for RHEL 6 and 7. From RHEL 9, extended support is unified as Extended Life Cycle Premium (ELCP, an add-on to RHEL Premium covering eligible minor releases up to 6 years from general availability), with Long-Life add-on term extensions for longer coverage. RHEL 8, 9 and 10 have a ten-year life cycle in the Full and Maintenance phases followed by an Extended Life Phase. Dates and terms are subject to change: confirm on the Red Hat life cycle page.

## Rules for using ESU
- ESU is a bridge with a migration plan and date, recorded as a risk with an owner.
- Plan for ESU cost to rise each year and compare it with migration cost.
- Applications on the box (SQL Server, Java, middleware) need their own support coverage.

## Verify
ESU-covered machines receive the latest monthly security update (check the KB or `pro status`) and appear in the migration plan with target dates.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn ESU overview for Windows Server 2012 and 2012 R2 (free in Azure, three years, ends 13 October 2026), Azure Arc ESU preparation page (keyless, monthly pay-as-you-go, Windows Server 2016 dates), Ubuntu Pro page (10 years, 15 with Legacy), Red Hat Enterprise Linux life cycle page (ELS legacy, ELCP, ten-year phases). The key activation commands and the Ubuntu `pro` client commands could not be confirmed and are gated.
Method: documentation only; no commands were run.
