---
id: computing-software.systems-network-administration.zabbix.psk-encryption
name: psk-encryption
category: computing-software
field: systems-network-administration
product: zabbix
tags: [psk, encryption, tls, pre-shared-key, tlsconnect]
level: advanced
status: docs-checked
description: "Encrypt agent, proxy and server traffic with pre-shared keys: identity, key size limits and configuration."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/encryption/using_pre_shared_keys
  - https://www.zabbix.com/documentation/current/en/manual/encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A PSK is a pair: a non-secret identity string and a secret hex value. The identity is a non-empty UTF-8 string, sent unencrypted over the network, so never put sensitive text in it. Never reuse example PSK values from the documentation.

Limits: identity up to 128 UTF-8 characters in Zabbix (127 bytes with OpenSSL). Value from 128 bits (32 hex digits) up to 2048 bits (512 hex digits). OpenSSL 1.1.1 allows only up to 512 bits (128 hex digits), but 1.1.1a and later allow 2048. The frontend accepts up to 2048 regardless, so staying within your crypto library's limit is your job; exceeding it breaks communication.

Each identity must map to exactly one value. Two keys with the same identity and different values cause unpredictable failures.

Generate a 256-bit key with openssl rand -hex 32 and save it in a PSK file.

Agent example:
TLSConnect=psk
TLSAccept=psk
TLSPSKFile=/path/to/zabbix_agentd.psk
TLSPSKIdentity=PSK 001
Then set the host's Connections to and from host to PSK in the frontend and enter the same identity and key. Restart the agent.

Proxy: set TLSConnect=psk (active proxy) with its own file and identity, or TLSAccept=psk for a passive proxy, and set Connections to proxy to PSK in the frontend.

On mismatch, check the troubleshooting page for PSK problems.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (encryption/using_pre_shared_keys; encryption): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
