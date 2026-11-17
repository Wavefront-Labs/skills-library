---
id: computing-software.systems-network-administration.active-directory.kerberos-authentication-troubleshooting
name: kerberos-authentication-troubleshooting
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, kerberos, authentication, troubleshooting, klist, setspn, spn, duplicate-spn, kdc, tgt, service-ticket, krb5, keytab, ktpass, clock-skew, w32time, time-sync, kerberos-errors, krb-ap-err-modified, kdc-err-s-principal-unknown, kdc-err-etype-nosupp, ntlm-fallback, event-4768, event-4769, event-4771, kerberos-delegation, double-hop, token-size, maxtokensize, secure-channel, http-sso, iis-kernel-mode-auth, linux-kerberos, kinit]
level: advanced
status: docs-checked
description: "Troubleshoot AD Kerberos failures: klist ticket flow, missing or duplicate SPNs, clock skew, encryption-type mismatches, keytabs, double-hop delegation and NTLM fallback."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/windows-security/kerberos-authentication-troubleshooting-guidance
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setspn
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/klist
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ktpass
  - https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4768
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos authentication troubleshooting — follow the ticket

**Goal:** when SSO fails, prompts for passwords, or "works with IP but not with name",
pin the failure to one step of the Kerberos exchange and fix that step.

## 1. The flow in one breath
Client gets a **TGT** from the KDC (AS-REQ, event **4768** on the DC), then asks for a
**service ticket** for the target's SPN (TGS-REQ, event **4769**), then presents it to the
service, which decrypts it with *its own account's* key. Every failure is one of:
can't reach/trust the KDC, the SPN maps to no/two/the wrong account, keys or encryption
types disagree, or time is off.

## 2. Look at the client first
```cmd
klist                       rem cached tickets: server SPN, etype, flags, KDC used
klist purge                 rem drop tickets (logon session); retest
klist get HTTP/app.corp.example
klist purge -li 0x3e7       rem SYSTEM/computer account tickets (services, GPO)
```
If there's **no ticket for the service SPN** after the access attempt, the client either
failed to get one (see DC events) or never tried, and silently fell back to **NTLM**.
Check on the server: Security event 4624 *Authentication Package* = NTLM vs Kerberos.

A common reason the client never tries Kerberos: the target was accessed by **IP address** or by an alias
that has no SPN registered.

## 3. SPN problems — the #1 cause
```cmd
setspn -Q HTTP/app.corp.example     rem who owns it? (add -F for the whole forest)
setspn -L svc-app                   rem SPNs on an account
setspn -X -F                        rem find duplicates across the forest
setspn -S HTTP/app.corp.example svc-app   rem -S checks for duplicates before adding (never use -A)
```
- **Missing SPN**: `KDC_ERR_S_PRINCIPAL_UNKNOWN` (the SPN is associated with no account; 4768/4769 result code 0x7 means the server was not found in the Kerberos database), NTLM fallback.
- **Duplicate SPN**: `KDC_ERR_PRINCIPAL_NOT_UNIQUE` (the SPN is associated with more than one account).
- **SPN on the wrong account or a clock/uniqueness problem**: the client cannot decrypt the service ticket, logged as `KRB_AP_ERR_MODIFIED` (System log, event ID 4). More than one issue causes it (clock skew, a non-unique SPN, the SPN on the wrong account), so read the related events.
- Register SPNs for **both** short name and FQDN.

## 4. Time
Default maximum tolerance for computer clock synchronization is **5 minutes** (Kerberos policy). `KRB_AP_ERR_SKEW` (0x25) is logged when the client timestamp differs from the server's by more than that.
```cmd
w32tm /query /status
```
By default domain members synchronize with a domain controller, and a PDC emulator synchronizes with a reliable source in its own domain or a DC in the parent domain; the forest-root PDC emulator can be pointed at an external NTP source.

## 5. Encryption types
`KDC_ERR_ETYPE_NOSUPP` (0xE): the KDC has no support for the encryption type, usually because a packet cannot be decrypted. Check the 4768/4769 `Ticket Encryption Type` (0x12 = AES256-CTS-HMAC-SHA1-96, 0x11 = AES128-CTS-HMAC-SHA1-96, 0x17 = RC4-HMAC) and the account's `msDS-SupportedEncryptionTypes`, which the DC uses to decide what the server supports.

## 6. Keytabs (non-Windows services)
```cmd
ktpass /princ HTTP/app.corp.example@CORP.EXAMPLE /mapuser svc-app /crypto AES256-SHA1 /ptype KRB5_NT_PRINCIPAL /pass * /out app.keytab
```
`ktpass` maps the principal to the domain account and writes the keytab. Check the keytab and `kinit` behaviour on the Linux side with that platform's Kerberos documentation.

## 7. Double hop
- A front end that must act as the user toward a back end (web app to SQL) needs
  **constrained delegation** (or RBCD) to the back-end SPN. Unconstrained is not the answer
  (see `computing-software.systems-network-administration.active-directory.ad-security-hardening`). Both forms are described in the Microsoft constrained delegation overview.

## 8. DC side
Failed 4768/4771 with result codes (0x18 bad password, 0x25 skew) and 4769 failures
pinpoint which step broke. Enable Kerberos auditing (*Audit Kerberos Authentication
Service / Service Ticket Operations*: Failure) if it's off.

## Verify
- [ ] After access, `klist` shows a ticket for the exact SPN with an AES etype.
- [ ] Server logon event shows Kerberos, not NTLM.
- [ ] `setspn -X -F` returns no duplicates; the SPN sits on the account that runs the service.
- [ ] Clock offset between client, server and DC is well inside the 5-minute tolerance.

## Checked
Checked 2026-10-27 against Microsoft Learn (Kerberos authentication troubleshooting guidance; events 4768, 4769 and 4771; Kerberos policy settings pages; setspn, klist and ktpass references; Windows Time Service articles; constrained delegation overview).
- Confirmed: klist purge -li 0x3e7; setspn -Q, -L, -X, -F and -S (setspn -A is allowed but -S checks for duplicates); KRB_AP_ERR_MODIFIED is event ID 4 with multiple possible causes; KDC_ERR_S_PRINCIPAL_UNKNOWN and KDC_ERR_PRINCIPAL_NOT_UNIQUE meanings; result codes 0x7, 0xE, 0x18 (reported in 4771) and 0x25; encryption types 0x11, 0x12 and 0x17; 5-minute default clock tolerance; ktpass /crypto AES256-SHA1 and /ptype KRB5_NT_PRINCIPAL; audit subcategory names.
- Removed: browser zone/allowlist remark, the useAppPoolCredentials claim, MaxTokenSize and HTTP header advice, hypervisor time-sync advice, the pre-AES password remark, and the Linux kinit/krb5.conf/KVNO guidance, none confirmed in readable sources.

Method: documentation only; no commands were run.
