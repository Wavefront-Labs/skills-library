---
id: computing-software.cybersecurity-defensive.nessus.authenticated-scanning
name: authenticated-scanning
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, tenable, tenable-io, tenable-vulnerability-management, authenticated-scanning, credentialed-scan, vulnerability-scanning, scan-policy, plugin-19506, plugin-21745, plugin-141118, smb, wmi, ssh, sudo, local-checks, qualys, openvas, greenbone, nessus-agent, privileged-account, vulnerability-management]
level: practitioner
status: docs-checked
description: "Run credentialed Nessus scans on Windows and Linux, prove authentication actually worked via plugin output, scan safely, and triage results."
sources: ["https://docs.tenable.com/nessus/Content/NessusCredentialedChecks.htm", "https://docs.tenable.com/nessus/Content/CredentialedChecksOnWindows.htm", "https://docs.tenable.com/nessus/Content/CredentialedChecksOnLinux.htm", "https://www.tenable.com/plugins/nessus/19506", "https://www.tenable.com/plugins/nessus/117887", "https://www.tenable.com/plugins/nessus/21745", "https://www.tenable.com/plugins/nessus/141118", "https://www.tenable.com/plugins/nessus/104410", "https://www.tenable.com/plugins/nessus/110385"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authenticated scanning with Nessus: see the real patch state, prove you did

**Goal:** scan hosts with credentials so Nessus performs local checks (patch levels, configuration) instead of relying on banners, and confirm every host actually authenticated, because a silent auth failure looks like a clean host.

## 1. Prepare scan accounts
- **Windows:** the account needs privileges to read the files and registry entries involved, which usually means administrative privileges. Without an administrator account Nessus can at best do registry-based patch checks; with one it checks the DLL versions on the host, which Tenable describes as considerably more accurate. Only Domain Administrator accounts can scan Domain Controllers.
  - Prerequisites per Tenable: no Windows security policy, local policy (for example "Deny access to this computer from the network"), antivirus/endpoint rule or IPS/IDS blocking the checks; SMB and WMI reachable through the host firewall (File and Printer Sharing on TCP 139 and 445); Remote Registry enabled (disabled by default; the scan policy option *Start the Remote Registry service during the scan* makes Nessus try to start it, which needs administrative credentials); the default administrative shares IPC$, ADMIN$ and C$ present.
  - For local (non-domain) accounts, set the network-access sharing model to *Classic - local users authenticate as themselves*, and either turn UAC off or add the registry DWORD `LocalAccountTokenFilterPolicy` = 1 under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\system` (Tenable's recommended alternative to disabling UAC).
- **Linux:** the SSH user must be able to run any command; Tenable says full compliance checks need root and recommends SSH keys over passwords. Non-privileged access can still do basic checks such as patch levels. Elevation by sudo or su is supported. Generate keys with `ssh-keygen -t ed25519`; for older SSH servers that reject ed25519/ecdsa, Tenable suggests `ssh-keygen -t rsa -b 4096`. The target's shell `PS1` must be four or more characters or scans can be drastically slower.
- Keep credentials in Nessus/Tenable's credential store or a vault integration, not in shared policy exports (Tenable also publishes guidance on protecting Windows scanning credentials).

## 2. Build the scan policy
Add the Windows and SSH credentials to the policy. Tune discovery and performance settings for your network and agree a scan window; on fragile devices see the fragile-device skill in this folder.

## 3. Prove authentication succeeded
After every scan, check these plugins (names confirmed on tenable.com/plugins):
| Plugin | Meaning |
|---|---|
| 19506 Nessus Scan Information | Reports, among other things, whether credentialed checks were possible |
| 141118 Target Credential Status by Authentication Protocol - Valid Credentials Provided | Valid credentials for an available protocol (reported per protocol, so SSH may succeed while SMB fails) |
| 117887 OS Security Patch Assessment Available | Nessus logged in and enumerated OS security patch levels |
| 21745 OS Security Patch Assessment Failed | Credentials did not allow login, or another problem occurred |
| 104410 Target Credential Status by Authentication Protocol - Failure for Provided Credentials | Could not log in with the provided credentials |
| 110385 Target Credential Issues by Authentication Protocol - Insufficient Privilege | Logged in, but credentials not privileged enough for all checks |
Report the share of in-scope hosts with 117887 as an authentication success rate beside vulnerability counts.

## 4. Triage results
1. Group findings by solution so one fix closes many findings.
2. Check plugin output paths before ticketing.
3. Mark remote-only findings on hosts with failed authentication; they are not comparable to credentialed ones.
4. Re-scan after remediation to close tickets.

## Gotchas
- A wrong password with account lockout policies can lock accounts across many hosts; test on a few hosts first.
- Firewalls that allow SMB only from management subnets mean the scanner must sit in those subnets.
- A noisy login script or custom shell for the scan user can confuse command parsing; keep it plain.

## Verify
- [ ] Scan account exists per platform with the least privilege that still works.
- [ ] 117887 (or the credentialed-checks indication in 19506) present on every in-scope host.
- [ ] Hosts with 21745, 104410 or 110385 have a ticket to fix access.
- [ ] Remediated findings confirmed by re-scan.

Related: computing-software.cybersecurity-defensive.vulnerability-management.risk-based-prioritisation

## Checked
2026-11-02. Confirmed from Tenable docs (Credentialed Checks, Credentialed Checks on Windows, Credentialed Checks on Linux) and the tenable.com plugin pages for 19506, 117887, 21745, 141118, 104410 and 110385. Removed: unsourced Windows account details (GPO Restricted Groups/LAPS), "Safe Checks"/thorough-test/port-scope/parallelism advice, numeric performance figures, the 24786/26917 plugin rows, the "Credentialed checks : yes" string, VPR/EPSS/KEV advice, Qualys/OpenVAS/agent comparison, NTLM/requiretty gotchas.

Method: documentation only; no commands were run.
