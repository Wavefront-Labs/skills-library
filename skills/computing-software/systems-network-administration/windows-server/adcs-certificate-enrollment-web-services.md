---
id: computing-software.systems-network-administration.windows-server.adcs-certificate-enrollment-web-services
name: adcs-certificate-enrollment-web-services
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, certificate-enrollment-web-services, cep, ces, cross-forest-enrollment]
level: advanced
status: docs-checked
description: "Deploy Certificate Enrollment Policy and Enrollment Web Services (CEP/CES) for enrollment over HTTPS from untrusted forests, workgroup machines or the internet."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcsenrollmentpolicywebservice
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcsenrollmentwebservice
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-certificate-enrollment-web-service
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/configure-certificate-enrollment-policy-web-service
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Certificate Enrollment Web Services (CEP and CES)

Normal autoenrollment uses LDAP + DCOM/RPC to the CA, which only works for domain members with line of sight.
**CEP** (policy: which templates) and **CES** (enrollment: submit requests) expose the same over HTTPS.

## Use cases
- Machines in another forest without a two-way trust, or in a DMZ/workgroup.
- Clients outside the network (with username/password or certificate auth).
- Avoid opening RPC/DCOM ports to the CA.

## Install (member server with IIS, HTTPS cert)
```powershell
Install-WindowsFeature ADCS-Enroll-Web-Pol,ADCS-Enroll-Web-Svc -IncludeManagementTools
Install-AdcsEnrollmentPolicyWebService -AuthenticationType Kerberos -SSLCertThumbprint <thumb>
Install-AdcsEnrollmentWebService -CAConfig 'CA01.ad.example.com\Example Issuing CA' -AuthenticationType Kerberos `
  -SSLCertThumbprint <thumb> -ServiceAccountName AD\svc-ces -ServiceAccountPassword (Read-Host -AsSecureString)
```
`-AuthenticationType` accepts `Kerberos`, `UserName` or `Certificate` (certificate authentication is used for
renewal with an existing certificate). Install one instance per auth type you need; the IIS virtual application
name follows the choice (for example `ADPolicyProvider_CEP_Kerberos`, `ADPolicyProvider_CEP_UsernamePassword`,
`KeyBasedRenewal_ADPolicyProvider_CEP_Certificate`).

- When CES runs on a different computer from the CA and issues new certificates, the CES account (or the computer
  account, if the application pool identity is used) must be trusted for delegation to the CA's host and RPCSS
  services; an SPN is required for a domain account. Renewal-only mode avoids delegation.
- Associate the CES URI with the CA so CEP returns it:
  `certutil -config <CAHost>\<CAName> -enrollmentServerURL <URL> Kerberos` (authentication types for this switch:
  `Kerberos`, `UserName`, `ClientCertificate`, `Anonymous`; modifiers `AllowRenewalsOnly`, `AllowKeyBasedRenewal`).

## Client config
GPO: Computer/User > Policies > Windows Settings > Security Settings > Public Key Policies > **Certificate Services
Client - Certificate Enrollment Policy**: add the CEP URI that you copied from the installed policy service's virtual application, and the auth type.

## Verify
- [ ] A client using only the CEP/CES URI (no LDAP to the CA) enrols and renews a certificate.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: `-AuthenticationType` values (Kerberos, UserName, Certificate) for both Install-AdcsEnrollmentPolicyWebService and Install-AdcsEnrollmentWebService in the windows-powershell-docs reference; virtual application names and delegation requirements (host and RPCSS, constrained delegation, renewal-only mode) in the configure Certificate Enrollment Web Service pages; the certutil -enrollmentServerURL syntax and modifiers in the certutil reference; the Group Policy path Computer Configuration > Windows Settings > Security Settings > Public Key Policies > Certificate Services Client - Certificate Enrollment Policy. Removed as unconfirmed: the msPKI-Enrollment-Servers attribute name, the full service.svc URI and the certutil -urlcache workgroup step. Fixed: UsernamePassword is a virtual application name suffix, not an -AuthenticationType value.

Method: documentation only; no commands were run.
