---
id: computing-software.systems-network-administration.wireshark.ntlmssp-authentication-analysis
name: ntlmssp-authentication-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ntlmssp, ntlm, authentication, smb2, http-auth]
level: practitioner
status: verified
description: "Analyse NTLMSSP negotiate/challenge/authenticate in Wireshark across SMB, HTTP and LDAP, identify users and NTLMv1 use, and diagnose auth failures."
sources:
  - https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-nlmp/
  - https://www.wireshark.org/docs/dfref/n/ntlmssp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTLMSSP authentication analysis

## Three messages
1. NEGOTIATE (type 1): client flags.
2. CHALLENGE (type 2): server challenge, target info (domain, server names), flags.
3. AUTHENTICATE (type 3): user, domain, workstation, NT/LM responses.

## Filters
```
ntlmssp
ntlmssp.messagetype == 0x00000003
ntlmssp.auth.username
ntlmssp.auth.domain
ntlmssp.auth.hostname
ntlmssp.ntlmv2_response              # NTLMv2
ntlmssp.auth.ntresponse && !ntlmssp.ntlmv2_response   # NTLMv1: weak, should be blocked
smb2.cmd == 1 && smb2.nt_status != 0 && smb2.nt_status != 0xc0000016   # failed SMB session setup
```
`smb2.cmd == 1` is Session Setup; `0xc0000016` is STATUS_MORE_PROCESSING_REQUIRED, excluded here so that this status
is not listed as a failure.
Transport examples: SMB2 SESSION_SETUP, HTTP `WWW-Authenticate: NTLM` / `Negotiate`, LDAP bind,
MS-RPC.

## Why NTLM instead of Kerberos?
NTLM appears when Kerberos failed or was not possible: connecting by IP address, missing/duplicate
SPN, client not domain joined, DC unreachable on 88. Check for preceding Kerberos errors
(`kerberos.error_code`) in the same seconds.

## Failure diagnosis
| Status after AUTHENTICATE | Meaning |
|---------------------------|---------|
| STATUS_LOGON_FAILURE (0xc000006d) | bad password or user |
| STATUS_ACCOUNT_LOCKED_OUT (0xc0000234) | locked |
| STATUS_PASSWORD_EXPIRED (0xc0000071) | expired |
| STATUS_ACCESS_DENIED after success | authorisation, not authentication |

## Security notes
- Enforce NTLMv2 only: `LmCompatibilityLevel` 5 = clients send NTLMv2 only and
  domain controllers refuse LM and NTLM (Microsoft policy page).
- `ntlmssp.negotiatesign` shows whether the AUTHENTICATE message's flags include signing (it was false in the test
  messages).
- Captures contain NTLM challenge/response data; treat them as sensitive.

## Verify
- [ ] The user and host in AUTHENTICATE match the expected account, and the result status is success.

## Checked
Run with TShark 4.4.1 on generated NTLM messages carried in HTTP `Authorization: NTLM` headers: type 1, 2 and 3
messages matched `ntlmssp`; `ntlmssp.messagetype == 0x00000003`, `ntlmssp.auth.username`/`domain`/`hostname`
extracted `alice`, `EXAMPLE`, `WS1`; an NTLMv2 AUTHENTICATE carried `ntlmssp.ntlmv2_response` (and also
`ntlmssp.auth.ntresponse`), while a 24-byte NTLMv1 response matched `ntlmssp.auth.ntresponse &&
!ntlmssp.ntlmv2_response`; `ntlmssp.negotiatesign` printed False. SMB2 command 1 = Session Setup and the four NT status
values (0xc000006d, 0xc0000234, 0xc0000071, 0xc0000016) read from `tshark -G values` and Microsoft's MS-ERREF
table; LmCompatibilityLevel text from the Microsoft policy page. No SMB2 traffic was generated.
