---
id: computing-software.it-support-helpdesk.remote-support-tools.rdp-connection-failure-troubleshooting
name: rdp-connection-failure-troubleshooting
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rdp-troubleshooting, rdp, remote-desktop, nla, credssp, port-3389, mstsc, enable-remote-desktop]
level: practitioner
status: draft
description: "Work through RDP failures in order: reachability on 3389, service and firewall, NLA and CredSSP errors, user rights, Entra-joined sign-in format, and the logs that explain it."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/rdp-error-general-troubleshooting"
  - "https://learn.microsoft.com/en-us/windows/client-management/client-tools/connect-to-remote-aadj-pc"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rdp-connection-failure-troubleshooting

## Order of checks
1. **Reachability**: `Test-NetConnection <host> -Port 3389`. False with ping OK means
   firewall, service, or wrong port. Error 0x204 in mstsc is the same signal.
2. **Enabled**: on the target, `Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server' fDenyTSConnections`
   must be 0; `Get-Service TermService` running; firewall group "Remote Desktop" enabled
   (`Enable-NetFirewallRule -DisplayGroup "Remote Desktop"`).
3. **Listener**: `netstat -ano | findstr :3389` shows LISTENING; another app on the port or
   a changed `PortNumber` value explains silence.
4. **Rights**: "not authorized for remote login" means the user is not in Remote Desktop
   Users/Administrators, or "Deny log on through Remote Desktop Services" applies
   (check with `gpresult /h`).
5. **Authentication**:
   - NLA required but client cannot do CredSSP (old client, untrusted domain) -> fix client;
     only disable NLA temporarily.
   - "CredSSP encryption oracle remediation" -> one side is unpatched; patch it.
   - Entra-joined target: sign in as `AzureAD\user@domain.com`, and the client must be
     Entra joined/registered to the same tenant, or use the web account option in newer
     clients.
6. **Licensing** (RDS hosts): "no Remote Desktop License Servers available" after the
   120-day grace period means the licence server or CAL mode is not configured.

## Logs on the target
- `TerminalServices-RemoteConnectionManager/Operational` 1149: network auth succeeded.
- `TerminalServices-LocalSessionManager/Operational` 21/24/25: logon, disconnect, reconnect.
- Security log 4625 with logon type 10: failed RDP logon and the reason code.

## Gotchas
- Sleeping laptops do not answer; set power plans on machines meant for RDP.
- Mapped `.rdp` files keep an old hostname or gateway; open a fresh mstsc to rule them out.
- Using an IP instead of a name breaks Kerberos and forces NTLM, which may be blocked.

## Verify
A fresh mstsc connection by name reaches the desktop, event 1149 and 21 appear, and the
ticket records which layer was at fault.
