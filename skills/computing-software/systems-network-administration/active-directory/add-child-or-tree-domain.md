---
id: computing-software.systems-network-administration.active-directory.add-child-or-tree-domain
name: add-child-or-tree-domain
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-ds, install-addsdomain, child-domain, tree-domain, domain-controller-deployment, multi-domain, enterprise-admins, dns-delegation, parent-child-trust, dns-delegation-new-domain]
level: practitioner
status: docs-checked
description: "Add a child or new-tree domain with Install-ADDSDomain: when it is justified, Enterprise Admin rights, DNS delegation and post-checks."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/addsdeployment/install-addsdomain
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-a-new-windows-server-2012-active-directory-child-or-tree-domain--level-200-
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/install-active-directory-domain-services--level-100-
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/planning-global-catalog-server-placement
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Add a child or tree domain

**First question: should you?** The forest, not the domain, is the security boundary.
Extra domains add DCs, GPO duplication, trust paths and admin overhead. Valid reasons today:
a hard requirement for different domain-level settings that fine-grained password policies
cannot meet, a legal/political requirement for separate Domain Admins (which still does not
isolate from Enterprise Admins), or replication isolation for huge directories. Otherwise use
OUs.

## Child domain (shares the parent's namespace)
```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSDomain -NewDomainName emea -ParentDomainName ad.example.com `
  -DomainType ChildDomain -NewDomainNetbiosName EMEA -DomainMode WinThreshold `
  -InstallDns -CreateDnsDelegation -DnsDelegationCredential (Get-Credential) `
  -SiteName LON -Credential (Get-Credential EXAMPLE\entadmin) `
  -SafeModeAdministratorPassword (Read-Host -AsSecureString) -Force
```
Result: `emea.ad.example.com` as a new domain in the existing forest. Run `Test-ADDSDomainInstallation`
with the same arguments first; it runs the prerequisite checks only.

## Tree domain (new namespace, same forest)
```powershell
Install-ADDSDomain -NewDomainName fabrikam.example -ParentDomainName ad.example.com `
  -DomainType TreeDomain -NewDomainNetbiosName FABRIKAM -InstallDns ...
```
Clients need to resolve both namespaces: add conditional forwarders or forest-wide replicated
DNS data.

## Requirements and gotchas
- **Enterprise Admins** credential to install a new child domain or domain tree. `-Credential` is only
  needed when you are not already logged on as an Enterprise Admin.
- Connectivity to the **domain naming master** is needed to add or remove a domain, and to the RID master for any DC
  install.
- DNS delegation: with Windows DNS, creating the delegation for a new domain is automatic on the install
  wizard path; `-CreateDnsDelegation` and `-DnsDelegationCredential` set it and the credential for it. If
  the parent DNS is not Windows, create the delegation manually.
- The new domain gets its own Domain Admins, default GPOs and the three domain-level roles (RID master,
  infrastructure master, PDC emulator). Do not put the infrastructure master on a GC unless every DC in the
  domain is a GC (or the forest has one domain); making every DC a GC avoids the issue.
- Plan at least two DCs per domain.

## Verify
- [ ] `Get-ADDomain emea.ad.example.com -Server ad.example.com` returns the new domain.
- [ ] `nltest /domain_trusts /all_trusts` lists both domains.
- [ ] Users in each domain can resolve and authenticate to resources in the other.

## Checked

Date: 2026-10-27. Documentation: Install-ADDSDomain (Windows Server 2025 module page), the AD DS install and
child/tree domain pages, Planning operations master role placement, Planning global catalog placement
(MicrosoftDocs/windows-powershell-docs and windowsserverdocs, main branch).
Confirmed: parameter names and `-DomainType` values, `-DomainMode WinThreshold` as an accepted value,
Enterprise Admins requirement and the conditional `-Credential`, automatic DNS delegation on the wizard path, domain
naming master and RID master connectivity, infrastructure master and GC rule, Test- cmdlet behaviour.
Removed unconfirmed claims: the statement that the parent-child and tree-root trusts are created as two-way
transitive trusts, and the NS/glue wording for delegation.

Method: documentation only; no commands were run.
