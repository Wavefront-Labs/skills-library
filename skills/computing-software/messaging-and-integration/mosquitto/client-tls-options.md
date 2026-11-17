---
id: computing-software.messaging-and-integration.mosquitto.client-tls-options
name: client-tls-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [tls, cafile, insecure, tls-use-os-certs]
level: practitioner
status: docs-checked
description: "Enable TLS in mosquitto_pub and mosquitto_sub with --cafile, --capath, --cert and --key, and know when port 8883 turns it on."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: connect clients over TLS.

- `--cafile file` or `--capath dir` enables TLS with x509 certificates. For `--capath` the files need a `.crt` ending and `openssl rehash <path>` must be run after changes.
- If `-p 8883` is used, the OS-provided certificates are loaded and neither `--cafile` nor `--capath` is needed. `--tls-use-os-certs` does this explicitly and is also set by `-L mqtts://...`.
- `--cert file` and `--key file` give the client certificate and private key for mutual TLS.
- `--ciphers` is an openssl cipher list; `--tls-version tlsv1.3|tlsv1.2` (default tlsv1.2) must match the broker.
- `--tls-alpn protocol` for brokers serving multiple protocols on one port.
- `--insecure` disables server hostname verification; testing only. The docs say it allows impersonation by DNS spoofing.
- `--no-tls` (2.1) disables all TLS, including the automatic use on port 8883.
- `--tls-keylog file` (2.1) logs TLS secrets for Wireshark or tcpdump decryption; debugging only.
- `--tls-engine`, `--keyform pem|engine` and `--tls-engine-kpass-sha1` for TPM-style engines.

TLS-PSK instead of certificates: `--psk hex-key --psk-identity identity`, both required.

```
mosquitto_pub -h broker.example.com -p 8883 --cafile /path/to/ca.crt -t a/b -m hi
```

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
