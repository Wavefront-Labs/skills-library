---
id: computing-software.it-support-helpdesk.desktop-support.scan-to-email-and-scan-to-folder-setup
name: scan-to-email-and-scan-to-folder-setup
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, printer, printing, scan-to-email, scan-to-folder, smb-scan, smtp-relay, smtp-auth, direct-send, mfp, multifunction-printer]
level: practitioner
status: docs-checked
description: "Set up and fix MFP scan-to-email with Microsoft 365 (SMTP AUTH client submission, direct send, relay connector) and understand SMB signing for scan-to-folder."
sources:
  - "https://learn.microsoft.com/en-us/exchange/mail-flow-best-practices/how-to-set-up-a-multifunction-device-or-application-to-send-email-using-microsoft-365-or-office-365"
  - "https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/deprecation-of-basic-authentication-exchange-online"
  - "https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scan-to-email-and-scan-to-folder-setup

Goal: scanning works and keeps working after Microsoft or Windows security changes that routinely break MFPs.

## Scan to email with Microsoft 365: pick one
| Method | Settings on the MFP | Send outside org | Notes |
|---|---|---|---|
| **Client SMTP submission (SMTP AUTH)** | `smtp.office365.com`, port 587 (recommended) or 25, TLS/StartTLS on, a licensed mailbox's credentials | Yes | SMTP AUTH must be enabled for that mailbox; it is disabled for organizations created after January 2020 but can be enabled per mailbox |
| **Direct Send** | your MX endpoint (for example `contoso-com.mail.protection.outlook.com`), port 25, no authentication, TLS optional | No (recipients in your own domains) | not exempt from anti-spam; an SPF record entry is recommended |
| **SMTP relay** | MX endpoint, port 25, TLS/StartTLS on | Yes | needs an inbound connector authenticating by TLS certificate (recommended) or a static, unshared public IP; any address in an accepted domain can be the sender |

- Client SMTP submission needs TLS 1.2 or 1.3. A device defaulting to port 465 does not support the required
  TLS versions. Throttling for client submission: 10,000 recipients per day and 30 messages per minute.
- Basic authentication for client SMTP submission is scheduled for retirement, is not compatible with Security
  defaults in Microsoft Entra ID, and OAuth is recommended. Microsoft's alternatives: High Volume Email for internal
  recipients only, or Azure Communication Services Email for internal and external. Follow the latest Microsoft
  announcement for dates.
- If the device sends as a different address from the one it signs in with, the sign-in account needs Send As
  permission, or the message bounces with `5.7.60 SMTP; Client doesn't have permissions to send as this sender`.
- Relay connector: Exchange admin center > Mail flow > Connectors > Add a connector, From "Your organization's
  email server", To Office 365. Dynamic IP addresses are not supported.
- Test by sending from the device and confirming the recipient receives it.

## Scan to folder (SMB)
- Use a dedicated service account with only the rights it needs on the scan folder.
- SMB signing is enabled in all versions of Windows. Domain controllers require signing by default. Where a
  non-Microsoft file server or device cannot sign, the signing requirement may need relaxing: follow
  Microsoft's "Control SMB signing behavior" page rather than guessing registry values.
- SMB 2.x/3.x signing is controlled solely by whether it is required (`RequireSecuritySignature` 0 or 1 on client
  and server); `EnableSecuritySignature` is ignored except for SMB1.
- Windows 11 24H2 can audit third-party SMB servers or clients that do not support signing or encryption
  (Event Viewer SMBClient and SMBServer Audit logs).
- Prefer Kerberos; connecting by IP address or CNAME makes SMB fall back to NTLM.

## Scan to OneDrive/SharePoint
Vendor cloud connectors avoid SMTP and SMB; consider them for new deployments.

## Gotchas
- Service account password changes break every MFP silently; record where the password lives.

## Verify
A test scan arrives in an internal and (if required) external mailbox, and a scan lands in the folder, after a printer reboot.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Microsoft 365 device-email, basic-auth deprecation and SMB signing pages. Removed as not found on
those pages: SMTP error code meanings, the UNC path example, the 35 MB limit, "SMB1 is off" and NTLMv1 claims, and
the claim that Windows 11 24H2 / Server 2025 require signing by default (the page says only that signing is enabled
in all versions). Dropped the CompTIA landing-page source.
