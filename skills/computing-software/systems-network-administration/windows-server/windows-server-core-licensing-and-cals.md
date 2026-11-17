---
id: computing-software.systems-network-administration.windows-server.windows-server-core-licensing-and-cals
name: windows-server-core-licensing-and-cals
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, activation-licensing, core-licensing, windows-server-cals, datacenter-vs-standard, virtualization-rights]
level: practitioner
status: docs-checked
description: "Work out Windows Server licensing: core-based licences, Standard vs Datacenter virtualization rights, CALs, pay as you go via Azure Arc, Azure Hybrid Benefit."
sources:
  - https://www.microsoft.com/en-us/windows-server/pricing
  - https://learn.microsoft.com/en-us/windows-server/get-started/editions-comparison
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Server core-based licensing and CALs

Not legal advice: confirm with your licensing agreement, the Product Use Rights and your reseller.

## Core licensing
- Both Standard and Datacenter use a core-based licensing model (Windows Server 2025 pricing page).
- Published edition pricing is for 16-core licences. Look up the minimum cores per processor and per server, and the
  pack sizes, in the Product Use Rights and licensing site; count physical cores per host before buying.

## Standard vs Datacenter (Windows Server 2025)
| | Standard | Datacenter |
|---|---|---|
| Virtual OSEs / Hyper-V isolated containers | 2, plus one Hyper-V host per licence | unlimited, plus one Hyper-V host |
| Windows containers | unlimited Windows containers and up to two Hyper-V containers | unlimited Windows and Hyper-V containers |
| Storage Spaces Direct | no | yes |
| Storage Replica | 1 partnership and 1 resource group with a single 2 TB volume | unlimited |
Standard is aimed at physical or minimally virtualized environments, Datacenter at highly virtualized datacenters.

## Client access licenses
- A Windows Server CAL is required for every user or device accessing a server (both editions). See the Product Use
  Rights for exceptions.
- RDS CALs are additional for Remote Desktop users (see rds-licensing-and-cals).

## Cloud and subscription options
- Azure Hybrid Benefit: apply existing Windows Server licences with Software Assurance to Azure migrations.
- Pay as you go through Azure Arc: customers without unlimited virtualization can add machines for capacity bursts;
  billed per CPU core. Unlimited virtualization is not available through pay as you go for on-premises Arc-enabled
  servers. See the pricing page for current rates.

## Verify
- [ ] Inventory of physical cores per host (`Get-CimInstance Win32_Processor | Measure NumberOfCores -Sum`)
      matches licences bought.

## Checked
2026-11-09. Confirmed against the Windows Server pricing page and the Learn editions comparison: core-based model,
16-core pricing basis, VM and container rights, Storage Replica limits, Storage Spaces Direct by edition, CAL
requirement, Azure Hybrid Benefit with Software Assurance, Arc pay as you go and its unlimited-virtualization
exclusion. Removed unconfirmed figures: core minimums and pack sizes, break-even VM count, 180-day dual use,
90-day reassignment, BIOS core-disable rule, SDN row, price.
Method: documentation only; no commands were run.
