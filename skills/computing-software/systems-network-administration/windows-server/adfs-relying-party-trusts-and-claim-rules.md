---
id: computing-software.systems-network-administration.windows-server.adfs-relying-party-trusts-and-claim-rules
name: adfs-relying-party-trusts-and-claim-rules
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-fs, adfs, relying-party-trust, claim-rules, add-adfsrelyingpartytrust, issuance-transform-rules, access-control-policy, saml]
level: advanced
status: docs-checked
description: "Add AD FS relying party trusts from metadata or manually, write issuance transform claim rules in the claim language, and apply access control policies."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/operations/create-a-relying-party-trust
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/technical-reference/the-role-of-the-claim-rule-language
  - https://learn.microsoft.com/en-us/powershell/module/adfs/add-adfsrelyingpartytrust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relying party trusts and claim rules

## Create the trust
```powershell
Add-AdfsRelyingPartyTrust -Name 'Payroll SaaS' -MetadataUrl 'https://payroll.example.net/saml/metadata' `
  -AccessControlPolicyName '<template name from Get-AdfsAccessControlPolicy>'
# manual (no metadata)
Add-AdfsRelyingPartyTrust -Name 'Legacy App' -Identifier 'urn:legacyapp' `
  -SamlEndpoint (New-AdfsSamlEndpoint -Binding POST -Protocol SAMLAssertionConsumer -Uri 'https://legacy.example.com/acs') `
  -AccessControlPolicyName '<template name from Get-AdfsAccessControlPolicy>'
```
Metadata-based trusts can monitor and auto-update from the partner's metadata (`-MonitoringEnabled $true -AutoUpdateEnabled $true`, with `-MetadataUrl`).

## Claim rules (issuance transform)
Rule language: condition => issue.
```
@RuleName = "LDAP attributes"
c:[Type == "http://schemas.microsoft.com/ws/2008/06/identity/claims/windowsaccountname", Issuer == "AD AUTHORITY"]
 => issue(store = "Active Directory",
    types = ("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
             "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname"),
    query = ";mail,givenName;{0}", param = c.Value);

@RuleName = "Role from group"
c:[Type == "http://schemas.microsoft.com/ws/2008/06/identity/claims/groupsid", Value == "S-1-5-21-...-1234"]
 => issue(Type = "http://schemas.microsoft.com/ws/2008/06/identity/claims/role", Value = "PayrollAdmin");
```
Apply:
```powershell
Set-AdfsRelyingPartyTrust -TargetName 'Payroll SaaS' -IssuanceTransformRulesFile '<vol>:\rules\payroll.txt'
```
`add(...)` instead of `issue(...)` adds the claim to the input claims for later rules
without sending it to the relying party. To send the email address as the Name ID, use the **Transform an Incoming Claim**
rule template and choose the outgoing name ID format the SP expects.

## Access control
Access control policies (AD FS 2016+) replace issuance authorization rules: permit specific
groups, require MFA from extranet, by device. List templates with `Get-AdfsAccessControlPolicy`.

## Troubleshoot
- The AD FS Admin log shows request errors; with auditing on (`Set-AdfsProperties -AuditLevel`), events 1200 and 1201 record
  application token success and failure.
- NameID format mismatches are the most common SaaS failure: compare with the SP's
  metadata and the SAML response (SAML-tracer).
- Signature algorithm and encryption certificate expectations differ per SP; see `-SignatureAlgorithm` on `Set-AdfsRelyingPartyTrust`.

## Verify
- [ ] Test login issues the expected claims (check with the SP's debug page or SAML-tracer).

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main and windows-powershell-docs (winserver2025-ps ADFS and WebApplicationProxy modules), entra-docs main.
Confirmed from the winserver2025-ps ADFS reference (Add-/Set-AdfsRelyingPartyTrust parameters -MetadataUrl, -MonitoringEnabled, -AutoUpdateEnabled, -Identifier, -SamlEndpoint,
-AccessControlPolicyName, -IssuanceTransformRulesFile, -SignatureAlgorithm; New-AdfsSamlEndpoint -Binding POST and -Protocol SAMLAssertionConsumer),
The-Role-of-the-Claim-Rule-Language (issue versus add, attribute-store issuance) and ad-fs-tshoot-logging (events 1200 and 1201, audit levels).
Removed the custom NameID rule with a claim property URI, the event 364 and 1000-series statements and the SHA-1 remark, which no page confirms.
Method: documentation only; no commands were run.
