---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.kerberos-and-ntlm-traffic-analysis
name: kerberos-and-ntlm-traffic-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [kerberos-traffic, ntlm-traffic, kerberoasting, as-rep-roasting, pass-the-hash, wireshark, active-directory, dfir]
level: advanced
status: verified
description: "Analyse Kerberos (AS, TGS, AP) and NTLM authentication on the wire to spot roasting, pass-the-hash, forged tickets and spraying, using Wireshark filters."
sources: ["https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-kile/2a32282e-dd48-4ad9-a542-609804b02cc9", "https://wiki.wireshark.org/Kerberos", "https://attack.mitre.org/techniques/T1558/003/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos and NTLM authentication traffic

**Goal:** use packet data from DC-adjacent sensors to identify credential attacks that host
logs may only partially record.

## Kerberos basics on the wire (TCP/UDP 88)
| msg_type | Message |
|---|---|
| 10 / 11 | AS-REQ / AS-REP (get TGT) |
| 12 / 13 | TGS-REQ / TGS-REP (get service ticket) |
| 14 / 15 | AP-REQ / AP-REP (present ticket to a service, inside SMB/HTTP/LDAP) |
| 30 | KRB-ERROR (e.g. `KDC_ERR_PREAUTH_REQUIRED` 25, `KDC_ERR_PREAUTH_FAILED` 24, `KDC_ERR_C_PRINCIPAL_UNKNOWN` 6) |
Columns: `kerberos.CNameString`, `kerberos.SNameString`, `kerberos.realm`, `kerberos.etype`,
`kerberos.ENCTYPE`, `kerberos.error_code`.

## Attack signatures
- **Kerberoasting:** one client sends many TGS-REQs for different SPNs in a short time,
  requesting RC4 in an AES environment. In Wireshark 4.4.1 the encryption types a TGS-REQ asks for are
  `kerberos.ENCTYPE`, while `kerberos.etype` is the type of an EncryptedData blob (the ticket in a reply, or the
  ticket and authenticator inside the request), so `kerberos.msg_type == 12 && kerberos.etype == 23` matches
  nothing for a plain RC4 request. Use `kerberos.msg_type == 12 && kerberos.ENCTYPE == 23` for the request and
  `kerberos.msg_type == 13 && kerberos.etype == 23` for the RC4 ticket the KDC actually issued.
- **AS-REP roasting:** AS-REQ without pre-auth data for accounts with "do not require
  pre-auth"; AS-REP returned without a prior error 25:
  `kerberos.msg_type == 11` from accounts you would expect to require pre-auth.
- **User enumeration / spraying:** many AS-REQs producing error 6 (unknown principal) or 24
  (bad password) from one source: `kerberos.error_code in {6, 24}`.
- **Golden ticket:** AP-REQ/TGS-REQ using a TGT that was never issued in an AS-REP seen by the
  sensor, unusual ticket lifetime, or RC4 TGT in an AES-only domain.
- **Overpass-the-hash:** AS-REQ with RC4 pre-auth from a workstation that normally uses AES.

## NTLM (inside SMB, HTTP, LDAP)
Filter `ntlmssp`; fields `ntlmssp.messagetype` (1 negotiate, 2 challenge, 3 auth),
`ntlmssp.auth.username`, `ntlmssp.auth.domain`, `ntlmssp.auth.hostname`,
`ntlmssp.ntlmv2_response` (NTLMv2) vs NTLMv1 (`ntlmssp.auth.ntresponse` of 24 bytes: weak).
- **Pass-the-hash:** NTLM auth to many hosts from one source using an admin account, with
  workstation name mismatching the source host, often where Kerberos would be expected.
- **Relay:** authentication arriving at a server from an IP different from the workstation
  named in `ntlmssp.auth.hostname`; coerced auth (MS-EFSR calls on the `efsrpc` or `lsarpc`
  pipe, or MS-RPRN print-spooler calls) preceding it.

## Decryption
With the service account keys in a keytab (Preferences > Protocols > KRB5: enable "Try to decrypt Kerberos blobs", `kerberos.decrypt`, and set the keytab file, `kerberos.file`), Wireshark
decrypts ticket parts to show PAC contents; useful for confirming forged tickets in a lab.

## Self-check
Each finding names source host, account, target SPN/service, encryption type and message
sequence, and is corroborated with DC events (4768, 4769, 4771, 4776).

## Checked
Run on Wireshark 4.4.1 with a scapy-built capture (KRB-ERROR 6, 24 and 25; TGS-REQ for RC4 and AES; AS-REQ with RC4;
TGS-REP with an RC4 and an AES ticket): `kerberos.msg_type`, `kerberos.error_code` (6 = C_PRINCIPAL_UNKNOWN,
24 = PREAUTH_FAILED, 25 = PREAUTH_REQUIRED), the comma set filter and `kerberos.ENCTYPE`/`kerberos.etype` behaved as
described above, and the message-type table (10 to 15, 30), `ntlmssp.messagetype` values 1 to 3 and every field name
exist in `tshark -G fields`/`-G values`. Event IDs 4768, 4769, 4771 and 4776 were checked against Microsoft Learn,
the `efsrpc` pipe against MS-EFSR, and the dissector's NTLMv1 handling is built on 24-byte responses (Wireshark
source). The attack signatures are heuristics to corroborate, not proof.
