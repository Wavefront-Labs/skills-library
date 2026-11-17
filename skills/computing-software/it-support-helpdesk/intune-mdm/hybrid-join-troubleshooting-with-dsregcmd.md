---
id: computing-software.it-support-helpdesk.intune-mdm.hybrid-join-troubleshooting-with-dsregcmd
name: hybrid-join-troubleshooting-with-dsregcmd
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, hybrid-join-troubleshooting, dsregcmd, hybrid-azure-ad-join, prt, entra-connect, scp, windows-enrollment]
level: advanced
status: docs-checked
description: "Fix Microsoft Entra hybrid join: reading dsregcmd /status, join phase and error codes, SCP and proxy checks, sync-join Pending devices, and event logs."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/devices/troubleshoot-hybrid-join-windows-current"
  - "https://learn.microsoft.com/en-us/entra/identity/devices/how-to-hybrid-join-verify"
  - "https://learn.microsoft.com/en-us/entra/identity/devices/how-to-hybrid-join"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hybrid-join-troubleshooting-with-dsregcmd

Hybrid joined = domain joined to on-premises AD and joined to Microsoft Entra ID.
Hybrid join underpins device-based Conditional Access, enterprise state roaming
and Windows Hello for Business, and the GPO-based Intune auto-enrollment needs
it (see gpo-triggered-mdm-enrollment-for-hybrid-devices).

## Step 1 and 2: read `dsregcmd /status`
Run in an elevated Command Prompt. Check:
| Field | Expected |
|---|---|
| DomainJoined | YES (NO means hybrid join is impossible) |
| WorkplaceJoined | NO (YES = a work account was added before hybrid join finished; ignored on Windows 10 1607+) |
| AzureAdJoined | YES (NO = the join has not finished yet) |
| AzureAdPrt (User State) | YES for SSO |

## Step 3: find the phase and error code
Windows 10 1803 and later: Diagnostic Data > "Previous Registration" shows
Registration Type (sync or federated), Error Phase, Client ErrorCode, Server
ErrorCode, Server Message, Https Status. It appears only when the device is
domain joined but not hybrid joined. The Diagnostic Data tests (AD Connectivity,
AD Configuration, DRS Discovery, DRS Connectivity, Token acquisition, Fallback
to Sync-Join) show which stage fails; the AD Configuration test reads the SCP.
Older builds: Event Viewer > Applications and Services Logs > Microsoft >
Windows > User Device Registration; events 304, 305, 307 (phase), 201
(discovery), 305 (authentication), 204 (join), 220 (computer object access).

## Step 4: causes by phase
**Precheck**: no line of sight to a domain controller; the device must be on the
internal network or a VPN with that line of sight.

**Discover**:
- SCP object misconfigured or unreadable: you need a valid SCP in the device's
  forest pointing at a verified domain in Entra.
  `0x801c001d` DSREG_AUTOJOIN_ADCONFIG_READ_FAILED.
- Cannot reach https://enterpriseregistration.windows.net in system context
  (`0x801c001f` timeout; `0x801c0021` generic discovery failure, look at the
  suberror e.g. `0x80072ee2` timeout, `0x80072efd` cannot connect,
  `0x80072f8f` proxy modified response).
- Cannot reach https://login.microsoftonline.com in system context for realm
  discovery (`0x801c003d`).
- `0x801c003a` tenant not found: SCP has the wrong tenant ID or the tenant has
  no active subscription. `0x801c0025` HTTP 503 from DRS: retry later.
- `0x8007000d`: proxy returned an HTML authorization page; the system context
  must authenticate to the proxy silently.

**Authentication** (federated domains only): the device gets a token from the
federation service by integrated Windows auth to an active WS-Trust endpoint.
Errors `0xcaa9...` / `0xcaa8...` cover non-WS-Trust providers, bad MEX XML,
network timeouts to login.microsoftonline.com and server faults; check
federation server settings and event 305.

**Join**:
- Sync-join: `0x801c03f2` DirectoryError "The device object by the given id isn't
  found" and AuthenticationError "verification of the target computer's SID" are
  expected until Microsoft Entra Connect syncs the device object; the next
  attempt after sync succeeds. "Tenant UUID not found" (AADSTS90002) means a
  wrong SCP tenant ID. A throttle message means wait 300 seconds.
- TPM: `0x80090016` NTE_BAD_KEYSET (TPM cleared or bad sysprep image; do not
  clear the TPM; the sysprep source must not itself be joined or registered);
  `0x80290407` and `0x80280036` (disable TPM; 1809+ detects TPM failures and joins
  without it); `0x80090031` TPM locked out (transient).
- `0x801c001d` with event 220: Windows cannot access the computer object in AD
  (errors 1312, 1317 point to AD replication problems).

## Network
Allow system-context access (not user proxy settings) to
https://enterpriseregistration.windows.net, https://login.microsoftonline.com
and https://device.login.microsoftonline.com. Configure WPAD or, on Windows 10
1709+, WinHTTP proxy by GPO. Exclude the registration and device login URLs from
TLS break-and-inspect or device registration and device-based Conditional Access
break.

## Pending devices
In the Entra device list a Registered state of Pending means hybrid join has not
completed (in federated setups only if registration failed and Entra Connect
syncs devices); wait for a sync cycle. The verify page has PowerShell to count and
list Pending hybrid devices.

## Verify
`dsregcmd /status` shows AzureAdJoined YES and AzureAdPrt YES, and the Entra
device shows join type Microsoft Entra hybrid joined with Registered populated.

## Checked
2026-11-08. Confirmed against the Microsoft Learn pages Troubleshoot Microsoft
Entra hybrid joined devices, Verify hybrid join (Pending state) and How to plan
hybrid join (proxy and endpoint requirements): field table, phases, error code
tables, sync-join behaviour, network guidance. Removed as unconfirmed: the
Automatic-Device-Join task path, userCertificate flow, a 30 minute sync figure,
0x80070774, stale or cloned image cleanup steps, dsregcmd /leave rejoin recipe,
Start-ADSyncSyncCycle, and the dsregcmd /status /debug switch.
Method: documentation only; no commands were run.
