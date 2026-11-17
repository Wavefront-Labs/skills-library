---
id: computing-software.systems-network-administration.active-directory.entra-domain-services-join
name: entra-domain-services-join
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, domain-join, entra-domain-services, aadds, managed-domain, aad-dc-administrators, vnet-dns, password-hash-sync, azure]
level: practitioner
status: docs-checked
description: "Join Windows Server VMs to Microsoft Entra Domain Services: VNet DNS, AAD DC Administrators, password hash prerequisites, OU and GPO limits of the managed domain."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/domain-services/join-windows-vm
  - https://learn.microsoft.com/en-us/entra/identity/domain-services/administration-concepts
  - https://learn.microsoft.com/en-us/entra/identity/domain-services/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Join servers to Microsoft Entra Domain Services

**What it is:** a managed AD DS domain (two DCs run by Microsoft) populated one-way from Entra ID. You get Kerberos, NTLM,
LDAP and Group Policy for lift-and-shift apps without running DCs, but you cannot sign in to the DCs. You manage it from a
management VM joined to the domain with the usual AD tools (ADAC, DNS and Group Policy snap-ins).

## Prerequisites
- Managed domain deployed into a virtual network; VMs in that network (or peered) and the network's DNS servers pointed at
  the managed domain so the VM can find it. The DNS name and virtual network cannot be changed after creation, the domain
  name prefix is limited to 15 characters, and the domain cannot move subscription, resource group or region.
- A user account in the managed domain. Password hashes for NTLM and Kerberos are not generated until you enable Domain
  Services: cloud-only users must change their password once; synced users need Entra Connect password hash sync enabled
  (it then also syncs the legacy hashes the managed domain needs).
- **Entra Cloud Sync is not supported with Domain Services**: sync on-premises users with Entra Connect Sync.
- Do not install Entra Connect inside the managed domain.

## Join
The process is the same as joining a regular AD DS domain. Use a domain account that exists in the managed domain and
works through the VNet (the Microsoft tutorial uses Azure Bastion to reach the VM):
```powershell
Add-Computer -DomainName <MANAGED_DOMAIN_FQDN> -Credential (Get-Credential) -Restart
```
If the join fails, see the Domain Services domain-join troubleshooting page.

## What differs from self-managed AD
- Sync is one-way from Entra ID; accounts you create directly in the managed domain are not synced back.
- A default password policy covers lockout, maximum age and complexity; you can create custom password policies for groups
  of users. Some settings apply only to users created in the managed domain.
- Forest trusts are supported (one-way or two-way, with incoming and outgoing directions as documented).
- An Entra-joined Azure VM (the "Login with Microsoft Entra ID" extension) cannot also be joined to Domain Services.

## Gotchas
- Large tenants take time to sync; new users are not instantly usable.
- Backups and sync frequency depend on the SKU (see the SKU table); restores go through Microsoft support.

## Verify
- [ ] `nltest /dsgetdc:<MANAGED_DOMAIN_FQDN>` on the VM returns a managed DC.
- [ ] A test Entra user (after the password hash is generated) can sign in to the server.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Domain Services join tutorial, administration concepts, create
instance tutorial, synchronization and the VM Entra sign-in page. Confirmed one-way sync, password hash generation rules,
the Cloud Sync exclusion, DNS and immutability notes, SKU-based backup and the Entra VM sign-in conflict. Removed the
`AAD DC Administrators` rights, the `AADDC Computers` OU path, the gMSA, LDAPS and schema statements and the NSG
advice, which the cited pages do not state.
Method: documentation only; no commands were run.
