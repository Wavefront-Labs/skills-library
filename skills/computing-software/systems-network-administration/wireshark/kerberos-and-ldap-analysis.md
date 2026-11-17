---
id: computing-software.systems-network-administration.wireshark.kerberos-and-ldap-analysis
name: kerberos-and-ldap-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, kerberos-analysis, ldap-analysis, active-directory, krb-error, clock-skew, ldap-bind, keytab]
level: practitioner
status: verified
description: "Troubleshoot AD authentication from captures: Kerberos AS/TGS exchanges and KRB_ERROR codes, clock skew, SPN errors, LDAP binds and result codes, and keytab decryption."
sources:
  - https://www.rfc-editor.org/rfc/rfc4120
  - https://www.wireshark.org/docs/dfref/k/kerberos.html
  - https://wiki.wireshark.org/Kerberos
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos and LDAP analysis

## Kerberos exchanges (TCP/UDP 88)
- AS-REQ / AS-REP: user gets a TGT (first logon, `kinit`).
- TGS-REQ / TGS-REP: TGT exchanged for a service ticket for an SPN (`HTTP/web01.example.net`).
- AP-REQ: ticket presented to the service (inside SMB, HTTP Negotiate, LDAP SASL).
```
kerberos
kerberos.msg_type == 30              # KRB_ERROR
kerberos.error_code
kerberos.SNameString == "HTTP"       # service names requested
```

## Common KRB_ERROR codes
| Code | Name | Meaning |
|---|---|---|
| 6 | KDC_ERR_C_PRINCIPAL_UNKNOWN | user/computer account not found |
| 7 | KDC_ERR_S_PRINCIPAL_UNKNOWN | SPN not registered (or duplicate): fix with `setspn` |
| 18 | KDC_ERR_CLIENT_REVOKED | account disabled/locked/expired |
| 23 | KDC_ERR_KEY_EXPIRED | password expired |
| 24 | KDC_ERR_PREAUTH_FAILED | wrong password |
| 25 | KDC_ERR_PREAUTH_REQUIRED | normal first round trip, not an error |
| 37 | KRB_AP_ERR_SKEW | clock difference beyond the tolerance (Microsoft's best-practice setting is 5 minutes) |
| 14 | KDC_ERR_ETYPE_NOSUPP | encryption type mismatch (RC4 disabled, AES not enabled on account) |
| 52 | KRB_ERR_RESPONSE_TOO_BIG | UDP response too large, client retries over TCP (normal) |

Wireshark's Info column prints these as `KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN`, `KRB5KDC_ERR_KEY_EXP`,
`KRB5KRB_AP_ERR_SKEW` and so on; the numbers match the table (all nine checked).
Error 25 followed by a successful AS-REP is the normal pre-authentication dance; do not chase it.

## Decrypting tickets
With a keytab (service or krbtgt keys, lab or with authorisation): Preferences > Protocols >
KRB5 (`kerberos.decrypt` = try to decrypt Kerberos blobs, `kerberos.file` = the keytab). The decrypted parts then appear in the
dissection tree.

## LDAP (389, 636 LDAPS)
```
ldap.protocolOp == 0                 # bindRequest
ldap.resultCode != 0
ldap.bindRequest_element && ldap.simple   # simple bind: password in clear on 389!
```
Result codes (names as Wireshark prints them): 49 invalidCredentials (Active Directory puts a Windows error code in
the message as `data 52e`: 0x52E = ERROR_LOGON_FAILURE, user name or password incorrect; 0x532 password expired;
0x533 account disabled; 0x775 account locked out), 8 strongAuthRequired (RFC 4511 `strongerAuthRequired`: the server wants stronger authentication),
32 noSuchObject (wrong base DN).

## Gotchas
- LDAP protected by SASL signing or sealing, or by TLS on 636, cannot be read without keys; the cleartext bind result
  on 389 still shows the result code.
- Kerberos over TCP may be split across segments; enable TCP reassembly.

## Verify
- [ ] For an authentication failure you can name the request type, the principal/SPN, the error
  code and the DC that answered.

## Checked
Run with TShark 4.4.1 on generated KRB-ERROR messages (codes 6, 7, 14, 18, 23, 24, 25, 37, 52 over UDP/88): all matched
`kerberos`, `kerberos.msg_type == 30`, `kerberos.error_code` and `kerberos.SNameString == "HTTP"`; error names read from
`tshark -G values` (eRR-C-PRINCIPAL-UNKNOWN, ..., eRR-RESPONSE-TOO-BIG). A hand-encoded LDAP simple bind and an
`invalidCredentials` response with `data 52e` matched `ldap.protocolOp == 0`, `ldap.resultCode != 0` and
`ldap.bindRequest_element && ldap.simple` (the password printed in clear). Windows error codes confirmed against
Microsoft's System Error Codes pages (1326 0x52E, 1330 0x532, 1331 0x533, 1909 0x775); 5-minute tolerance from the
Microsoft policy page. `kerberos.decrypt`, `kerberos.file`, `kerberos.desegment` and `ldap.tls.port` 636 read from
`-G currentprefs`. For keytab decryption the text only names the preferences.
