---
id: computing-software.cybersecurity-defensive.system-hardening.windows-rdp-hardening
name: windows-rdp-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [windows-hardening, rdp-hardening, nla, restricted-admin, remote-credential-guard, rdp-tls, remote-desktop-users]
level: practitioner
status: docs-checked
description: "Harden RDP on Windows hosts: NLA, TLS and certificates, who may log on, Restricted Admin and Remote Credential Guard, redirection limits, session timeouts, and firewall scoping."
sources: ["https://learn.microsoft.com/en-us/windows/security/identity-protection/remote-credential-guard", "https://www.cisecurity.org/benchmark/microsoft_windows_server", "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/remote-desktop-listener-certificate-configurations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows RDP hardening

(Publishing RDP to users remotely belongs behind RD Gateway or ZTNA; this is host-side configuration.)

## GPO settings (Computer > Admin Templates > Windows Components > Remote Desktop Services > RD Session Host)
- **Security**:
  - Require user authentication for remote connections by using Network Level Authentication: Enabled.
  - Server authentication certificate template: issue RDP certificates from your PKI so clients can verify
    the host (no more self-signed warnings that train users to click through).
- **Session Time Limits** and **Device and Resource Redirection**: set idle and disconnected session limits, and disable redirection types you do not need.
- Do not allow passwords to be saved (client side).

## Who can log on
Use the User Rights Assignment for allowing and denying log on through Remote Desktop Services: allow Administrators plus a specific per-server group; deny guests, local accounts on domain members, service accounts, and Tier 0 accounts on lower-tier hosts.

## Protect admin credentials
- **Remote Credential Guard** (GPO "Restrict delegation of credentials to remote servers"):
  credentials stay on the client; Kerberos requests are redirected back. Requires Kerberos, Windows 10 1607+/2016+.
- **Restricted Admin mode**: no credentials sent at all; the session uses the
  machine identity for outbound network access. Enable it per the Remote Credential Guard page.
  Caveat: Restricted Admin enables pass-the-hash to RDP; Remote Credential Guard is preferred.

## Network
- Windows Firewall: allow TCP/UDP 3389 only from jump hosts/PAWs/management subnets.
- Change of port is obscurity, not security.
- Disable RDP entirely where unused.

## Logging
Forward Windows logon events and the Remote Desktop Services operational logs to the SIEM.

## Gotchas
- NLA requires CredSSP; keep CredSSP patched.

## Verify
Connecting without NLA fails; from a non-management subnet the port is filtered; Remote Credential Guard
works for admins; a member of no RDP group is denied.

## Checked

Date: 2026-10-28

- Confirmed (Remote Credential Guard page, RDP listener certificate page): Remote Credential Guard redirects Kerberos requests back to the client so credentials are not exposed on a compromised target; Restricted Admin mode exists with the CredSSP restricted remote administration policy; RDP listener certificate configuration.
- Removed (not found in the fetched pages): encryption level and security layer values, session time figures, redirection list, quoted user-rights policy names, mstsc flags and registry values, event IDs, Encryption Oracle Remediation value, Entra RDP note. CIS benchmark source is registration-gated.
Method: documentation only; no commands were run.
