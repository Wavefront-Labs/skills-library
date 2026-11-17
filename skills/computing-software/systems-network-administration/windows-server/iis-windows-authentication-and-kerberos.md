---
id: computing-software.systems-network-administration.windows-server.iis-windows-authentication-and-kerberos
name: iis-windows-authentication-and-kerberos
category: computing-software
field: systems-network-administration
product: windows-server
tags: [iis, iis-windows-authentication, kerberos, setspn, gmsa-app-pool]
level: advanced
status: docs-checked
description: "Configure IIS Windows authentication with Kerberos: Negotiate providers, kernel-mode auth and useAppPoolCredentials, SPNs for custom host names and delegation."
sources:
  - https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/authentication/windowsauthentication/
  - https://learn.microsoft.com/en-us/iis/configuration/system.webserver/security/authentication/windowsauthentication/providers/
  - https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/iis/www-authentication-authorization/troubleshoot-kerberos-failures-ie
  - https://learn.microsoft.com/en-us/archive/blogs/webtopics/service-principal-name-spn-checklist-for-kerberos-authentication-with-iis-7-07-5
  - https://learn.microsoft.com/en-us/archive/blogs/amol/understanding-kernel-mode-authentication-in-iis-7
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IIS Windows authentication and Kerberos

## Enable
Install the Windows Authentication role service (it is not part of the default IIS installation), disable Anonymous
authentication for the site or application, then enable Windows authentication:
```powershell
Set-WebConfigurationProperty -PSPath IIS:\ -Location 'Default Web Site/app' -Filter /system.webServer/security/authentication/windowsAuthentication -Name enabled -Value true
Set-WebConfigurationProperty -PSPath IIS:\ -Location 'Default Web Site/app' -Filter /system.webServer/security/authentication/anonymousAuthentication -Name enabled -Value false
```
The `providers` list holds two entries by default, Negotiate (tries Kerberos if available) and NTLM, and cannot be
extended. Provider order is the order of the list; removing Negotiate leaves NTLM only. The `useKernelMode`
attribute turns kernel-mode authentication on or off.

## SPNs: whose key decrypts the ticket?
- With **kernel-mode authentication** (on by default in IIS 7 and later) Kerberos tickets are decrypted with the
  **machine account** key, so the SPN belongs on the computer account. A custom pool identity with its own SPN then
  fails unless you set `useAppPoolCredentials="true"` (decrypts with the pool identity and keeps kernel mode) or
  turn kernel mode off (not recommended for performance).
- Site on the server's own name with the default pool identity: the computer's HOST SPNs already cover it.
- Custom host name on one server: `setspn -S HTTP/app.corp.example.com SRV01$`.
- Farm behind a load balancer: run all pools as the same domain account or gMSA, register `HTTP/app.corp.example.com`
  on that account and set `useAppPoolCredentials`:
```powershell
Set-WebConfigurationProperty -PSPath IIS:\ -Location 'Default Web Site/app' -Filter /system.webServer/security/authentication/windowsAuthentication -Name useAppPoolCredentials -Value true
```
Duplicate SPNs (the same HTTP/name on two accounts) cause KRB_AP_ERR_MODIFIED because the ticket may be encrypted
with either account's password; find them with `setspn -X`.

## Browsers
For automatic logon the site must be in a zone the browser trusts for integrated authentication (Local Intranet or
a policy allow list). See Microsoft's Kerberos failure troubleshooting page for the checks.

## Double hop (IIS to SQL/file share as the user)
Needs Kerberos delegation (constrained delegation or resource-based constrained delegation) from the pool account to
the back-end SPN.

## Diagnose
`klist` on the client shows the `HTTP/<host>` ticket; the IIS log username field is filled. 401.1 means logon failed (bad credentials) and 401.2 a
server authentication configuration problem.

## Verify
- [ ] Client gets a Kerberos ticket for the site SPN; logon type shows Kerberos.

## Checked
Date 2026-10-27. Documentation: IIS windowsAuthentication and providers reference pages, Microsoft Kerberos
troubleshooting for IIS and two Microsoft blog archive articles on kernel-mode authentication and the SPN checklist
(archived blog material, not formal product documentation). Confirmed: provider list, useKernelMode, machine-account
decryption, useAppPoolCredentials purpose, duplicate SPN symptom, 401.1/401.2 meanings. Security-log event details are not covered.
Method: documentation only; no commands were run.
