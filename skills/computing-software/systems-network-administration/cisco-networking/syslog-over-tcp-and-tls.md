---
id: computing-software.systems-network-administration.cisco-networking.syslog-over-tcp-and-tls
name: syslog-over-tcp-and-tls
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, syslog, syslog-tls, logging-host-transport, rfc5425, rsyslog, secure-logging]
level: practitioner
status: draft
description: "Send IOS XE syslog over TCP or TLS (RFC 5425) to rsyslog or syslog-ng: transport config, trustpoints, collector setup and what happens when the TCP peer is down."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/esm/configuration/xe-16/esm-xe-16-book/esm-sys-msg-log.html
  - https://datatracker.ietf.org/doc/html/rfc5425
  - https://www.rsyslog.com/doc/configuration/modules/imtcp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syslog over TCP and TLS

## Why
UDP syslog (514) is unreliable and plaintext; messages vanish under congestion and can be read
or spoofed. TCP adds delivery; TLS (RFC 5425, TCP 6514) adds encryption and server authentication.

## IOS XE
```
logging host 10.0.0.50 transport tcp port 1514
! TLS:
crypto pki trustpoint SYSLOG-CA
 enrollment terminal
 revocation-check none
crypto pki authenticate SYSLOG-CA          ! paste the CA that signed the collector cert
logging host 10.0.0.50 transport tls port 6514 profile SYSLOG-TLS
logging tls-profile SYSLOG-TLS
 ciphersuite aes-128-cbc-sha aes-256-cbc-sha
 tls-version TLSv1.2
```
Exact `logging tls-profile` options vary by release; check `logging tls-profile ?`.

## rsyslog collector
```
# /etc/rsyslog.d/10-tls.conf
global(DefaultNetstreamDriver="gtls"
       DefaultNetstreamDriverCAFile="/etc/rsyslog/ca.pem"
       DefaultNetstreamDriverCertFile="/etc/rsyslog/server.pem"
       DefaultNetstreamDriverKeyFile="/etc/rsyslog/server.key")
module(load="imtcp" StreamDriver.Name="gtls" StreamDriver.Mode="1" StreamDriver.AuthMode="anon")
input(type="imtcp" port="6514")
```
`AuthMode="anon"` encrypts without validating the client; use `x509/name` if the routers have certificates.

## Behaviour to know
- TCP logging buffers when the collector is down; the buffer is finite and messages beyond it are dropped.
  Keep `logging buffered` locally as a backstop.
- Framing: IOS XE uses octet-counting for TCP/TLS; the collector must accept it (rsyslog does).
- Firewalls must allow TCP 6514/1514 from the logging source interface (`logging source-interface Loopback0`).

## Verify
```
show logging | include Logging to|tls|tcp
```
Collector: `ss -tnp | grep 6514` shows an established session from each device; `openssl s_client -connect <collector>:6514` validates the server cert.
