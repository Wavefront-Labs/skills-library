---
id: computing-software.systems-network-administration.cisco-networking.https-management-with-trustpoint
name: https-management-with-trustpoint
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ip-http-secure-server, https-management, trustpoint, crypto-pki, webui, restconf, self-signed-certificate]
level: practitioner
status: draft
description: "Run IOS XE HTTPS management (WebUI/RESTCONF) on a proper trustpoint certificate, restrict ciphers and access, and disable plain HTTP."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/https/configuration/xe-16/https-xe-16-book/nm-http-web.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_pki/configuration/xe-16/sec-pki-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTPS management with a trustpoint

## Certificate
Self-signed (`TP-self-signed-xxxx`) is created automatically but browsers and tools distrust it.
Enrol a CA-signed cert:
```
crypto key generate rsa label HTTPS-KEY modulus 2048 exportable
crypto pki trustpoint HTTPS-TP
 enrollment terminal pem
 subject-name CN=sw1.example.net
 subject-alt-name sw1.example.net
 rsakeypair HTTPS-KEY
 revocation-check none
crypto pki enroll HTTPS-TP          ! prints CSR; sign it on your CA
crypto pki authenticate HTTPS-TP    ! paste issuing CA cert
crypto pki import HTTPS-TP certificate   ! paste signed device cert
```
Or SCEP/EST enrollment with `enrollment url`.

## HTTPS server
```
no ip http server                         ! no plain HTTP
ip http secure-server
ip http secure-trustpoint HTTPS-TP
ip http secure-ciphersuite aes-128-cbc-sha aes-256-cbc-sha ecdhe-rsa-aes-128-gcm-sha256
ip http tls-version TLSv1.2
ip http authentication aaa login-authentication HTTP-AUTH   ! or local
ip http access-class ipv4 MGMT-ACL
ip http max-connections 5
ip http timeout-policy idle 600 life 86400 requests 10000
```
`ip http client` settings are separate (device as HTTP client).

## Gotchas
- Changing trustpoints restarts the HTTPS server; sessions drop.
- Certificate expiry silently breaks RESTCONF automation: monitor `show crypto pki certificates HTTPS-TP`.
- `ip http secure-server` with no ACL exposes the WebUI on every interface including WAN.
- Old CVEs (e.g. CVE-2023-20198 WebUI) were exploited on internet-facing HTTP(S): never expose management to the internet.

## Verify
```
show ip http server secure status         ! trustpoint, ciphers, TLS version
openssl s_client -connect <DEVICE>:443 -servername sw1.example.net
```
- [ ] Cert chain validates, TLS 1.2+, HTTP port 80 closed.
