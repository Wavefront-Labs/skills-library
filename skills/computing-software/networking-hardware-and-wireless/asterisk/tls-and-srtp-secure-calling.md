---
id: computing-software.networking-hardware-and-wireless.asterisk.tls-and-srtp-secure-calling
name: tls-and-srtp-secure-calling
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, tls, srtp, sdes, ast-tls-cert, certificates, secure-calling, media-encryption, transport]
level: practitioner
status: docs-checked
description: "Set up TLS signalling and SRTP media for PJSIP: generate CA, server and client certificates with ast_tls_cert, a protocol=tls transport, and media_encryption=sdes on the endpoint."
sources:
  - https://docs.asterisk.org/Deployment/Secure-Calling/Secure-Calling-Tutorial/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS and SRTP secure calling
TLS encrypts signalling (hides who you call); SRTP encrypts media. The tutorial uses the Blink softphone.

**Keys.** Create a keys directory, then run `ast_tls_cert` (from `contrib/scripts` in the source):
- Server: `-C <host or IP> -O "<organisation>" -d <dir> -b 2048`. It prompts for a CA passphrase and creates `ca.key`, `ca.crt`, `asterisk.key`, `asterisk.crt`, `asterisk.pem`.
- Client: `-m client -c <ca.crt> -k <ca.key> -C <phone host> -O ... -d <dir> -o <name> -b 2048`.
Copy the client `.pem` and `ca.crt` to the phone. For a `.p12`, use `openssl pkcs12 -export`.

**PJSIP transport:**
```
[transport-tls]
type=transport
protocol=tls
bind=0.0.0.0:5061
cert_file=/path/to/keys/asterisk.crt
priv_key_file=/path/to/keys/asterisk.key
method=sslv23
```
**Endpoint:** a normal aor (`max_contacts`, `remove_existing`), auth (`userpass`) and endpoint with `media_encryption=sdes`.

Do not set `transport=` on the endpoint: with pjproject at least as late as 2.4.5 it can cause "Connection refused". Let pjproject choose; if problems remain set `rewrite_contact = yes`.

For legacy chan_sip: `tlsenable=yes`, `tlsbindaddr`, `tlscertfile`, `tlscafile`, and peer `transport=tls`.

The tutorial's SRTP part is written for chan_sip: libsrtp must be installed before Asterisk is built, and the peer gets `encryption=yes`.

Use a better password than the tutorial's.

## Checked
2026-11-09: read the cited Secure Calling Tutorial in full and confirmed the ast_tls_cert options and output files, the PJSIP transport and endpoint examples, the transport= warning, the chan_sip settings and the libsrtp note. Added the SRTP and libsrtp note. Nothing else removed.

Method: documentation only; no commands were run.
