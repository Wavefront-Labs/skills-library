---
id: computing-software.systems-network-administration.samba.smb-protocol-security
name: smb-protocol-security
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smb-protocol-security, server-signing, smb-encryption, smb-conf, tls]
level: advanced
status: docs-checked
description: "Set Samba SMB protocol versions, signing, encryption, NTLM and TLS options with their defaults, for both server and client sides, plus multichannel and port settings."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smb protocol security
Server side (`[global]` unless noted):
- `server min protocol` default `SMB2_02` (set `NT1` only for SMB1-only legacy clients); `server max protocol` default `SMB3`.
- `server signing` default `default`: required on AD DCs, disabled otherwise; SMB2 signing cannot be fully disabled.
- `server smb encrypt` (per share too) default `default` (acts as `if_required`); values `off`, `if_required`, `desired`, `required`.
- `ntlm auth` default `ntlmv2-only`; other values `yes`, `no`, `mschapv2-and-ntlmv2-only`, `disabled`.
- `ldap server require strong auth` default `yes`.
- `restrict anonymous` default `0`; `null passwords` default `no`.
- `server smb transports` default `tcp, nbt` (port 445 raw TCP, port 139 NetBIOS framing; `quic` is optional); `smb ports` is a synonym with no default of its own.
- `server multi channel support` default `yes` (since 4.15 on Linux/FreeBSD).
- `machine password timeout` default `604800` seconds.

Client side: `client min protocol` `SMB2_02`, `client max protocol` `default` (SMB3_11), `client smb encrypt` `default`, `client signing` `default`, `client use kerberos` `desired`. Deprecated since 4.13: `client NTLMv2 auth` (yes), `client lanman auth` (no), `client plaintext auth` (no).

TLS: `tls enabled` `yes`; `tls keyfile` `tls/key.pem`; `tls certfile` `tls/cert.pem`; `tls cafile` `tls/ca.pem`; relative paths resolve against `private dir`.

Verify the effective value with `testparm -sv --parameter-name="server min protocol"`.

## Checked

2026-11-04. Confirmed against the smb.conf(5) and testparm(1) manual pages: every default listed above, the 4.13 deprecations, the 4.15 multichannel default, SMB2 signing note, server smb encrypt values, `--parameter-name` and `-v`/`-s` options of testparm. Reworded the smb ports line (the page defaults server smb transports to `tcp, nbt`). Removed the smbclient option line (smbclient page not read).
Method: documentation only; no commands were run.
